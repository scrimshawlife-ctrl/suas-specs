# D-006 counsel fact sheet — legal / HIPAA classification facts

**Status:** `DECISION_PENDING`. This file does **not** close D-006.
**HIPAA_APPLICABILITY:** `DECISION_PENDING`
**Authority:** Counsel owns classification (D-006) and register review (D-013).
**Date:** 2026-08-26 PT
**Related:** [COMPLIANCE.md](COMPLIANCE.md), [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [CONSENT.md](CONSENT.md), [DECISIONS.md](DECISIONS.md), [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

This document is **not legal advice**. It is **not** a HIPAA authorization, **not** a BAA, **not** a Notice of Privacy Practices, and **not** a certificate.

```text
THIS DOCUMENT DOES NOT MAKE SUAS HIPAA-COMPLIANT,
CCPA-COMPLIANT, TCPA-COMPLIANT, OR ANYTHING-COMPLIANT.
Do not claim HIPAA applies. Do not claim HIPAA does not apply.
```

---

## 1. Why this exists

Counsel needs a single packet of product facts to classify whether SUAS or a partner is a HIPAA covered entity (CE), a business associate (BA), or neither. Classification is D-006. Until it closes, implementation and public copy must not treat HIPAA as decided.

---

## 2. Official definitions (cite; do not paraphrase into a conclusion)

Use the HHS pages and the CFR text. Do not treat this section as a finding that SUAS is a CE, a BA, or neither.

- Covered entities and business associates: https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html
- Business associates: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html
- Sample BAA provisions: https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html
- Security Rule summary: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
- Definitions live at 45 CFR 160.103 (CE / BA). If an entity is neither, HHS says the HIPAA Rules do not apply to it.
- A CE is a health plan, a health care clearinghouse, or a health care provider that transmits health information electronically in connection with a standard transaction for which HHS adopted a standard.
- A BA creates, receives, maintains, or transmits PHI for a CE. A BAA is required when a CE engages a BA. Do not execute a BAA *as if* HIPAA applies until D-006 closes ([COMPLIANCE.md](COMPLIANCE.md) §5).

---

## 3. OBSERVED product facts counsel should use

Label each item `OBSERVED` unless a different label is stated.

**Identity and contact** (`OBSERVED`)

- Product name: Shut Up and Serve (SUAS). Builder: zer0state.
- Legal entity on public legal copy: Zero State LLC, 30 N Gould St Ste R, Sheridan, WY 82801. That address is a registered-agent mailing / legal home. It is not a claim that operations run there.
- Contact: zer0state@zer0state.com
- Canonical spec repo: `scrimshawlife-ctrl/suas-specs`. Implementation: `scrimshawlife-ctrl/SUAS`. Public Pages: https://scrimshawlife-ctrl.github.io/suas/ — poster, not live operations.

**Release and readiness** (`OBSERVED`)

- Released spec stack: `0.3.0` (D-033 native mobile contract released). The implementation kernel pin in `SUAS` remains `0.2.0` until a separate re-pin.
- SPEC-017 implementation conformance is active and **NOT READY**. All 12 readiness gates remain `NOT_READY`. SPEC-018 is the go/no-go for any real pilot or production.

**Intended later use** (`OBSERVED` as specified intent; not authorized today)

Identified opt-in coordination for veterans: Check-In `qv-001`, Support Signal `sv-001` in fixture/disabled modes, QRF / Support Case coordination.

Not an EHR. Not a diagnosis tool. Not suicide prediction. Not automated 911/PSAP dispatch. Not a VA health/benefits/identity API. Not Medi-Cal / CMS billing (billing adapter `FUTURE`). Not a store-distributed native app this week.

**Public legal copy** (`OBSERVED`)

Public legal/terms already say: not a HIPAA authorization; not a BAA; D-006 pending; do not say a health-privacy statute applies or does not.

**Operating agreement** (`OBSERVED`)

An operating-agreement draft exists as an unsigned multi-member OA. Do **not** invent member percents, capital, CEM, bank, or signatures.

**Pilot and open counsel items** (`OBSERVED`)

Pilot geography named in specs: Santa Clara County, 25–50 veterans, **not authorized**. D-008 partners remain open. D-013 counsel review of [COMPLIANCE.md](COMPLIANCE.md) remains open.

**Data the product is specified to handle when operated** (`OBSERVED`)

Identity (email/phone via passwordless auth), self-attested veteran status, consent grants, Check-In answers on published questionnaire `qv-001`, Support Signal levels, Support Case / QRF coordination facts, trusted-circle membership, fulfillment/request status.

[PRIVACY.md](PRIVACY.md) forbids collecting diagnosis / medical-history dumps and SUD treatment records by default. 42 CFR Part 2 is `NOT_COMPUTABLE` unless SUD records are later specified.

**Technical controls specified as product rules** (`OBSERVED`)

These are product rules. They are not a HIPAA conclusion.

- TLS
- Database and backup encryption (key management `DECISION_PENDING`)
- RBAC
- Tenant isolation
- Row-level authz
- MFA for Responder / Org Admin / SUAS Admin
- Immutable audit/domain events
- Minimization
- Consent evaluated at use time
- No production data in LOCAL/TEST/STAGING
- No secrets in git, logs, or client bundles
- UI string-forbid "HIPAA compliant" / "CCPA compliant" / "TCPA compliant"

**Deletion** (`OBSERVED` / `DECISION_PENDING`)

A synthetic deletion drill exists in implementation. D-007 retention/deletion durations remain `DECISION_PENDING`. The PRIVACY gate is `NOT_READY`.

**Vendors** (`DECISION_PENDING`)

D-001 hosting, D-002 auth/MFA factor, D-003 SMS, D-004 email, and D-005 production DB are all `DECISION_PENDING`. Production SMS/email/DB hosting is deferred in the 0.1.0 ledger.

**Native mobile** (`OBSERVED`)

[MOBILE_SURFACE.md](MOBILE_SURFACE.md) is released. Store listing and real-veteran use remain SPEC-018-gated. Compliance claims are forbidden in store metadata. D-034 on-device data protection is open.

---

## 4. What counsel is asked to decide (D-006)

Record one of the following. Do not invent the answer in this file.

- SUAS is a CE
- SUAS is a BA of a named CE
- SUAS is neither
- `EVIDENCE_INSUFFICIENT`, with the missing facts listed

---

## 5. What follows only if counsel later records that HIPAA applies

These items are **not** in force today.

- BAAs for vendors that would meet the then-decided definition (host, DB, auth, SMS, email, others).
- Security Rule risk analysis, policies, workforce training, contingency / restore evidence.
- Breach-notification counsel (deadlines follow class; do not invent them now).
- If CE: Notice of Privacy Practices and individual-rights process (access / amend / accounting).
- D-007 durations must be decided before production data operation.

---

## 6. Forbidden until D-006 closes

- Claim HIPAA applies or does not apply.
- Claim "HIPAA compliant".
- Execute a BAA as if HIPAA already applies.
- Collect diagnosis / medical-history dumps or Part 2 SUD records.
- Invent statutory notice deadlines.
- Put HIPAA in hackathon pitch copy as a completed status.

---

## 7. Open related decisions

| ID | Topic | Status |
|---|---|---|
| D-006 | Legal / HIPAA classification | `DECISION_PENDING` |
| D-013 | Counsel review of the compliance register | `DECISION_PENDING` |
| D-007 | Retention / deletion durations | `DECISION_PENDING` |
| D-001–D-005 | Hosting, auth/MFA, SMS, email, production DB | `DECISION_PENDING` |
| D-008 | Operating pilot partners | `DECISION_PENDING` |
| D-034 | On-device protection of locally retained veteran data | `DECISION_PENDING` |
