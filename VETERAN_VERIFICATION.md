# VETERAN_VERIFICATION.md — Veteran status verification

**Status:** proposed / not release-authoritative  
**Decision:** D-035  
**Related:** [DECISIONS.md](DECISIONS.md), [D035_ASSIMILATION.md](D035_ASSIMILATION.md), [D035_PROTOCOL.md](D035_PROTOCOL.md), [D035_TEST_VECTORS.md](D035_TEST_VECTORS.md), [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md), [ONBOARDING.md](ONBOARDING.md), [APIS.md](APIS.md), [AUTH.md](AUTH.md), [CONSENT.md](CONSENT.md), [COMPLIANCE.md](COMPLIANCE.md), [DATA_MODEL.md](DATA_MODEL.md), [SECURITY.md](SECURITY.md), [TESTING.md](TESTING.md)

## 1. Purpose

Define an optional, consent-bound capability for verifying Veteran status during onboarding without making federal verification a prerequisite for receiving urgent SUAS support.

This specification is additive. Until D-035 is explicitly settled and released, D-016 remains authoritative: self-attestation plus a working passwordless contact is sufficient for the current pilot.

D-035 is a provenance/verification capability. It is not benefit adjudication, clinical identity, emergency dispatch, a VA partnership claim, or authority to collect broad military records.

## 2. Canonical invariants

1. SUAS owns `VeteranVerificationPort`; VA schemas never become domain schemas.
2. VA verification is optional unless a later released decision explicitly makes stronger proofing mandatory.
3. D-016 self-attestation remains the fallback under this proposal.
4. `NOT_CONFIRMED` is never equivalent to `NOT_A_VETERAN` or `NEVER_SERVED`.
5. A verification outcome alone cannot deny an explicit support request.
6. Status-only verification cannot be used to justify service-history, disability, benefits, health, claims, or clinical data access.
7. Provider credentials, access tokens, refresh tokens, ICNs, raw JWTs, and full VA payloads do not enter domain rows/events/logs.
8. Production use remains blocked until D-035 and the applicable production gates are separately settled.

## 3. Provider boundary and supported families

SUAS owns a provider-neutral `VeteranVerificationPort`.

Candidate VA adapter families:

| Adapter family | VA interaction | Key privacy characteristic |
|---|---|---|
| `VaVeteranConfirmationAdapter` | status-only Veteran Confirmation API; API key; demographic matching request | narrow response, but SUAS must collect/transmit an approved demographic projection |
| `VaServiceHistoryEligibilityAdapter` | Veteran Service History and Eligibility API; OAuth 2.0/OIDC Authorization Code Grant for Veteran-mediated access | Veteran directly authorizes access; status scope can be constrained, but OAuth/token handling is introduced |

Additional SUAS adapters:

- `SelfAttestationAdapter` — required fallback while D-016 remains applicable;
- `FixtureVeteranVerificationAdapter` — deterministic synthetic LOCAL/TEST evidence only.

### 3.1 Selection principle

Do **not** equate “narrower endpoint” with “more private.”

Adapter selection MUST minimize the **total SUAS data flow**, considering:

- PII SUAS must collect;
- PII SUAS must transmit;
- credentials/tokens SUAS must protect;
- persistence requirements;
- user agency/consent;
- provider production-access feasibility;
- onboarding friction;
- security and accessibility complexity.

The initial production adapter family is therefore an explicit D-035 owner choice, not an implementation heuristic. See [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md).

## 4. Onboarding flow

```text
PASSWORDLESS_AUTH
  -> PILOT_CONSENT
  -> VETERAN_VERIFICATION_CHOICE
       -> VA_VERIFICATION      when configured + Veteran chooses/authorizes
       -> SELF_ATTESTATION     fallback/decline/unavailable/inconclusive
       -> MANUAL_REVIEW        optional operational path if separately staffed
  -> ENROLLMENT_COMPLETE
  -> FIRST_CHECK_IN
```

Rules:

1. Declining VA verification MUST NOT prevent the Veteran from selecting self-attestation under the current policy.
2. VA outage, timeout, OAuth failure, matching failure, or `NOT_CONFIRMED` result MUST NOT independently deny crisis/safety support or an explicit support request.
3. Verification choice must be explicit; no hidden automatic VA lookup during onboarding.
4. The user must know before external navigation or transmission that VA will be contacted and for what purpose.
5. Sandbox verification must be visibly non-production and never represented as real Veteran verification.

## 5. Canonical domain contract

