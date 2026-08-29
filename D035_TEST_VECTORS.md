# D035_TEST_VECTORS.md — Deterministic Veteran verification vectors

**Status:** proposed / not release-authoritative  
**Decision:** D-035  
**Protocol:** [D035_PROTOCOL.md](D035_PROTOCOL.md)

## 1. Purpose

Provide deterministic implementation and review vectors for D-035. These vectors use synthetic identifiers only. They do not authorize calls to VA production systems.

## 2. Normalization vectors

| Vector | Provider input class | Expected SUAS result |
|---|---|---|
| VV-001 | confirmed Title 38 status | `VERIFIED`, reason `null` |
| VV-002 | `PERSON_NOT_FOUND` | `NOT_CONFIRMED/PERSON_NOT_FOUND` |
| VV-003 | `NOT_TITLE_38` | `NOT_CONFIRMED/NOT_TITLE_38` |
| VV-004 | `MORE_RESEARCH_REQUIRED` | `NOT_CONFIRMED/MORE_RESEARCH_REQUIRED` |
| VV-005 | provider reason `ERROR` | `UNAVAILABLE/ERROR` |
| VV-006 | unknown reason string | `UNAVAILABLE/PROVIDER_REASON_UNKNOWN`; no definitive user claim |
| VV-007 | malformed provider payload | `UNAVAILABLE/PROVIDER_RESPONSE_INVALID` |
| VV-008 | provider timeout before any response | `UNAVAILABLE/PROVIDER_UNAVAILABLE` |
| VV-009 | provider 429 | `UNAVAILABLE/PROVIDER_RATE_LIMITED`; retry policy only |
| VV-010 | OAuth user cancellation | no settled VA result required; fallback remains available |

## 3. OAuth security vectors

### VV-OAUTH-001 — valid bound callback

Given:
- authenticated Veteran `VET-A`;
- SUAS session `SES-A`;
- transaction `TX-A` bound to `VET-A` + `SES-A`;
- valid unconsumed state;
- valid PKCE verifier;
- signed provider token with expected issuer/audience/expiry;

When callback is received,

Then:
- `TX-A` is atomically consumed;
- provider status query may execute;
- exactly one verification settlement is written;
- no token/JWT/raw provider body is written to domain events or ordinary logs.

### VV-OAUTH-002 — state mismatch

Given callback state not matching `TX-A`,

Then:
- callback rejected;
- no token exchange;
- no verification settlement;
- audit reason `STATE_MISMATCH`.

### VV-OAUTH-003 — replay

Given `TX-A` is already consumed,

When the same callback is replayed,

Then:
- reject;
- no second provider mutation/query requiring authorization-code reuse;
- no second verification settlement;
- audit reason `CALLBACK_REPLAY`.

### VV-OAUTH-004 — cross-user substitution

Given transaction for `VET-A`, but callback is handled under authenticated session for `VET-B`,

Then:
- reject before verification settlement;
- audit bounded reason `STATE_MISMATCH` or dedicated cross-user mismatch code;
- no Veteran data crosses between users.

### VV-OAUTH-005 — bad PKCE

Given wrong verifier,

Then token exchange fails closed and no verification settles.

### VV-OAUTH-006 — invalid JWT signature

Given token signature validation fails,

Then:
- no provider identity/status is trusted;
- result is not `VERIFIED`;
- bounded failure `TOKEN_VALIDATION_FAILED`.

### VV-OAUTH-007 — wrong issuer/audience/expired

Each condition independently fails closed with `TOKEN_VALIDATION_FAILED`.

### VV-OAUTH-008 — scope expansion

Given configured/requested scope contains any value outside released allowlist,

Then:
- authorization initiation fails before redirect;
- audit `SCOPE_MISMATCH` or `CONFIGURATION_INVALID`;
- broader scope is never sent.

## 4. API-key confirmation vectors

