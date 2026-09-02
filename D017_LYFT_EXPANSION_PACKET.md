# D017_LYFT_EXPANSION_PACKET.md — Lyft Concierge transportation adapter expansion

**Status:** `DECISION_PENDING` / draft / not implementation authority  
**Owner:** `@scrimshawlife-ctrl`  
**Related:** [DECISIONS.md](DECISIONS.md), [RIDES.md](RIDES.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [ENVIRONMENT.md](ENVIRONMENT.md), [SECURITY.md](SECURITY.md), [RESILIENCE.md](RESILIENCE.md), [PRIVACY.md](PRIVACY.md), [CONSENT.md](CONSENT.md)

## 1. Trigger and observed boundary

The owner reports that Lyft approved the SUAS business account on 2026-09-02. Public Lyft Business material confirms that Lyft Concierge can request rides on behalf of riders and that API clients must be connected to a Lyft Business program and approved in the Lyft Developer Portal before that program can be managed through the API.

This evidence is sufficient to open a D-017 expansion review. It is not yet evidence that:

- a Concierge program is connected to a SUAS API client;
- the API client is approved for that program;
- production credentials, scopes, endpoints, webhooks, quotas, or support escalation are available;
- a sandbox or no-charge test mechanism exists;
- Lyft authorizes SUAS to create a live ride;
- funding, spending controls, rider communications, accessibility handling, privacy, or launch ownership are settled.

The released D-017 decision continues to authorize Uber only as the first API-backed transportation adapter family. Lyft remains a draft stub in [RIDES.md](RIDES.md) until an owner-accepted release supersedes that boundary.

## 2. Proposed decision

Add **Lyft Concierge** as a second replaceable adapter behind the existing provider-neutral `TransportationPort` and Provider Router. This would not replace Uber, Manual, Fake, voucher, volunteer, or information-only paths and would not make Lyft concepts canonical SUAS domain language.

If accepted, the runtime mode should be provider-specific and explicit, for example `lyft_concierge`, rather than overloading `uber_api` or selecting a provider by credential presence.

## 3. Required owner evidence before acceptance

Record status and evidence location for every item. Never place secret values or copied rider data in this repository.

| Gate | Required evidence | Status |
|---|---|---|
| Business account | Independently owned SUAS Lyft Business organization is active | `OWNER_REPORTED` |
| Program | Named Concierge program and accountable business owner | `NOT_OBSERVED` |
| API client connection | Program is connected to the intended SUAS API client and connection is approved | `NOT_OBSERVED` |
| Credential ownership | Client ID/secret are stored in the approved secret boundary; names only in evidence | `NOT_OBSERVED` |
| Authentication contract | Official token endpoint, grant, exact minimum scopes, expiry, and rotation/revocation behavior | `NOT_OBSERVED` |
| API contract | Official quote/create/status/cancel endpoints and version are available to the implementation team | `NOT_OBSERVED` |
| Idempotency | Official create/cancel idempotency semantics or explicit confirmation that none exist | `NOT_OBSERVED` |
| Ambiguous outcomes | Provider lookup/reconciliation path after timeout or unknown create/cancel result | `NOT_OBSERVED` |
| Webhooks | Official event list, signature scheme, replay guidance, retry policy, and status lookup fallback | `NOT_OBSERVED` |
| Test boundary | Sandbox, test mode, or owner-approved no-rider/no-charge validation method | `NOT_OBSERVED` |
| Rider communications | Whether Lyft sends SMS/calls, required phone capability, and accessible no-smartphone fallback | `NOT_OBSERVED` |
| Accessibility | Available ride products, wheelchair/Assisted limits, and truthful operator/rider copy | `NOT_OBSERVED` |
| Geographic coverage | Approved operating geography and unsupported-area response | `NOT_OBSERVED` |
| Funding and limits | Program payer, spend owner, per-ride/day limits, approval path, dispute/refund owner | `DECISION_PENDING` |
| Privacy/legal | Minimum data terms, retention/deletion, incident contact, and BAA determination if applicable | `DECISION_PENDING` |
| Operations | Support escalation, outage fallback, alert owner, reconciliation queue owner, and hours | `DECISION_PENDING` |
| Launch | SPEC-018 plus pilot/production, real-effect, consent, reporting, and human sign-offs | `BLOCKED` |

## 4. Adapter contract if released

A Lyft adapter must:

1. implement only the released `TransportationPort` capability and remain adapter-local;
2. require a documented human dispatcher action before quote or booking;
3. evaluate consent and construct the released minimum-necessary transportation projection before transmission;
4. exclude ride reason, Check-In answers, Support Signal basis, distress framing, case narrative, diagnosis, and unrelated veteran data;
5. use persistent SUAS `FulfillmentAttempt` identity before every external mutation;
6. use provider idempotency only if official evidence confirms its semantics, without weakening SUAS idempotency;
7. record timeouts and ambiguous create/cancel outcomes as `PROVIDER_UNKNOWN` and reconcile before duplicate-risk retry;
8. normalize provider statuses into SUAS integration-level outcomes without changing Service Request state directly;
9. verify webhook authenticity over the exact raw body, reject replay/duplicates, and preserve polling reconciliation;
10. preserve Manual and Fake transportation adapters and route to a human path on unsupported, degraded, funding-blocked, or ambiguous outcomes;
11. expose normalized health and rate-limit state without credentials or rider data;
12. fail closed outside an explicitly released environment and deployment record.

## 5. Minimum-necessary projection review

The existing released transportation projection is the starting ceiling, not automatic permission to transmit every field. Lyft field mapping must be documented against official API requirements.

| SUAS field | Proposed use | Release requirement |
|---|---|---|
| Rider first and last name | Ride identification | Confirm required format and minimization |
| Rider phone number | Provider/rider coordination | Confirm SMS/voice behavior and consent basis |
| Pickup coordinates/address | Dispatch | Confirm exact required representation |
| Drop-off coordinates/address | Dispatch | Confirm exact required representation |
| Product/ride type | Selected offer | Normalize outside domain state |
| Driver note | Minimum operational instruction only | Prohibit clinical, crisis, eligibility, and case details |
| Internal attempt key | SUAS idempotency/audit | Do not transmit unless official idempotency field permits it |

## 6. Environment and effect gates

Until this packet is accepted in a released manifest:

- no `lyft_concierge` runtime mode is valid;
- no Lyft credential may be configured in LOCAL, TEST, shared STAGING, client bundles, or the current Worker;
- no quote, booking, cancellation, webhook, or rider notification may contact Lyft;
- no live, free, discounted, or owner-funded ride is a harmless test;
- the existing Worker remains `SUAS_TRANSPORTATION_ADAPTER_MODE=fake`;
- `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false`, `REAL_WORLD_EFFECTS=disabled`, `PILOT_LAUNCH=blocked`, and `PRODUCTION_LAUNCH=blocked` remain unchanged.

A later implementation release must add explicit secret names, configuration validation, deployment ownership, callback/webhook ingress, test vectors, and rollback/reconciliation evidence. Credentials alone must never enable the adapter.

## 7. Proposed staged implementation after release

1. **Contract fixture:** adapter-local DTO/status/error fixtures derived from redacted official documentation, with no network calls.
2. **Disabled adapter:** typed configuration and registry entry that fails closed unless all release and environment gates pass.
3. **Synthetic transport tests:** quote/create/status/cancel, rate limit, invalid credential, timeout, ambiguous result, webhook signature/replay, and reconciliation tests using a scripted transport.
4. **Provider test boundary:** official sandbox/test mechanism only, with synthetic rider data and proof of no charge/no real dispatch.
5. **Production preflight:** credential status, program connection, webhook reachability, spend controls, on-call owner, manual fallback, privacy/legal acceptance, and SPEC-018 evidence.
6. **Owner-observed first ride:** separately authorized, tightly bounded, human-dispatched production validation. Never automated from CI.

## 8. Owner decision options

- `ACCEPT_FOR_SPEC_RELEASE`: Lyft Concierge becomes a second D-017 adapter family, subject to every gate above.
- `EVIDENCE_REQUIRED`: keep this packet open while collecting missing provider/API/operational evidence.
- `DEFER`: retain Lyft as a manual Concierge path only.
- `REJECT`: do not integrate Lyft.

**Current recommendation:** `EVIDENCE_REQUIRED`. Business-account approval materially advances feasibility, but public evidence does not establish the API client/program connection, technical contract, safe test boundary, or operational authority required for implementation.

## 9. Public sources observed

- Lyft Business Help, “Concierge API overview”: <https://help.lyft.com/business/hc/en-us/articles/360001599667-Concierge-API-overview>
- Lyft Business Help, “Managing your API client and program connections”: <https://help.lyft.com/business/hc/en-us/articles/8587470351891-Managing-your-API-client-and-program-connections>
- Lyft Business Help, “Lyft Business for Healthcare”: <https://help.lyft.com/business/hc/en-us/articles/360002086147-Lyft-Business-for-Healthcare>

Public marketing/help material is contextual evidence only. Official authenticated API documentation and owner contract records control the implementation mapping.
