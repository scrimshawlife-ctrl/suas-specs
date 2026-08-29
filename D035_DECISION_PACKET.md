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

## 5. Recommended settlement shape

A conservative initial settlement would be:

```text
Capability: OPTIONAL_VA_VETERAN_STATUS_VERIFICATION
Fallback: SELF_ATTESTATION remains available
Production required: NO
Initial environment: SANDBOX only
Broader VA data: FORBIDDEN
Reporting use: FORBIDDEN absent D-025 authority
Service denial from verification result alone: FORBIDDEN
```

The adapter family itself should be chosen only after the privacy owner compares the demographic projection required by Veteran Confirmation against the OAuth data flow required by Service History/Eligibility.

## 6. Owner questions

### B1 — Capability

Should optional VA-backed status verification be authorized at all?

`ACCEPT | REJECT | DEFER`

### B2 — Initial adapter family

Choose one:

```text
VA_VETERAN_CONFIRMATION
VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY
BOTH_WITH_DEPLOYMENT_POLICY
DEFER_ADAPTER_SELECTION
```

### B3 — Fallback

Recommended:

```text
SELF_ATTESTATION_REMAINS_AVAILABLE
```

Any choice to remove fallback is outside this D-035 proposal and requires a new decision.

### B4 — Environment

Recommended initial authority:

```text
LOCAL_FIXTURE + VA_SANDBOX_ONLY
```

Production requires a separate readiness settlement.

### B5 — Data collection

For `VA_VETERAN_CONFIRMATION`, approve an exact demographic projection only after privacy review.

For OAuth, approve exact scope set:

```text
openid
profile
veteran_status.read
```

### B6 — Re-verification

Recommended initial rule:

```text
ONE_TIME_ONBOARDING_ONLY
NO_BACKGROUND_REVERIFICATION
NO_OFFLINE_ACCESS
```

### B7 — User-visible semantics

Approve the invariant:

```text
NOT_CONFIRMED != NOT_A_VETERAN
```

### B8 — Support-access rule

Approve:

```text
VA verification failure, cancellation, outage, or non-confirmation
MUST NOT independently block an explicit support request.
```

## 7. Release settlement form

```text
Gate: D-035 Veteran Verification
Owner name and role:
Decision: ACCEPT | REJECT | DEFER
Date/time (UTC):

B1 capability:
B2 adapter family:
B3 fallback policy:
B4 environment authority:
B5 exact demographic projection OR OAuth scope set:
B6 re-verification policy:
B7 NOT_CONFIRMED semantic invariant: ACCEPT | REJECT
B8 support-access invariant: ACCEPT | REJECT

Retention/privacy constraints:
Security constraints:
Accessibility/copy constraints:
Reporting constraints:
Relationship to D-016:
Required evidence references/hashes:
Production authority: BLOCKED | SEPARATELY_SETTLED
```

## 8. Required evidence before ACCEPT

At minimum:

- exact VA documentation references and retrieval date;
- chosen adapter data-flow diagram;
- data inventory/projection hash;
- threat model;
- synthetic normalization vectors;
- callback/replay/PKCE evidence if OAuth selected;
- log/redaction proof;
- accessibility review plan;
- privacy owner attestation;
- explicit statement that production operation remains blocked unless separately settled.
