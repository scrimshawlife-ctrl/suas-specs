# D035_ASSIMILATION.md — Veteran verification cross-spec assimilation

**Status:** proposed / not release-authoritative  
**Decision:** D-035  
**Primary contract:** [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md)  
**Current released fallback:** D-016 self-attestation  

## 1. Purpose

This file reconciles D-035 Veteran verification with the released SUAS specification set without silently rewriting released v0.1–v0.3 history.

Until D-035 is explicitly settled and released, D-016 remains authoritative: Veteran enrollment may use self-attestation plus a working passwordless contact channel and MUST NOT require VA verification, DD-214 upload, or in-person proofing.

When D-035 is released, the clauses in this file become the required cross-spec interpretation. Any older sentence that categorically forbids all VA Veteran-status verification is superseded only to the extent stated here. No other VA health, benefits, disability, clinical, or identity capability is implicitly enabled.

---

## 2. Canonical capability boundary

Add the provider-neutral capability:

```text
VETERAN_VERIFICATION
  port: VeteranVerificationPort
  implementations:
    - VaVeteranConfirmationAdapter
    - VaServiceHistoryEligibilityAdapter
    - SelfAttestationAdapter
    - FixtureVeteranVerificationAdapter
```

Rules:

1. SUAS domain code depends on `VeteranVerificationPort`, never VA SDK or payload types.
2. For status-only onboarding, the narrowest VA API that satisfies the released contract SHOULD be used.
3. The broader VA Veteran Service History and Eligibility API may implement the same port, but broader service-history, disability, benefits, flashes, or permanent-and-total data MUST NOT be fetched merely to verify Veteran status.
4. VA OAuth is verification federation, not SUAS authentication. SUAS passwordless authentication remains authoritative for SUAS sessions.
5. Self-attestation remains a first-class fallback unless a later released decision explicitly removes it.
6. Verification result alone does not authorize disclosure, service denial, benefit adjudication, diagnosis, or emergency dispatch.

---

## 3. ONBOARDING.md assimilation

### 3.1 Veteran flow

Interpret `ONBOARDING.md` §7.1 as:

```text
PASSWORDLESS_AUTH
  -> PILOT_CONSENT
  -> VETERAN_VERIFICATION
       -> VA_STATUS          when configured + Veteran authorizes
       -> SELF_ATTESTATION   fallback / decline / unavailable / inconclusive
       -> MANUAL_REVIEW      optional operational path
  -> ENROLLMENT_COMPLETE
  -> FIRST_CHECK_IN
```

The released D-016 sentence "No VA identity API" is narrowed as follows after D-035 release:

- no VA API is **required** to enroll;
- an approved VA Veteran-status verification adapter MAY be offered;
- declining, failing, or receiving an inconclusive VA result MUST NOT remove the D-016 fallback;
- no DD-214 upload or in-person proofing is introduced;
- SUAS MUST NOT imply VA partnership or benefit eligibility adjudication.

### 3.2 Enrollment command

`POST /veterans/me/commands/complete-enrollment` may complete when the released enrollment policy is satisfied by either:

- a valid `VERIFIED` VeteranVerification; or
- the permitted D-016 `SELF_ATTESTATION` fallback.

VA verification MUST NOT become an undocumented hard prerequisite.

### 3.3 UX rules

The Veteran-facing verification surface MUST:

- explain the purpose before redirect;
- identify that authentication/authorization occurs with VA;
- state what data/scopes are requested;
- provide a visible self-attestation fallback under the current policy;
- distinguish `NOT_CONFIRMED` from "not a Veteran";
- preserve an explicit support-request path when VA is unavailable.

---

## 4. APIS.md assimilation

### 4.1 Plane A additions

Add SUAS-owned endpoints, subordinate to [API.md](API.md) conventions:

| Method / path | Purpose |
|---|---|
| `POST /veterans/me/verification/va/authorize` | Start a session-bound VA authorization transaction. |
| `GET /auth/va/callback` | Validate callback, exchange authorization code, normalize result, persist bounded evidence. |
| `GET /veterans/me/verification` | Read the authenticated Veteran's normalized verification state. |
| `POST /veterans/me/verification/commands/self-attest` | Record permitted self-attestation fallback. |
| `POST /veterans/me/verification/commands/retry` | Begin a new allowed verification attempt. |

