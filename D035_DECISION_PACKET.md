# D035_DECISION_PACKET.md — Owner settlement packet for Veteran verification

**Status:** proposed  
**Decision:** D-035  
**Primary contract:** [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md)  
**Protocol:** [D035_PROTOCOL.md](D035_PROTOCOL.md)  
**Vectors:** [D035_TEST_VECTORS.md](D035_TEST_VECTORS.md)

## 1. Decision to make

Choose whether SUAS should offer an optional higher-confidence VA-backed Veteran-status verification path during onboarding while preserving D-016 self-attestation as fallback.

## 2. Facts already determined

### OBSERVED — SUAS

- D-016 currently makes self-attestation sufficient for the released pilot.
- D-035 is additive and must not silently make VA verification mandatory.
- SUAS treats Veteran support data as highly sensitive.
- D-007 retention durations, D-013 counsel review, D-025 reporting privacy, and D-034 native local-data protection remain independently gated.

### OBSERVED — VA interfaces

Two materially different status-verification patterns exist:

1. **Veteran Confirmation API**
   - status-only output;
   - API-key authorization;
   - caller supplies identifying information to match the person;
   - `not confirmed` has reason codes including `PERSON_NOT_FOUND`, `NOT_TITLE_38`, `MORE_RESEARCH_REQUIRED`, `ERROR`.

2. **Veteran Service History and Eligibility API**
   - OAuth 2.0/OIDC supported;
   - Authorization Code Grant supports Veteran-mediated consent;
   - `veteran_status.read` is the status scope;
   - broader service history, disability, benefits, flashes, and P&T scopes exist but are outside D-035 status-only purpose;
   - provider guidance recommends requesting the fewest scopes required.

## 3. Architecture consequence

The phrase “use the narrower API” is insufficient as a privacy rule.

The owner must choose between two data-flow models:

```text
A. DEMOGRAPHIC_MATCH
SUAS collects/transmits a minimum demographic projection
  -> VA Veteran Confirmation API
  -> normalized status

B. VETERAN_MEDIATED_OAUTH
Veteran authenticates/authorizes with VA
  -> VA Service History/Eligibility veteran-status scope
  -> normalized status
```

Both map to the same SUAS `VeteranVerificationPort`.

## 4. Decision criteria

Score each proposed adapter against:

| Criterion | Question |
|---|---|
| Data minimization | What new PII must SUAS collect, retain, or transmit? |
| User agency | Does the Veteran directly authorize VA access? |
| Friction | How many steps and failure modes are added to onboarding? |
| Access feasibility | Can SUAS obtain sandbox and production access under VA requirements? |
| Security | What credentials/tokens/demographic matching data must SUAS protect? |
| Reliability | What happens on VA outage, mismatch, or inconclusive result? |
| Mobile fit | Can the flow be implemented safely in native clients? |
| Auditability | Can SUAS prove exactly what was requested and why? |
| Scope containment | Can implementation prevent accidental expansion into service/benefit/health data? |

## 5. Owner direction recorded 2026-08-29

The owner accepted the recommended initial direction for D-035 design work:

```text
B1 capability: ACCEPT
B2 preferred adapter family: VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY
B3 fallback policy: SELF_ATTESTATION_REMAINS_AVAILABLE
B4 initial environment authority: LOCAL_FIXTURE + VA_SANDBOX_ONLY
B5 OAuth scope set:
  openid
  profile
  veteran_status.read
B6 re-verification policy:
  ONE_TIME_ONBOARDING_ONLY
  NO_BACKGROUND_REVERIFICATION
  NO_OFFLINE_ACCESS
B7 semantic invariant: ACCEPT
  NOT_CONFIRMED != NOT_A_VETERAN
B8 support-access invariant: ACCEPT
  verification failure/cancellation/outage/non-confirmation must not independently block an explicit support request
```

This owner direction does **not** by itself close D-035 or authorize production operation. It establishes the preferred implementation path for further specification and sandbox evidence.

`VaVeteranConfirmationAdapter` remains a secondary/alternate adapter family. It MUST NOT be used as an automatic fallback from OAuth. Activating it still requires an explicit deployment decision and an approved demographic projection.

## 6. Recommended settlement shape

```text
Capability: OPTIONAL_VA_VETERAN_STATUS_VERIFICATION
Preferred adapter: VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY
Fallback: SELF_ATTESTATION remains available
Initial environment: LOCAL_FIXTURE + VA_SANDBOX_ONLY
Production authority: BLOCKED
Broader VA data: FORBIDDEN
Reporting use: FORBIDDEN absent D-025 authority
Service denial from verification result alone: FORBIDDEN
Background re-verification: FORBIDDEN
Offline access: FORBIDDEN
```

## 7. Remaining owner/evidence questions before D-035 can close

The following remain unresolved and prevent release settlement:

1. Exact VA application/client registration identifiers and environment separation.
2. Exact redirect URI(s) for SANDBOX and later PRODUCTION.
3. Privacy Owner attestation for the OAuth data flow and normalized persistence set.
4. D-007-compatible retention posture for verification evidence and transient OAuth transaction material.
5. Security evidence for state, PKCE, callback replay, issuer/audience/signature validation, token redaction, and cross-user binding.
6. Accessibility review of redirect/cancel/error/fallback behavior.
7. Sandbox evidence hashes proving exact scope containment and no broader VA data collection.
8. Explicit release settlement recording that production remains separately blocked.

## 8. Release settlement form

```text
Gate: D-035 Veteran Verification
Owner name and role:
Decision: ACCEPT | REJECT | DEFER
Date/time (UTC):

B1 capability: ACCEPT
B2 adapter family: VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY
B3 fallback policy: SELF_ATTESTATION_REMAINS_AVAILABLE
B4 environment authority: LOCAL_FIXTURE + VA_SANDBOX_ONLY
B5 OAuth scope set: openid profile veteran_status.read
B6 re-verification policy: ONE_TIME_ONBOARDING_ONLY / NO_BACKGROUND_REVERIFICATION / NO_OFFLINE_ACCESS
B7 NOT_CONFIRMED semantic invariant: ACCEPT
B8 support-access invariant: ACCEPT

Sandbox redirect URI:
Production redirect URI: NOT_AUTHORIZED
VA application/client identifier reference:
Retention/privacy constraints:
Security constraints:
Accessibility/copy constraints:
Reporting constraints:
Relationship to D-016: additive; self-attestation remains sufficient fallback
Required evidence references/hashes:
Production authority: BLOCKED
```

## 9. Required evidence before ACCEPT/RELEASE

At minimum:

- exact VA documentation references and retrieval date;
- chosen OAuth data-flow diagram;
- exact scope-manifest hash;
- threat model;
- synthetic normalization vectors;
- callback/replay/PKCE evidence;
- JWT signature/issuer/audience/expiry validation evidence;
- log/redaction proof;
- cross-user/cross-tenant negative evidence;
- accessibility review evidence;
- privacy owner attestation;
- explicit statement that production operation remains blocked unless separately settled.
