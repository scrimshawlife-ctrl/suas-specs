# D035_SANDBOX_EVIDENCE_AUTHORITY.md — limited sandbox evidence authority

**Decision:** D-035 Veteran Verification  
**Gate qualifier:** `IMPLEMENTATION_EVIDENCE_AUTHORIZED`  
**Global decision status:** `DECISION_PENDING`  
**Release authority:** [RELEASE_DECISIONS-0.4.0.md](RELEASE_DECISIONS-0.4.0.md) / [RELEASE_MANIFEST-0.4.0.md](RELEASE_MANIFEST-0.4.0.md)  
**Production authority:** `BLOCKED`

## Owner settlement

Gate: D-035 Veteran Verification — Sandbox Evidence Authority

Decision: `ACCEPT_LIMITED_IMPLEMENTATION_AUTHORITY`

This settlement authorizes implementation of the VA Service History and Eligibility status-only OAuth path in LOCAL fixture and VA SANDBOX environments solely to produce D-035 release evidence. It does not close D-035, replace D-016, authorize production credentials, or authorize production operation.

## Limited implementation scope

- Preferred adapter: `VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY`.
- Authorization model: OAuth 2.0 / OIDC Authorization Code Grant.
- Approved sandbox scope set: `openid profile veteran_status.read`.
- Fallback: `SELF_ATTESTATION_REMAINS_AVAILABLE` under D-016.
- Re-verification: `ONE_TIME_ONBOARDING_ONLY`, `NO_BACKGROUND_REVERIFICATION`, `NO_OFFLINE_ACCESS`.

The authorized work is limited to the provider-neutral `VeteranVerificationPort`, VA sandbox adapter, OAuth authorization transaction state, PKCE S256, state/session binding, callback replay protection, JWT signature/issuer/audience/expiry validation, normalized verification persistence, sandbox onboarding UX, deterministic and sandbox integration tests, accessibility/privacy/data-flow/log-redaction/scope-containment evidence, and corrected SUAS-specific staging redirect configuration.

## Invariants and prohibitions

`NOT_CONFIRMED != NOT_A_VETERAN`. VA verification failure, cancellation, outage, or non-confirmation MUST NOT independently block an explicit support request.

The following remain forbidden: production VA credentials; PRODUCTION adapter mode; real production Veteran data; removal of D-016 self-attestation; Client Credentials as the onboarding default; Veteran Confirmation demographic lookup as a silent fallback; `offline_access`; service-history, disability, benefits, flashes, P&T, health, claims, or FHIR access; DD-214 or SSN collection; background re-verification; reporting use under D-035; and any claim that D-035 is decided.

Normalized verification evidence only may be retained. Raw VA payloads, access/refresh tokens, and provider secrets are not domain storage. D-007 remains independently unresolved and D-025 remains controlling for reporting.

## Evidence required before final settlement

1. exact VA sandbox client identifier reference;
2. exact registered sandbox redirect URI;
3. approved scope-set manifest/hash;
4. Privacy Owner attestation and D-007-compatible retention posture;
5. state/PKCE/JWT/replay security evidence;
6. log/redaction evidence;
7. accessibility review evidence; and
8. scope-containment and environment-isolation evidence hashes.

D-035 may move to `DECIDED` only after those records are reviewed and explicitly accepted by the designated owner(s). This qualifier is a gate qualifier, not a replacement global decision status.