Provider-native VA paths are adapter-local and are not Plane A product contracts.

### 4.2 Plane B addition

Add:

| Capability ID | Need | Decision | Notes |
|---|---|---|---|
| `VETERAN_VERIFICATION` | Optional Veteran-status provenance during onboarding | D-035 | Disabled by default; VA adapter only after D-035 release/environment gate; self-attestation fallback remains. |

### 4.3 Forbidden-client reconciliation

The existing `APIS.md` §3.4 prohibition on "VA benefits/health/identity APIs" remains in force except for the exact D-035 Veteran-status verification capability.

After D-035 release, interpret it as:

> Do not add VA benefits, health, clinical, disability, broad identity, or service-history clients except the minimum Veteran-status verification adapter explicitly authorized by D-035 and VETERAN_VERIFICATION.md.

D-035 MUST NOT be used as authority to add VA health records, disability ratings, benefit enrollment, clinical FHIR, claims, or unrelated service-history collection.

### 4.4 Port isolation examples

Add `VeteranVerificationPort` to the capability-port examples. Adapter replacement MUST require no domain-state rewrite.

---

## 5. AUTH.md assimilation

SUAS authentication remains passwordless under the existing AUTH contract.

VA OAuth/OIDC:

- does not create a SUAS session by itself;
- does not replace magic-link/email/phone authentication;
- MUST begin from or bind to the authenticated Veteran's SUAS session;
- MUST bind `state` to the initiating SUAS user/session;
- MUST reject callback replay and cross-user substitution;
- MUST use PKCE for public/native clients where a client secret cannot be held safely;
- MUST validate issuer, audience, expiry, and signature of relevant signed tokens;
- MUST keep provider credentials/tokens out of client-visible configuration, domain events, analytics, and ordinary logs.

The AUTH test statement "enrollment does not require VA API" remains true. D-035 makes VA verification optional, not required.

---

## 6. CONSENT.md assimilation

VA authorization is distinct from:

- Pilot participation consent;
- Trusted Circle grants;
- service-provider disclosure grants;
- notification preferences.

Before redirecting to VA, SUAS MUST record or otherwise durably bind the Veteran's explicit initiation to:

- purpose: `VETERAN_STATUS_VERIFICATION`;
- requested data/scope set;
- consent/notice template version;
- initiating Veteran and session;
- timestamp.

Minimum onboarding scope set:

```text
openid
profile
veteran_status.read
```

`offline_access`, service history, disability, benefit, flashes, permanent-and-total, or other scopes are forbidden for status-only onboarding unless separately released.

Revocation or expiry of provider authorization stops future VA calls. Historical normalized verification/audit evidence is handled under D-007 and the applicable retention contract; provider authorization revocation does not silently erase immutable audit history.

The closed third-party disclosure permission/scope table in CONSENT.md is not automatically expanded by D-035. If implementation requires a first-class ConsentGrant vocabulary change rather than an authorization transaction/notice record, that vocabulary change requires its own released schema update.

---

## 7. DATA_MODEL.md assimilation

Add logical entity:

### veteran_verifications

```text
veteran_verification_id
veteran_id
method = VA_VETERAN_STATUS | SELF_ATTESTATION | MANUAL_REVIEW
status = VERIFIED | NOT_CONFIRMED | PENDING | UNAVAILABLE | REVOKED
source = VA | SUAS
source_contract_version
verified_at nullable
not_confirmed_reason nullable = PERSON_NOT_FOUND | NOT_TITLE_38 | MORE_RESEARCH_REQUIRED | ERROR
consent_or_authorization_reference nullable
audit_event_id
created_at
updated_at
```

Rules:

