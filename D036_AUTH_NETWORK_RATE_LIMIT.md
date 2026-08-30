# D036_AUTH_NETWORK_RATE_LIMIT.md — Authentication network-signal throttling decision packet

**Status:** `DECISION_PENDING`  
**Epistemic state:** proposal for owner review; not released for implementation  
**Affected contract:** [AUTH.md](AUTH.md) §3  
**Affected clients:** `suas` web/API, `suas-ios`, and `suas-android` through the shared `/api/v0` challenge boundary  
**Production authority:** none

## 1. Decision requested

Choose the network-signal policy that complements the released persistent destination/account challenge limits.

The owner must settle all of these together:

1. issuance threshold and window;
2. authoritative client-address source at each runtime boundary;
3. behavior when no trustworthy address is available;
4. privacy-safe subject derivation and retention;
5. response and audit behavior;
6. rollout boundary for synthetic STAGING, a future pilot, and production.

Merging this packet without an explicit owner decision does not authorize implementation. No runtime default may silently choose an option.

## 2. Existing authority and observed implementation state

### Released

- [AUTH.md](AUTH.md) §3 requires challenge throttling by address/account and network signal where appropriate.
- Correctness and abuse-control counters must be shared or equivalently distributed. Process-local counters are not authoritative.
- [API.md](API.md) §6 assigns HTTP `429` to rate/backpressure limits.
- [PRIVACY.md](PRIVACY.md) requires minimization and allows only device telemetry required by authentication/session security.
- [AGENTS.md](AGENTS.md) prohibits inventing deferred product rules in implementation.

### Observed in `scrimshawlife-ctrl/suas` after runtime PR #149

- Challenge issuance is persistently limited by normalized destination.
- The released destination budget is three issuances per 15 minutes.
- Rate-limited HTTP responses use canonical `RATE_LIMITED` bodies and a positive `Retry-After` header.
- The Worker dispatch boundary maps Cloudflare `CF-Connecting-IP` into Fastify's request peer address.
- Direct Node execution has a socket peer address and no configured trusted-proxy chain.
- No network subject is currently consumed by the challenge service.

Observed code is not a product decision and does not settle this packet.

## 3. Threat and usability model

The network signal is a coarse abuse control, not identity proofing and not authorization.

It should reduce:

- distributed challenge flooding against many destinations from one source;
- provider-cost abuse;
- enrollment probing at volume despite uniform public responses;
- pressure on shared challenge and audit storage.

It must not:

- identify a veteran;
- reveal whether a destination is enrolled;
- block an entire shelter, library, carrier NAT, or shared household under ordinary use;
- trust attacker-supplied forwarding headers;
- store raw network addresses longer than required for the active abuse-control window;
- create a production-readiness claim.

## 4. Options

### Option A — conservative shared-network budget

- **Budget:** 10 challenge issuances per 15 minutes per network subject.
- **Benefit:** stronger provider-cost and flood protection.
- **Risk:** elevated false positives for shelters, libraries, clinics, carrier NAT, and shared responder networks.
- **Assessment:** not recommended for the initial controlled-pilot shape without evidence that shared-network use is rare.

### Option B — balanced shared-network budget

- **Budget:** 20 challenge issuances per 15 minutes per network subject.
- **Benefit:** caps broad spraying while allowing multiple legitimate users behind one shared address.
- **Risk:** a determined attacker can still distribute traffic across networks; shared sites can still exhaust the budget during bursts.
- **Assessment:** `INFERRED` recommendation for synthetic-STAGING rehearsal and a future controlled pilot. It is not owner-approved until explicitly settled.

### Option C — no fixed network budget yet

- Retain destination limits only and collect privacy-safe aggregate evidence before setting a network threshold.
- **Benefit:** avoids an unsupported false-positive threshold.
- **Risk:** leaves provider-cost and multi-destination spray abuse controlled only by destination buckets and provider-side limits.
- **Assessment:** valid fail-closed governance choice if the owner will not yet authorize a numeric threshold. It does not satisfy a claim that network throttling is implemented.

### Option D — adaptive/risk-based network scoring

- Vary limits using reputation, device signals, geography, or behavior scoring.
- **Assessment:** rejected for this release. It expands collection, explainability, privacy, vendor, and false-positive scope beyond the released MVP.

## 5. Proposed trust policy

This section is `PROPOSED`, not released.

| Runtime boundary | Proposed authoritative source | Headers not trusted |
|---|---|---|
| Cloudflare Worker | The Worker-runtime `CF-Connecting-IP` value forwarded into the in-process Fastify peer address | Client-supplied `X-Forwarded-For`, `Forwarded`, or arbitrary address headers |
| Direct Node server | The immediate socket peer address | Forwarding headers unless a later deployment decision names and configures trusted proxies |
| Test/in-process injection | Explicit synthetic `remoteAddress` fixture | Ambient machine or CI metadata |
| No trustworthy address | One shared `_unknown` subject | Silently skipping the network limiter |