```text
VeteranVerification {
  id
  veteran_id
  attempt_id
  method: VA_VETERAN_STATUS | SELF_ATTESTATION | MANUAL_REVIEW
  status: VERIFIED | NOT_CONFIRMED | PENDING | UNAVAILABLE | REVOKED
  source: VA | SUAS
  adapter_family
  adapter_version
  provider_environment: SANDBOX | PRODUCTION | NONE
  source_contract_version
  scope_set_id_or_projection_id?
  verified_at?
  settled_at?
  not_confirmed_reason?: PERSON_NOT_FOUND | NOT_TITLE_38 | MORE_RESEARCH_REQUIRED | ERROR
  authorization_reference?
  audit_event_id
}
```

Historical attempts are preserved. A current projection must use an explicit deterministic selection rule and never rely on insertion order alone.

## 6. Result semantics

| Provider result | SUAS result | Required behavior |
|---|---|---|
| Title 38 confirmed | `VERIFIED` | Record bounded normalized evidence/provenance. |
| `PERSON_NOT_FOUND` | `NOT_CONFIRMED` | Offer correction/retry and permitted fallback. |
| `NOT_TITLE_38` | `NOT_CONFIRMED` | State only that VA did not confirm Title 38 status. Never infer no service. |
| `MORE_RESEARCH_REQUIRED` | `NOT_CONFIRMED` | Offer fallback; optionally direct Veteran to VA review outside SUAS. |
| provider/source `ERROR` | `UNAVAILABLE` | Preserve fallback; retry only under resilience policy. |
| unknown/malformed provider reason | `UNAVAILABLE` | Fail to less certainty, never more certainty. |
| OAuth declined/cancelled | no settled VA result required | Preserve self-attestation path. |

## 7. OAuth status-only contract

Applies when `VaServiceHistoryEligibilityAdapter` is selected.

Canonical minimum requested scope set:

```text
VA_STATUS_ONLY_V1 = {
  openid,
  profile,
  veteran_status.read
}
```

Forbidden for status-only onboarding absent another released decision:

```text
offline_access
service_history.read
disability_rating.read
disability_rating_summary.read
enrolled_benefits.read
flashes.read
permanent_and_total_disability.read
```

Rules:

- Authorization Code Grant for Veteran-mediated access;
- PKCE `S256` for public/native clients and wherever the selected VA client contract requires/supports it;
- unpredictable one-time `state`, bound to the initiating authenticated SUAS Veteran/session;
- `nonce` where required by the OIDC flow/client design;
- exact configured redirect URI;
- JWT signature, issuer, audience, and expiry validation;
- callback replay and cross-user substitution rejected;
- provider tokens excluded from browser-visible state, analytics, domain events, and ordinary logs;
- no background refresh/re-verification and no `offline_access` under the initial status-only proposal.

Detailed transaction semantics are in [D035_PROTOCOL.md](D035_PROTOCOL.md).

## 8. API-key confirmation contract

Applies only if `VaVeteranConfirmationAdapter` is explicitly selected.

The Veteran Confirmation API uses an API key and identifying demographic request data. Therefore the exact SUAS demographic projection is **not implied by provider schema**.

Before this adapter can leave fixture-only design status, the Privacy Owner must approve and hash an exact projection containing only fields SUAS is permitted to collect/transmit for matching.

Rules:

1. Provider-optional fields are not automatically SUAS-authorized fields.
2. SSN collection is not authorized by D-035 unless explicitly added by a later owner decision.
3. Demographic matching fields must not appear in ordinary logs/traces/metrics.
4. Corrected retries create new attempts and preserve prior outcomes.
5. API key remains server-side secret material and is environment-scoped.

## 9. Consent and notice

VA verification authorization/notice is separate from:

- Pilot participation consent;
- Trusted Circle grants;
- provider-fulfillment disclosure consent;
- notification preferences.

Before VA interaction, SUAS must present and version a notice stating at minimum:

- the purpose is Veteran-status verification;
- which adapter/data-flow pattern is being used;
- what data/scopes will be transmitted/requested;
- whether the user will leave SUAS to authenticate with VA;
- that declining does not remove the D-016 self-attestation fallback under the current policy;
- that SUAS does not determine VA benefit eligibility from the result;
- that `NOT_CONFIRMED` does not necessarily mean the person never served.

No dark pattern may make the optional VA path appear mandatory.

## 10. Persistence and retention

Default persistence posture is normalized verification evidence only.

Persist:

- normalized status/reason;
- adapter family/version;
- provider environment;
- scope-set/projection identifier;
- timestamps;
- bounded audit references.

Do not persist in domain storage:

- access/refresh tokens;
- API keys/client secrets;
- ICNs;
- raw ID/access JWTs;
- complete VA request/response bodies;
- full provider errors containing Veteran data.

D-007 remains unresolved. D-035 MUST NOT invent retention durations. Any transient provider credential/token storage requires explicit expiry/revocation/deletion behavior.

## 11. Product API surface

Proposed SUAS-owned surface, subordinate to [API.md](API.md):

