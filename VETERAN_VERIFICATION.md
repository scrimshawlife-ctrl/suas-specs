# VETERAN_VERIFICATION.md — Veteran status verification

**Status:** proposed / not release-authoritative
**Decision:** D-035
**Related:** [DECISIONS.md](DECISIONS.md), [D035_ASSIMILATION.md](D035_ASSIMILATION.md), [ONBOARDING.md](ONBOARDING.md), [APIS.md](APIS.md), [AUTH.md](AUTH.md), [CONSENT.md](CONSENT.md), [COMPLIANCE.md](COMPLIANCE.md), [DATA_MODEL.md](DATA_MODEL.md), [SECURITY.md](SECURITY.md), [TESTING.md](TESTING.md)

## 1. Purpose

Define an optional, consent-bound capability for verifying Veteran status during onboarding without making federal verification a prerequisite for receiving urgent SUAS support.

This specification is additive. Until D-035 is released, D-016 remains authoritative: self-attestation plus working passwordless contact is sufficient for the current pilot.

[D035_ASSIMILATION.md](D035_ASSIMILATION.md) is the normative cross-spec reconciliation package for this proposed decision. It defines how ONBOARDING, APIS, AUTH, CONSENT, DATA_MODEL, SECURITY, COMPLIANCE/PRIVACY, TESTING, ENVIRONMENT/DEPLOYMENT, MOBILE_SURFACE, EVENT_MODEL, reporting, and release settlement must interpret D-035 when it is released. It does not itself close D-035 or rewrite released history.

## 2. Provider boundary

SUAS owns a `VeteranVerificationPort`. VA products are adapter-local implementations.

Initial VA adapter family: VA Veteran Service History and Eligibility API, using Veteran-mediated OAuth 2.0 / OpenID Connect Authorization Code Grant. For status-only verification, implementations SHOULD prefer the narrower VA Veteran Confirmation API when it satisfies the same SUAS contract, because VA recommends that API when only Title 38 status is needed.

Provider SDK types, ICNs, access tokens, refresh tokens, launch context, raw VA payloads, and VA endpoint-specific status objects MUST NOT become SUAS domain types.

## 3. Onboarding flow

```text
PASSWORDLESS_AUTH
  -> PILOT_CONSENT
  -> VETERAN_VERIFICATION
       -> VA_STATUS (preferred when configured and consented)
       -> SELF_ATTESTATION (fallback)
       -> MANUAL_REVIEW (optional operational path)
  -> ENROLLMENT_COMPLETE
  -> FIRST_CHECK_IN
```

Rules:

1. VA verification is optional until a later released decision explicitly makes it mandatory.
2. Declining VA authorization MUST NOT prevent the veteran from using the self-attestation path.
3. VA outage, timeout, OAuth failure, ambiguous match, or `not confirmed` result MUST NOT independently deny crisis/safety support or an explicit request for assistance.
4. SUAS MUST NOT describe `NOT_TITLE_38`, `PERSON_NOT_FOUND`, or `MORE_RESEARCH_REQUIRED` as proof that the person never served.
5. Verification is identity/provenance support. It is not eligibility adjudication for VA benefits and does not create a VA partnership claim.

## 4. Minimum authorization

For onboarding status verification, request the minimum scopes necessary:

- `openid`
- `profile`
- `veteran_status.read`

Do not request `service_history.read`, disability-rating scopes, benefits scopes, flashes, permanent-and-total disability, or `offline_access` merely to prove Veteran status.

Any later request for additional VA scopes requires a separate released SUAS capability/decision, explicit Veteran consent, and a documented minimum-necessary purpose.

## 5. Canonical domain contract

```text
VeteranVerification {
  id
  veteran_id
  method: VA_VETERAN_STATUS | SELF_ATTESTATION | MANUAL_REVIEW
  status: VERIFIED | NOT_CONFIRMED | PENDING | UNAVAILABLE | REVOKED
  source: VA | SUAS
  source_contract_version
  verified_at?
  not_confirmed_reason?: PERSON_NOT_FOUND | NOT_TITLE_38 | MORE_RESEARCH_REQUIRED | ERROR
  consent_grant_id?
  audit_event_id
}
```

The default persistence posture is normalized evidence only. Do not persist the complete VA response unless a later released requirement identifies a necessary field and retention basis.