If a later production topology adds another proxy, the deployment must explicitly name the trusted hop and add conformance evidence. A generic `trust proxy = true` configuration is insufficient.

## 6. Proposed privacy design

This section is `PROPOSED`, not released.

1. Normalize IPv4 and IPv6 text before subject derivation.
2. Derive the persistent bucket subject as a keyed digest of the normalized address and a purpose string such as `auth.challenge.issue.network.v1`.
3. Use a dedicated secret boundary. Do not reuse a session credential, provider key, or database URL as the digest key.
4. Store only the derived subject, fixed window start, count, and timestamps needed by the limiter.
5. Do not write raw addresses or derived subjects to ordinary request, audit, evidence, or provider logs.
6. Remove expired network buckets after the active window plus one cleanup window. This operational cleanup proposal does not settle D-007 retention for veteran/domain records.
7. Rotation of the digest key may invalidate active network buckets and must be treated as a bounded operational event, not silent permanent bypass.

## 7. Proposed behavior

This section is `PROPOSED`, not released.

- Consume the network bucket and destination bucket before user lookup or delivery.
- Require both buckets to allow issuance.
- Preserve the same public response for enrolled and unenrolled destinations while under budget.
- On either exceeded bucket, return canonical HTTP `429`, code `RATE_LIMITED`, and a positive `Retry-After` derived from the limiting bucket.
- Do not send an email or create a challenge after a network rejection.
- Do not include the raw address, derived subject, destination, enrollment state, or bucket type in the public error body.
- Record privacy-safe operational metrics only: bucket type, allowed/limited outcome, and retry-window class. Do not emit combinable address or destination dimensions.

## 8. Acceptance vectors required after a decision

| ID | Given | When | Then |
|---|---|---|---|
| D036-001 | one network subject and distinct unknown destinations | requests stay under both budgets | every request receives the uniform accepted response and no provider message |
| D036-002 | one network subject and enough distinct destinations to exceed the network budget | the next challenge is submitted | response is `429 RATE_LIMITED` with positive `Retry-After`; no challenge or provider send occurs |
| D036-003 | one enrolled destination below its destination budget but a network subject above its budget | a challenge is submitted | network rejection wins before delivery and does not reveal enrollment |
| D036-004 | two different network subjects and one destination | requests are submitted | the shared destination budget remains authoritative across both networks |
| D036-005 | no trustworthy client address | requests exceed the shared `_unknown` budget | unattributable traffic is throttled rather than unmetered |
| D036-006 | spoofed `X-Forwarded-For` or `Forwarded` values | requests arrive through Worker and direct Node boundaries | spoofed values do not create new authoritative subjects |
| D036-007 | IPv4/IPv6 equivalent textual forms | requests are submitted | normalization maps equivalent addresses to one subject |
| D036-008 | a rate-limited request | logs, audit, evidence, and metrics are inspected | no raw address, derived subject, destination, OTP, cookie, or provider credential appears |
| D036-009 | both public STAGING hosts | the network limit is exercised | both hosts observe the same shared persistent bucket |
| D036-010 | native and browser challenge routes | equivalent requests are submitted | both use the same released network policy and canonical error semantics |

## 9. Owner decision form

The owner should record one complete selection. Partial approval does not release implementation.

```text
D-036_STATUS=DECISION_PENDING | DECIDED
NETWORK_OPTION=A | B | C
ISSUE_LIMIT=<integer or NOT_APPLICABLE>
WINDOW_SECONDS=<integer or NOT_APPLICABLE>
WORKER_ADDRESS_SOURCE=CF_CONNECTING_IP | OTHER
NODE_ADDRESS_SOURCE=SOCKET_PEER | TRUSTED_PROXY_POLICY
MISSING_ADDRESS_BEHAVIOR=SHARED_UNKNOWN_BUCKET | OTHER
SUBJECT_STORAGE=KEYED_DIGEST | OTHER
EXPIRED_BUCKET_CLEANUP=<bounded duration or rule>
AUTHORIZED_ENVIRONMENTS=SYNTHETIC_STAGING | CONTROLLED_PILOT | PRODUCTION
OWNER=<name or handle>
DECIDED_AT=<date>
CONSEQUENCES=<short statement>
```

## 10. Status and non-goals

Until the owner completes §9 and releases the coherent cross-artifact change:

- `D-036 = DECISION_PENDING`;
- no threshold in this packet is implementation-authoritative;
- the runtime must retain its released destination/account limits;
- no production, pilot, provider-cost, SLO, privacy-compliance, or abuse-prevention claim is authorized;
- this packet does not modify D-002, D-007, D-021, D-023, D-024, D-025, D-034, or any launch gate.