These vectors apply only if D-035 settles `VaVeteranConfirmationAdapter` as an authorized adapter.

### VV-CONF-001 — minimum projection

Given the released demographic projection allowlist,

When confirmation request is created,

Then only fields in that allowlist are serialized.

### VV-CONF-002 — unapproved optional field

Given provider accepts an optional demographic field not in the SUAS released allowlist,

Then SUAS rejects/omits it before provider call.

### VV-CONF-003 — raw demographic logging

Given a confirmation request,

Then DOB, ZIP, name, SSN-like values, and other matching data do not appear in ordinary logs, traces, metrics, or Audit Event payload bodies.

### VV-CONF-004 — retry after `PERSON_NOT_FOUND`

A corrected retry creates a new attempt preserving prior history. Prior result is not overwritten.

## 5. Enrollment vectors

### VV-ENR-001 — VA verified

`VERIFIED` satisfies the verification branch of enrollment when all other enrollment prerequisites pass.

### VV-ENR-002 — VA declined

User declines/cancels VA authorization and chooses self-attestation. Enrollment can still complete under D-016 fallback.

### VV-ENR-003 — VA unavailable

Provider timeout/error does not block self-attestation or an explicit support request.

### VV-ENR-004 — NOT_TITLE_38

UI and API output MUST NOT say `not a Veteran`, `never served`, or equivalent. Self-attestation/manual fallback remains visible according to released policy.

### VV-ENR-005 — MORE_RESEARCH_REQUIRED

Fallback remains available. SUAS may direct the Veteran to VA for manual review but does not adjudicate the status itself.

## 6. Environment vectors

| Vector | Condition | Expected |
|---|---|---|
| VV-ENV-001 | D-035 not released | VA adapters unavailable; self-attestation only |
| VV-ENV-002 | `DISABLED` | no VA UI and no outbound VA network call |
| VV-ENV-003 | `SANDBOX` | only sandbox endpoint/credentials/test identities |
| VV-ENV-004 | sandbox result displayed | visibly non-production; cannot be promoted as real evidence |
| VV-ENV-005 | production credential in TEST | startup/config validation fails closed |
| VV-ENV-006 | production mode before production gate | startup/adapter activation fails closed |

## 7. Persistence vectors

### VV-DATA-001

Settled verification row contains normalized state, adapter family/version, environment, timestamps, and audit references only.

### VV-DATA-002

The following strings/types MUST be absent from domain verification rows and event payloads:

```text
access_token
refresh_token
client_secret
apikey
ICN
id_token
raw JWT
raw provider response body
```

### VV-DATA-003

Retry/new attempt preserves prior immutable evidence; current projection changes deterministically without deleting history.

## 8. Concurrency/idempotency vectors

### VV-CONC-001

Two simultaneous callbacks for one transaction produce at most one consumed transaction and one settlement.

### VV-CONC-002

Same authorization-start idempotency key + same request returns/reuses one active logical transaction.

### VV-CONC-003

Same key + conflicting request fails with deterministic idempotency conflict before external call.

### VV-CONC-004

Two verification attempts settling out of order do not use insertion order as current-state authority. Current selection rule must be explicit and deterministic.

## 9. Accessibility/UX vectors

- keyboard-only user can select VA verification or self-attestation;
- focus returns predictably after provider callback;
- cancellation/error state announces itself semantically;
- verification status is not color-only;
- `NOT_CONFIRMED` language is understandable without provider jargon;
- no dark pattern makes the optional VA path appear mandatory;
- external redirect is announced before navigation;
- mobile deep-link return preserves accessible context.

## 10. Evidence bundle

A conformant evidence bundle records:

```text
spec commit SHA
adapter implementation SHA
provider docs URL + retrieval date
scope/projection hash
synthetic fixture hash
test command
machine/environment identity
results
redaction scan result
accessibility review artifact
privacy owner decision/reference
```

A passing bundle is evidence for review; it does not itself settle D-035 or production readiness.