1. Store normalized evidence, not complete provider payloads.
2. Do not persist access token, refresh token, ICN, raw JWT, or provider response body in this domain row.
3. If provider-token retention is necessary, token storage is infrastructure/security state and MUST be encrypted, access-controlled, environment-scoped, and separately deletable/revocable.
4. A new attempt does not rewrite historical verification evidence silently.
5. `NOT_CONFIRMED` is not equivalent to `NOT_A_VETERAN`.
6. Verification state is scoped to the Veteran identity and cannot be copied across users or tenants.
7. Sandbox verification evidence MUST be distinguishable from production evidence and MUST NOT be promoted as real verification.

Add required access paths for Veteran + current verification state and authorization-transaction replay protection.

---

## 8. SECURITY.md assimilation

Add threat/control requirements:

| Threat | Required control |
|---|---|
| OAuth login CSRF / callback mix-up | unpredictable `state`, bound to initiating authenticated SUAS session, one-time consumption |
| Authorization-code interception | PKCE where applicable; exact redirect URI; code single-use |
| OIDC token forgery | signature + issuer + audience + expiry validation |
| Cross-user token substitution | bind provider transaction/token/result to initiating SUAS user; reject mismatch |
| Callback replay | transaction nonce/state consumed atomically; replay fails closed |
| Scope expansion | allowlist released scopes; reject unexpected configured scope expansion |
| Provider-token leakage | secret storage/encryption/redaction/no domain-event or browser exposure |
| Raw VA payload leakage | normalized projection only; no body logging/tracing |
| Sandbox/prod confusion | environment-scoped credentials/endpoints and explicit evidence provenance |
| Verification overclaim | map provider results only to released normalized states; no "never served" inference |

Production credentials and endpoints MUST be separately configured from sandbox. Missing/invalid configuration fails closed to `DISABLED`/`UNAVAILABLE`, while the permitted self-attestation/support fallback remains available.

---

## 9. COMPLIANCE.md / PRIVACY.md assimilation

Treat VA-derived Veteran verification data as sensitive identity/provenance data regardless of unresolved HIPAA classification.

Required posture:

- purpose limitation: Veteran-status verification only;
- minimum necessary collection;
- no silent secondary use for scoring, diagnosis, marketing, reporting, benefit eligibility, or provider ranking;
- no raw VA payload retention by default;
- D-007 governs retention/deletion duration and remains unresolved;
- D-025 reporting policy does not gain access to row-level Veteran verification data;
- production enablement requires the applicable privacy/counsel/security review evidence;
- authorization/token material MUST be excluded from exports unless a released legal/product requirement explicitly requires it.

D-035 does not establish HIPAA applicability, VA partnership status, federal contractor status, or any compliance certification.

---

## 10. TESTING.md assimilation

Add a Veteran-verification suite before any non-local adapter enablement.

Required deterministic cases:

1. disabled adapter performs no outbound VA call;
2. authorization request contains exactly the released minimum scope set;
3. `state` is unpredictable, session-bound, one-time, and rejects mismatch/replay;
4. PKCE verifier/challenge path rejects missing or incorrect verifier where applicable;
5. signed token validation rejects bad signature, issuer, audience, and expiry;
6. callback cannot bind another Veteran's provider transaction;
7. confirmed status -> `VERIFIED`;
8. `PERSON_NOT_FOUND` -> `NOT_CONFIRMED`;
9. `NOT_TITLE_38` -> `NOT_CONFIRMED`, never "never served";
10. `MORE_RESEARCH_REQUIRED` -> `NOT_CONFIRMED`;
11. provider/source error -> `UNAVAILABLE`;
12. OAuth cancel/decline leaves self-attestation available;
13. timeout/5xx leaves explicit support path available;
14. raw tokens, ICNs, JWTs, and VA response bodies are absent from logs/events/analytics fixtures;
15. sandbox evidence cannot be represented or promoted as production verification;
16. cross-user and cross-tenant negative tests pass;
17. status-only adapter requests no broader VA scopes;
18. D-016 regression: enrollment can still complete through the allowed self-attestation path while D-035 fallback remains released.

Readiness mapping:

- OAuth/session binding -> **AUTH**
- authorization/minimization -> **CONSENT** + **PRIVACY**
- adapter isolation/result normalization -> **AUTH** + **PRIVACY**
- environment/configuration/runbook -> **OPERATIONS**
- cross-user/cross-tenant negative tests -> **AUTH** + **PRIVACY**

