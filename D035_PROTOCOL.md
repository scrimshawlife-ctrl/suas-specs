# D035_PROTOCOL.md — Veteran verification protocol and state contract

**Status:** proposed / not release-authoritative  
**Decision:** D-035  
**Primary contract:** [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md)  
**Cross-spec reconciliation:** [D035_ASSIMILATION.md](D035_ASSIMILATION.md)

## 1. Purpose

Define the protocol-level behavior required to implement optional VA-backed Veteran-status verification without coupling SUAS domain semantics to a single VA API family.

This document does not close D-035 and does not authorize production operation.

## 2. Adapter families

SUAS owns `VeteranVerificationPort`.

Permitted adapter families after D-035 release:

| Adapter | External model | Default use |
|---|---|---|
| `VaVeteranConfirmationAdapter` | API key + identifying demographic fields | Preferred when status-only confirmation is sufficient and privacy review accepts the demographic projection |
| `VaServiceHistoryEligibilityAdapter` | Veteran-mediated OAuth 2.0/OIDC Authorization Code Grant | Preferred when Veteran-mediated authorization is required or when a later released capability needs another permitted endpoint |
| `SelfAttestationAdapter` | SUAS-owned self-attestation | Required fallback under current D-016 relationship |
| `FixtureVeteranVerificationAdapter` | deterministic synthetic data | LOCAL/TEST only |

The domain result is identical regardless of adapter.

## 3. Selection rule

Selection is policy-driven and configuration-bounded.

```text
if D035 not released:
  use SelfAttestationAdapter only
else if environment == PRODUCTION and production gate not settled:
  VA adapters disabled
else if released deployment policy selects status-only confirmation:
  use VaVeteranConfirmationAdapter
else if released deployment policy selects Veteran-mediated OAuth:
  use VaServiceHistoryEligibilityAdapter
else:
  use SelfAttestationAdapter
```

No runtime heuristic may silently choose a broader VA API because more data is available.

## 4. Verification attempt state machine

Canonical attempt states:

```text
CREATED
  -> AWAITING_USER_ACTION
  -> AUTHORIZING | READY_TO_QUERY
  -> QUERYING
  -> SETTLED

Exceptional terminal states:
  CANCELLED
  EXPIRED
  FAILED_FINAL
```

Provider/result state is separate from attempt state.

Canonical verification result:

```text
PENDING
  -> VERIFIED
  -> NOT_CONFIRMED
  -> UNAVAILABLE
  -> REVOKED
```

`NOT_CONFIRMED` is a provider interpretation result, not proof of non-service.

## 5. OAuth transaction contract

For `VaServiceHistoryEligibilityAdapter`, create a one-time `VeteranVerificationAuthorizationTransaction` containing only:

```text
transaction_id
veteran_id
session_id
provider = VA
adapter_family
state_hash
pkce_verifier_encrypted_or_ephemeral
nonce_hash nullable
redirect_uri_id
requested_scope_set_id
status = CREATED | REDIRECTED | CALLBACK_RECEIVED | CONSUMED | EXPIRED | CANCELLED
created_at
expires_at
consumed_at nullable
```

Rules:

1. `state` MUST be cryptographically unpredictable and single-use.
2. Persist a hash of `state`, not the plaintext value, unless the storage model proves equal or stronger confidentiality.
3. `state` MUST bind the provider callback to the initiating SUAS Veteran and session.
4. PKCE uses `S256` where supported/required; public/native clients MUST NOT hold a client secret.
5. `redirect_uri` MUST be selected from configuration; user input cannot choose an arbitrary callback URI.
6. Callback handling atomically consumes the transaction before settling verification.
7. A callback with missing, expired, mismatched, or already-consumed state fails closed.
8. Provider authorization cancellation is a user-controlled cancellation, not an authentication failure.

## 6. Scope policy

### 6.1 OAuth status-only scope set

Canonical scope set identifier:

```text
VA_STATUS_ONLY_V1 = {
  openid,
  profile,
  veteran_status.read
}
```

For status-only onboarding, configured scopes MUST be a subset of the released allowlist and MUST NOT silently inherit broader provider defaults.

Forbidden absent another released decision:

```text
offline_access
service_history.read
disability_rating.read
disability_rating_summary.read
enrolled_benefits.read
flashes.read
permanent_and_total_disability.read
```

If the provider application registration has broader default scopes, SUAS MUST explicitly request the narrower released subset.

### 6.2 API-key confirmation projection

For `VaVeteranConfirmationAdapter`, the exact demographic request projection is `DECISION_PENDING` until privacy review and VA contract review define the minimum fields SUAS may collect/transmit.

The adapter MUST NOT infer that every provider-accepted optional demographic field is authorized for SUAS collection.

## 7. Provider result normalization

Canonical normalization table:

