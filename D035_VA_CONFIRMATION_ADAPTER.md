# D035_VA_CONFIRMATION_ADAPTER.md — VA Veteran Confirmation adapter contract

**Status:** proposed / not release-authoritative  
**Decision:** D-035  
**Adapter:** `VaVeteranConfirmationAdapter`  
**Primary contract:** [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md)  
**Protocol:** [D035_PROTOCOL.md](D035_PROTOCOL.md)  
**Decision packet:** [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md)

## 1. Purpose

Pin the concrete provider contract for SUAS integration with the VA Veteran Confirmation API while preserving the provider-neutral `VeteranVerificationPort` boundary.

This file does not close D-035 and does not authorize production operation.

## 2. Provider contract facts

Observed VA contract for Veteran Confirmation API v1:

- purpose: confirm whether an individual has Title 38 Veteran status;
- method: `POST /status`;
- authorization: API key in HTTP header `apikey`;
- request model: identifying demographic attributes used to match a person;
- response model: `confirmed` or `not confirmed`, with a `not_confirmed_reason` when not confirmed;
- v1 removes SSN from the Veteran Confirmation request model and uses demographic/address information instead;
- sandbox uses mock data and the same underlying business logic with a different data store.

Provider-native paths, schemas, and response objects remain adapter-local.

## 3. Version boundary

Canonical provider family for this adapter:

```text
VA Veteran Confirmation API v1
```

Version 0 is not authorized. Any provider version change requires contract review before configuration is advanced.

The adapter MUST expose a bounded internal provider-version identifier, for example:

```text
VA_VETERAN_CONFIRMATION_V1
```

Do not infer compatibility with future VA versions.

## 4. HTTP contract

The adapter performs one provider query per verification attempt:

```text
POST {configured_va_confirmation_base_url}/status
```

Required request characteristics:

```text
Content-Type: application/json
apikey: <server-side secret>
```

Rules:

1. The `apikey` header name is exact.
2. API keys MUST NOT be sent in query strings, request bodies, browser-visible headers, client bundles, logs, traces, metrics, Domain Events, or Audit Event payloads.
3. Base URL is configuration-owned and environment-scoped; user input cannot choose it.
4. HTTPS is mandatory outside a local deterministic fake.
5. Redirect-following to arbitrary hosts is forbidden.
6. Provider response bodies are parsed only after bounded status/content checks.

## 5. Environment configuration

Canonical logical modes:

```text
DISABLED
SANDBOX
PRODUCTION
```

Recommended configuration identifiers:

```text
SUAS_VA_CONFIRMATION_MODE
SUAS_VA_CONFIRMATION_BASE_URL
SUAS_VA_CONFIRMATION_API_KEY        # secret, never committed
SUAS_VA_CONFIRMATION_PROJECTION_ID
```

These names are proposed implementation identifiers, not external API fields.

Environment rules:

- `DISABLED`: no outbound call and no Veteran Confirmation UI action.
- `SANDBOX`: sandbox endpoint + sandbox API key + synthetic/test identities only.
- `PRODUCTION`: impossible until D-035 is released, VA production access is approved, Privacy/Security evidence is accepted, and production is separately re-settled.
- sandbox and production keys MUST be separate credentials.
- environment mismatch fails closed.

## 6. Secret lifecycle

The API key is security infrastructure state.

Required controls:

1. server-side secret store only;
2. environment-scoped secret identity;
3. never stored in domain tables;
4. never returned by admin/config APIs;
5. redacted from exception text and structured logs;
6. rotate without domain migration;
7. revoke/replace on suspected disclosure;
8. startup/adapter-health check may verify presence/shape but MUST NOT print the secret;
9. credential fingerprints, if used operationally, MUST be irreversible and non-secret.

A missing or malformed API key produces `CONFIGURATION_INVALID` / adapter `UNAVAILABLE`; it does not fall through to an unauthenticated provider call.

## 7. Demographic projection gate

The provider accepts demographic attributes for matching, but provider acceptance does not define SUAS authority to collect them.

Canonical SUAS rule:

```text
NO_REQUEST_UNTIL projection_id is released and Privacy Owner approved.
```

The exact production projection remains `DECISION_PENDING`.

The approved projection artifact MUST contain:

```text
projection_id
projection_version
allowed_field_names
required_vs_optional designation
source of each field inside SUAS
purpose = VETERAN_STATUS_VERIFICATION
normalization rules
validation rules
prohibited fields
retention/transience rule
privacy_owner
approval_timestamp
canonical hash
```

D-035 does **not** authorize SSN collection. Version 1 of the provider contract was designed to remove SSN from this API family.

## 8. Input validation and normalization

Before transmission:

- validate only fields present in the released projection;
- reject unexpected fields rather than forwarding them;
- normalize names/address data according to the pinned provider contract;
- preserve the Veteran's source data separately from provider-normalized request material where necessary; provider normalization must not silently rewrite the Veteran profile;
- never enrich the request from unrelated Case, Check-In, Trusted Circle, clinical, benefits, or provider data.

VA release notes document strict name/input formatting behavior. The adapter MUST treat provider validation requirements as adapter-local normalization/validation constraints rather than altering SUAS domain identity semantics.

## 9. Request persistence boundary

By default, do not persist the complete demographic provider request.

Persist only bounded evidence such as:

```text
attempt_id
projection_id
projection_hash
adapter_version
provider_environment
request_started_at
request_finished_at
normalized_result
bounded_reason_code
http_outcome_class
```

If temporary request material must be held for a retry, it MUST have explicit expiry, access control, and deletion semantics governed by D-007/privacy review.

## 10. Response normalization