Passing these tests does not by itself make D-035 production-ready; STATUS.md must record accepted evidence and the global production gate must be re-settled.

---

## 11. ENVIRONMENT / DEPLOYMENT assimilation

Canonical adapter modes:

```text
DISABLED
SANDBOX
PRODUCTION
```

Rules:

- default is `DISABLED`;
- LOCAL may use deterministic fakes without VA network access;
- TEST/STAGING may use VA sandbox only after D-035 implementation authority exists;
- sandbox identities/data remain non-production fixtures;
- PRODUCTION mode is impossible until D-035 is released, VA production access is approved/configured, required security/privacy evidence is accepted, and SUAS production is explicitly re-settled;
- environment mismatch fails closed;
- no production VA credential is valid in LOCAL/TEST/STAGING configuration.

---

## 12. MOBILE_SURFACE.md assimilation

Native clients MAY initiate VA authorization only through the released verification contract.

Requirements:

- Authorization Code + PKCE;
- no client secret in the app bundle;
- callback/deep-link/universal-link handling must bind to the initiating transaction and reject replay;
- locally retained authorization transaction material receives the protections required by D-034 once settled;
- mobile VA verification remains optional under the D-016 fallback unless later released otherwise.

---

## 13. EVENT_MODEL / audit assimilation

Do not emit raw provider payloads as Domain Events.

Audit facts should be bounded to outcomes such as:

- verification authorization initiated;
- callback accepted/rejected;
- provider verification succeeded/not-confirmed/unavailable;
- fallback selected;
- authorization revoked/expired where observed.

Audit payloads record identifiers, outcome/reason code, adapter family/version, environment, scope-set identifier, and timestamps — not tokens, ICNs, raw JWTs, or complete VA responses.

A new domain-event type is NOT required merely to implement D-035 unless a downstream domain workflow needs replayable business semantics. Audit evidence is sufficient for provider-protocol mechanics.

---

## 14. Reporting assimilation

D-035 verification status MUST NOT silently become an aggregate reporting dimension.

Until D-025 is settled, reporting remains disabled/limited according to the released reporting contract. Verification provenance/status cannot be used to create row-level exports, small-cell segments, or cross-tenant reports without explicit authority.

---

## 15. Decision relationship

### D-016

D-035 does not invalidate the historical D-016 decision. On D-035 release, the relationship should be recorded as:

```text
D-016: self-attestation is sufficient and remains fallback.
D-035: optional higher-confidence VA Veteran-status verification is authorized.
```

A future decision may make stronger proofing mandatory, but D-035 alone does not.

### D-007

Retention/deletion remains open. Therefore D-035 production enablement MUST minimize stored evidence and MUST NOT invent retention durations.

### D-013

Counsel/compliance review remains a production/pilot-operation gate as already specified. D-035 does not close it.

### D-025

Aggregate reporting remains independently gated. D-035 data does not expand reporting authority.

### D-034

Native-device local protection remains independently open. D-035 does not weaken its gate.

---

## 16. Release settlement requirements

D-035 may move from `DECISION_PENDING`/proposed to `DECIDED` only with an owner settlement containing:

```text
Gate: D-035 Veteran Verification
Owner name and role:
Decision: ACCEPT | REJECT | DEFER
Date/time (UTC):
Scope and constraints:
Authorized adapter/API family:
Minimum scope set:
Fallback policy:
Environment boundary:
Retention/privacy constraints:
Required evidence references/hashes:
Relationship to D-016:
```

An ACCEPT decision authorizes implementation according to the released spec. It does not by itself authorize production operation.

---

## 17. Non-goals

D-035 does not authorize:

- VA health-record access;
- VA disability-rating access;
- benefit enrollment or adjudication;
- DD-214 collection;
- clinical FHIR integration;
- background surveillance/re-verification;
- `offline_access` without a later released purpose;
- removal of the self-attestation fallback;
- denial of crisis/safety support solely from verification outcome;
- a claim that SUAS is affiliated with or endorsed by VA;
- reporting expansion;
- production enablement before gate settlement.