| Method / path | Effect |
|---|---|
| `GET /veterans/me/verification` | Read normalized current/history view permitted by the product contract. |
| `POST /veterans/me/verification/commands/self-attest` | Record D-016 fallback. |
| `POST /veterans/me/verification/commands/retry` | Create a new permitted verification attempt. |
| `POST /veterans/me/verification/va/authorize` | Start bound OAuth transaction when OAuth adapter selected. |
| `GET /auth/va/callback` | Provider callback endpoint; validates/consumes transaction and settles bounded evidence. |
| `POST /veterans/me/verification/va/confirm` | Optional SUAS-owned command if API-key confirmation adapter is selected; exact request shape depends on released demographic projection. |

Provider-native VA paths are adapter-local and never Plane A contracts.

## 12. Capability/environment states

Canonical state:

```text
DISABLED
SANDBOX
PRODUCTION
```

- `DISABLED`: default; no VA UI/outbound call.
- `SANDBOX`: VA sandbox/test data only; cannot create real verification evidence.
- `PRODUCTION`: impossible until D-035 is released, selected VA production access is approved/configured, required evidence is accepted, and SUAS production is explicitly re-settled.

LOCAL may use deterministic fixtures without network access.

## 13. Security invariants

Threats/control details are normative in [D035_PROTOCOL.md](D035_PROTOCOL.md) and [D035_ASSIMILATION.md](D035_ASSIMILATION.md).

Minimum invariants:

- no arbitrary provider endpoint/redirect URI;
- no credential/token/client-secret leakage;
- no callback replay;
- no cross-user/cross-tenant binding;
- no scope/projection expansion outside released allowlist;
- no raw VA payload logging;
- environment credentials/endpoints strictly separated;
- unexpected provider result fails toward `UNAVAILABLE`, not toward certainty;
- sandbox evidence cannot be promoted to production evidence.

## 14. Concurrency and idempotency

- authorization-start commands use persistent idempotency where network/client retries could duplicate transactions;
- one OAuth transaction is consumed at most once;
- concurrent callbacks settle at most one result for the transaction;
- retry creates a new attempt identity;
- prior attempts are not mutated into new meanings;
- current verification projection is deterministic over durable attempt history.

## 15. Accessibility and friction

The flow must demonstrate WCAG 2.2 AA target behavior consistent with SUAS:

- keyboard/focus access to both VA and self-attestation choices;
- external redirect announced;
- callback return restores understandable context;
- cancellation/error announced semantically;
- status not conveyed by color only;
- `NOT_CONFIRMED` copy avoids provider jargon and unsupported conclusions;
- no repeated authorization loop traps the user;
- explicit support remains reachable when verification fails.

## 16. Reporting boundary

Verification status/provenance is not automatically an operational reporting dimension.

Until D-025 provides authority, D-035 data MUST NOT create:

- row-level reporting exports;
- small-cell Veteran verification segments;
- cross-tenant status comparisons;
- outcome claims based on verification status.

## 17. Test evidence

[D035_TEST_VECTORS.md](D035_TEST_VECTORS.md) is the canonical deterministic vector set for the proposal.

Before SANDBOX adapter activation, evidence must include:

- adapter isolation/normalization tests;
- exact scope/projection allowlist and hash;
- OAuth state/PKCE/token/callback tests if OAuth selected;
- demographic projection/privacy tests if API-key confirmation selected;
- PII/log-redaction scan;
- cross-user/cross-tenant negative tests;
- environment separation tests;
- self-attestation regression;
- accessibility review;
- Privacy Owner approval of the data flow.

## 18. Decision dependencies

- **D-016:** remains sufficient fallback; D-035 adds optional higher-confidence provenance.
- **D-007:** retention durations remain open; minimize storage and do not invent durations.
- **D-013:** counsel/compliance review remains independently required for production/pilot operations where applicable.
- **D-025:** reporting remains independently gated.
- **D-034:** native local-data protection remains independently gated.

## 19. Owner settlement

The owner must explicitly settle:

- whether the capability is accepted;
- which initial adapter/data-flow family is authorized;
- exact OAuth scopes **or** exact demographic projection;
- environment authority;
- fallback policy;
- one-time vs background re-verification;
- privacy/retention constraints;
- evidence references/hashes;
- relationship to D-016;
- production authority (normally separately blocked).

Use [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md).

## 20. Non-goals

D-035 does not authorize:

- VA health records;
- disability ratings;
- enrolled-benefit records;
- claims/benefit adjudication;
- service-history collection for status-only onboarding;
- DD-214 upload;
- clinical FHIR integration;
- background surveillance/re-verification;
- `offline_access` under the initial status-only proposal;
- removal of self-attestation fallback;
- service denial solely from verification outcome;
- VA affiliation/endorsement claims;
- production activation without explicit gate settlement.