Provider values normalize as follows:

| Provider result | SUAS result | SUAS reason |
|---|---|---|
| confirmed | `VERIFIED` | null |
| not confirmed + `PERSON_NOT_FOUND` | `NOT_CONFIRMED` | `PERSON_NOT_FOUND` |
| not confirmed + `NOT_TITLE_38` | `NOT_CONFIRMED` | `NOT_TITLE_38` |
| not confirmed + `MORE_RESEARCH_REQUIRED` | `NOT_CONFIRMED` | `MORE_RESEARCH_REQUIRED` |
| not confirmed + `ERROR` | `UNAVAILABLE` | `ERROR` |
| unknown reason / malformed body | `UNAVAILABLE` | provider-response-invalid audit class |

Never map an unknown provider value to a more definitive SUAS state.

`NOT_CONFIRMED` is not `NOT_A_VETERAN`.

## 11. Provider HTTP/failure semantics

Canonical adapter failure classes:

```text
CONFIGURATION_INVALID
AUTHENTICATION_REJECTED
REQUEST_INVALID
PROVIDER_RATE_LIMITED
PROVIDER_UNAVAILABLE
PROVIDER_RESPONSE_INVALID
PROVIDER_REASON_UNKNOWN
TIMEOUT
NETWORK_ERROR
```

Behavior:

- 401/403-like provider authentication failure -> `UNAVAILABLE`, operator-visible credential fault;
- 400-like request validation failure -> no automatic semantic downgrade; record bounded failure and permit correction/retry;
- 429 -> `UNAVAILABLE`, obey provider backoff/retry policy;
- 5xx/network/timeout -> `UNAVAILABLE`, bounded retry only;
- malformed success response -> `UNAVAILABLE`;
- no provider failure can independently block the D-016 fallback or an explicit support request.

Exact retry counts/durations are not invented here; use released resilience constants when available.

## 12. Retry and idempotency

A Veteran Confirmation query is a read-like external operation but still requires attempt identity.

Rules:

1. one SUAS verification attempt has one stable attempt id;
2. safe transport retry may reuse that attempt id if request projection/hash is identical;
3. corrected demographic input creates a new attempt;
4. previous result remains historical evidence;
5. retries MUST NOT create duplicate settled verification rows for one logical attempt;
6. if outcome is unknown after transport failure, retry only according to bounded resilience policy;
7. do not treat the provider API key as an idempotency mechanism.

## 13. Logging and telemetry

Allowed telemetry dimensions:

```text
adapter_family
adapter_version
provider_environment
normalized_status
bounded_failure_class
latency_bucket
projection_id
```

Forbidden telemetry/log content:

```text
apikey
name
DOB
street address
city
state when combinable with identity
ZIP when combinable with identity
email
phone
raw request body
raw response body
provider-generated identifying fields
```

Operational metrics must remain compatible with D-025 privacy/reporting constraints.

## 14. Security tests

Required tests before SANDBOX activation:

1. request contains `apikey` header and never query/body credential;
2. missing key fails before provider call;
3. malformed key/configuration fails closed;
4. arbitrary provider base URL injection rejected;
5. unexpected request field rejected before provider call;
6. only released projection fields transmitted;
7. API key absent from logs/errors/admin reads/test snapshots;
8. demographic values absent from ordinary logs/traces/metrics;
9. sandbox credential cannot be used in production mode;
10. production credential cannot be loaded in LOCAL/TEST/STAGING configuration;
11. malformed/unknown provider reason maps to `UNAVAILABLE`;
12. `NOT_TITLE_38` never renders as proof of no military service.

## 15. Deterministic sandbox vectors

Test fixtures MUST use VA-provided sandbox identities or SUAS-local provider fakes. Real Veteran data is forbidden in LOCAL/TEST/STAGING.

At minimum cover:

```text
CONFIRMED
PERSON_NOT_FOUND
NOT_TITLE_38
MORE_RESEARCH_REQUIRED
ERROR
401/403 equivalent
400 validation failure
429
5xx
network timeout
malformed JSON/schema
unknown not_confirmed_reason
```

Fixture data must be clearly labeled synthetic and cannot be promoted as production verification evidence.

## 16. Production evidence packet

Before `PRODUCTION` mode can be considered, produce:

```text
VA production-access approval reference
provider docs/version/retrieval date
approved projection artifact + hash
Privacy Owner attestation
secret-storage/rotation evidence
sandbox-vs-production isolation evidence
adapter contract test results
PII/log-redaction evidence
negative security tests
normalization vectors
failure/retry evidence
accessibility/copy review
D-035 settlement reference
production gate re-settlement reference
```

Missing evidence means `NOT_READY`.

## 17. Relationship to OAuth adapter

This adapter is not a fallback from a failed OAuth transaction unless deployment policy explicitly permits both adapters and the Veteran is shown/consents to the second data-flow model.

SUAS MUST NOT silently switch from Veteran-mediated OAuth to demographic API-key lookup because OAuth fails.

Each adapter has distinct notice, privacy, credential, and evidence requirements.

## 18. External references

Provider contract consulted: VA Developer, Veteran Confirmation API documentation and release notes, current as of 2026-08-29.

Key externally observed facts:

- API-key authorization uses HTTP header `apikey`;
- status endpoint is `POST /status`;
- v1 removed SSN from this API and uses demographic/address information;
- `not confirmed` reason values include `PERSON_NOT_FOUND`, `NOT_TITLE_38`, `MORE_RESEARCH_REQUIRED`, `ERROR`;
- sandbox uses mock data.

These facts must be revalidated during a future provider-version upgrade or production-access review.