| Provider fact | SUAS status | reason |
|---|---|---|
| Title 38 status confirmed | `VERIFIED` | null |
| person not found | `NOT_CONFIRMED` | `PERSON_NOT_FOUND` |
| not Title 38 | `NOT_CONFIRMED` | `NOT_TITLE_38` |
| more research required | `NOT_CONFIRMED` | `MORE_RESEARCH_REQUIRED` |
| VA/source-system error | `UNAVAILABLE` | `ERROR` |
| network timeout / 5xx / malformed response | `UNAVAILABLE` | provider-normalized technical code, audit-only |
| user cancels OAuth | no settled VA result required | `USER_CANCELLED` audit fact |

Rules:

1. `NOT_TITLE_38` MUST NOT render as “you are not a Veteran.”
2. `PERSON_NOT_FOUND` MUST offer correction/retry where appropriate.
3. `MORE_RESEARCH_REQUIRED` MAY point to VA for manual review but SUAS does not perform benefit adjudication.
4. `ERROR` is retryable according to resilience policy and MUST NOT become `NOT_CONFIRMED`.
5. Unknown provider reason values fail to `UNAVAILABLE`, never to a more definitive status.

## 8. Idempotency and concurrency

- Starting the same logical authorization with the same idempotency key returns the same active transaction while it remains usable.
- A consumed transaction cannot be replayed.
- Concurrent callbacks for one transaction produce at most one settled verification.
- Concurrent verification attempts MAY exist only if product policy explicitly permits it; settlement must identify which attempt is current without deleting history.
- A retry creates a new attempt identity and preserves the previous outcome.
- Provider retries MUST NOT duplicate domain evidence rows for the same settled attempt.

## 9. Persistence boundary

Persist in domain storage:

```text
verification id
veteran id
method
normalized status
normalized reason
adapter family/version
scope-set id or projection id
provider environment = SANDBOX | PRODUCTION
verified/settled timestamps
source contract version
audit references
```

Do not persist in domain storage:

```text
access token
refresh token
client secret
API key
ICN
raw id_token/JWT
raw provider response
full provider error body
provider cookies/session artifacts
```

If a provider credential/token must be retained transiently, it belongs in security/infrastructure storage with explicit expiry and deletion semantics.

## 10. User-visible result semantics

Canonical semantic messages, not final copy:

| State | Meaning shown to user |
|---|---|
| `VERIFIED` | VA confirmed the configured Veteran-status criterion. |
| `NOT_CONFIRMED/PERSON_NOT_FOUND` | VA could not match the submitted/authorized information to a confirmable record. |
| `NOT_CONFIRMED/NOT_TITLE_38` | VA did not confirm Title 38 Veteran status. This does not state that the person never served. |
| `NOT_CONFIRMED/MORE_RESEARCH_REQUIRED` | VA could not confirm status from the available records and may require review. |
| `UNAVAILABLE` | Verification is temporarily unavailable. |

Exact copy must be versioned and accessibility-reviewed before release.

## 11. Support-access invariant

At every non-`VERIFIED` outcome:

```text
IF explicit support request exists
THEN verification state alone MUST NOT block the request path.
```

Other independently released eligibility/routing policies may still apply, but D-035 itself creates no service-denial rule.

## 12. Observability

Metrics may include bounded operational counters such as:

```text
verification_attempt_started_total
verification_attempt_settled_total{status,adapter_family,environment}
verification_callback_rejected_total{reason_code}
verification_provider_error_total{adapter_family,reason_class}
```

Metrics MUST NOT include names, email, phone, DOB, ZIP, ICN, tokens, raw provider reasons containing PII, or tenant-combinable small-cell dimensions.

D-025 still controls reporting use.

## 13. Failure taxonomy

Canonical failure classes:

```text
USER_CANCELLED
AUTHORIZATION_DENIED
STATE_MISMATCH
STATE_EXPIRED
CALLBACK_REPLAY
PKCE_FAILED
TOKEN_EXCHANGE_FAILED
TOKEN_VALIDATION_FAILED
SCOPE_MISMATCH
PROVIDER_UNAVAILABLE
PROVIDER_RATE_LIMITED
PROVIDER_RESPONSE_INVALID
PROVIDER_REASON_UNKNOWN
CONFIGURATION_INVALID
ENVIRONMENT_MISMATCH
```

Only bounded reason classes enter audit/metrics. Raw provider bodies do not.

## 14. Release evidence

Before SANDBOX activation, evidence must include:

- adapter contract tests;
- scope/projection allowlist proof;
- state/PKCE/callback replay tests where OAuth is used;
- PII/log redaction tests;
- deterministic normalization vectors;
- environment isolation tests;
- self-attestation regression tests;
- accessibility review of the verification choice/failure flow;
- privacy owner review of the data projection;
- evidence hashes and exact provider docs/version/date consulted.

Before PRODUCTION activation, additionally require VA production access approval, D-035 release settlement, applicable D-007/D-013 constraints, accepted STAGING evidence, and explicit production gate re-settlement.