## 6. VA result normalization

| Provider result | SUAS result | Required behavior |
|---|---|---|
| Title 38 confirmed | `VERIFIED` | Record normalized verification evidence and provenance. |
| `PERSON_NOT_FOUND` | `NOT_CONFIRMED` | Offer retry/correction and self-attestation/manual fallback. |
| `NOT_TITLE_38` | `NOT_CONFIRMED` | State only that VA did not confirm Title 38 status. Do not infer no military service. |
| `MORE_RESEARCH_REQUIRED` | `NOT_CONFIRMED` | Offer fallback; optionally direct user to VA review outside SUAS. |
| provider/source error | `UNAVAILABLE` | Preserve onboarding fallback; no denial solely from provider failure. |
| OAuth declined/cancelled | no VA verification record required | Continue with self-attestation if the Veteran chooses. |

## 7. OAuth and security

The VA adapter MUST:

- use Authorization Code Grant for Veteran-mediated access;
- use PKCE where the client cannot securely hold a client secret, including native mobile clients;
- use and validate `state`;
- use `nonce` when OpenID Connect semantics require it;
- validate JWT signatures and issuer/audience/expiry claims;
- bind callback state to the initiating authenticated SUAS session;
- reject callback replay and cross-user token substitution;
- keep client secrets and bearer/refresh tokens out of browser-visible state, logs, analytics, domain events, and resource rows;
- encrypt retained provider credentials/tokens at rest if retention is necessary;
- avoid requesting `offline_access` for one-time onboarding verification unless a later contract requires background re-verification.

## 8. Consent and privacy

VA authorization is separate from Pilot consent and separate from Trusted Circle disclosure grants.

Before redirecting to VA, SUAS must explain:

- that the user is leaving SUAS to authenticate with VA;
- the specific purpose: Veteran-status verification;
- the scopes/data requested;
- that declining does not block the self-attestation fallback under the current pilot contract;
- that SUAS does not determine VA benefit eligibility from this result.

D-007 retention/deletion remains unresolved. Production persistence beyond minimum normalized evidence remains blocked until the applicable retention basis is settled.

## 9. Product API surface

Proposed SUAS-owned surface:

| Method / path | Effect |
|---|---|
| `POST /veterans/me/verification/va/authorize` | Create a bound OAuth authorization transaction and return/redirect to the configured VA authorization URL. |
| `GET /auth/va/callback` | Validate callback, exchange code, normalize status, write audit evidence. |
| `GET /veterans/me/verification` | Read the authenticated Veteran's normalized verification state. |
| `POST /veterans/me/verification/commands/self-attest` | Record self-attestation fallback. |
| `POST /veterans/me/verification/commands/retry` | Start a new permitted verification attempt. |

Exact API shapes remain subordinate to [API.md](API.md) conventions and must not expose VA-native payloads.

## 10. Capability and environment states

`VETERAN_VERIFICATION` adapter state:

- `DISABLED` — default; no VA authorization UI or outbound call.
- `SANDBOX` — VA sandbox/test identities only; never represent sandbox verification as real-world verification.
- `PRODUCTION` — blocked until D-035 is released, production VA access is approved/configured, security/privacy evidence is accepted, and the SUAS production gate is re-settled.

Self-attestation remains available regardless of VA adapter state unless a later released decision explicitly changes D-016.

## 11. Test evidence

Required before enabling the adapter outside local fixtures:

1. authorization URL contains only approved minimum scopes;
2. state/PKCE/nonce validation and callback session binding;
3. invalid/replayed callback rejection;
4. JWT signature/issuer/audience/expiry rejection tests;
5. confirmed status normalization;
6. all documented not-confirmed reasons normalize without overclaiming;
7. VA timeout/5xx degrades to fallback without blocking explicit support requests;
8. OAuth decline/cancel path remains usable;
9. raw tokens, ICNs, and VA payloads absent from application logs/audit payloads;
10. cross-user and cross-tenant negative tests;
11. sandbox/test data is visibly non-production and cannot be promoted as real verification evidence.

## 12. Release gate

This document does not close D-035 by itself.

A release settlement must record the owner decision, exact authorized adapter/API family, minimum scopes, environment boundary, privacy/retention constraints, evidence references, and whether D-016 is superseded or remains the fallback contract.
