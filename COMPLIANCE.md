# COMPLIANCE.md — Compliance register (SUAS v0.1)

**Related:** [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [DECISIONS.md](DECISIONS.md), [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md), [CONSENT.md](CONSENT.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [SAFETY.md](SAFETY.md), [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md), [SETTLEMENT.md](SETTLEMENT.md), [PILOT.md](PILOT.md), [ONBOARDING.md](ONBOARDING.md), [RIDES.md](RIDES.md), [ISLANDS.md](ISLANDS.md)

**Status:** `draft` / `0.1.0`. This file is a **register**, not a certification.

---

## 1. Purpose

Record legal and regulatory regimes that **might** apply to SUAS, the epistemic status of each, the operational controls already specified, and what is forbidden. This is a **compliance register**, not a claim that SUAS is compliant with any regime.

This document is **not legal advice**. Counsel and [D-006](DECISIONS.md) own legal classification. Implementation, ops, and product copy must not treat this file as a certificate, a filing, or a completed legal review.

```
THIS DOCUMENT DOES NOT MAKE SUAS HIPAA-COMPLIANT,
CCPA-COMPLIANT, TCPA-COMPLIANT, OR ANYTHING-COMPLIANT.
```

Do not display "HIPAA compliant", "CCPA compliant", "TCPA compliant", or any equivalent claim in product UI, onboarding copy, or operator consoles. See [ONBOARDING.md](ONBOARDING.md).

---

## 2. HIPAA_APPLICABILITY

```
HIPAA_APPLICABILITY = DECISION_PENDING
```

See [SECURITY.md](SECURITY.md) and [DECISIONS.md](DECISIONS.md) **D-006**. Whether SUAS or a partner is a covered entity (CE) or business associate (BA) is **not decided**. Do not claim HIPAA applies. Do not claim HIPAA does not apply. Do not invent a BA agreement as if the classification were closed.

Counsel facts for classification are in [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md). That file is a register packet, not a legal opinion. It does not close D-006 and does not change `HIPAA_APPLICABILITY`.

---

## 3. What SUAS does regardless of legal class

These controls are **product and security rules**. They are not a legal conclusion that any statute is satisfied.

| Control | Rule | Spec |
|---|---|---|
| Sensitivity | Treat veteran support data as **highly sensitive** regardless of HIPAA classification | [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md) |
| TLS | All network traffic in transit | [SECURITY.md](SECURITY.md) |
| Encryption at rest | Database and backups encrypted; key management `DECISION_PENDING` | [SECURITY.md](SECURITY.md) |
| RBAC | Role + tenant + row + consent | [AUTH.md](AUTH.md), [SECURITY.md](SECURITY.md) |
| Tenant isolation | `tenant_id` on tenant-owned rows; no cross-tenant query without an audited SUAS-admin path | [SECURITY.md](SECURITY.md) |
| MFA | Required for Responder, Organization Administrator, SUAS System Administrator | [AUTH.md](AUTH.md) |
| Audit | Immutable Audit Events and Domain Events | [EVENT_MODEL.md](EVENT_MODEL.md) |
| Minimization | Do not collect fields not required by a specified workflow | [PRIVACY.md](PRIVACY.md) |
| Consent grants | First-class, purpose-scoped, revocable; evaluated at use time | [CONSENT.md](CONSENT.md) |
| No prod data in dev | Absolute. LOCAL / TEST / STAGING never receive PRODUCTION data | [DEPLOYMENT.md](DEPLOYMENT.md) |

---

## 4. Regime register

Do **not** invent applicability as fact. The **Epistemic** and **Status** columns are the authority for how strongly a row may be treated.

| Regime | Why it might apply | Epistemic | Status | What SUAS does now | What is forbidden |
|---|---|---|---|---|---|
| HIPAA / HITECH | SUAS or a partner *might* later be classified as a CE or BA. Depends on legal facts not in this stack. | `DECISION_PENDING` (D-006) | Open. Counsel owns classification. | Treat data as highly sensitive; TLS; encryption at rest; RBAC; tenant isolation; MFA; audit; minimization; consent grants; no prod-in-dev. Do not collect PHI-like dumps (diagnoses, medical history) by default ([PRIVACY.md](PRIVACY.md)). | Claim HIPAA applies or does not apply. Claim "HIPAA compliant". Collect diagnosis / medical-history dumps. Execute a BAA *as if* HIPAA already applies (see §5). |
| 42 CFR Part 2 | Would matter only if substance-use-disorder (SUD) records enter scope. | `NOT_COMPUTABLE` unless SUD records are later specified | Out of MVP collection scope | Do not collect SUD treatment records. | Collect Part 2 records. Invent a Part 2 compliance program. |
| CCPA / CPRA | Pilot geography is Santa Clara County, California. Veterans in the pilot are consumers under California privacy law (`INFERRED` from geography + role, not a counsel opinion). | `INFERRED` relevant | Do not claim compliance | Minimization; veteran export (package format `DECISION_PENDING`, [PRIVACY.md](PRIVACY.md)); deletion process gated on D-007; no sale of data. | Claim "CCPA compliant" / "CPRA compliant". Sell data. Invent a completed deletion SLA before D-007. |
| TCPA / California robocall-SMS rules | MVP uses SMS for OTP and operational notices ([AUTH.md](AUTH.md), [NOTIFICATIONS.md](NOTIFICATIONS.md)). | `INFERRED` relevant | Do not claim compliance. SMS vendor D-003 open. | Require documented `consent_basis` before every SMS. Revocation stops future sends. If no SMS provider, mark the channel `UNAVAILABLE` ([ONBOARDING.md](ONBOARDING.md)). | Claim TCPA compliance. Send SMS without `consent_basis`. Fake-send when the channel is unavailable. |
| CAN-SPAM / California email rules | MVP uses EMAIL for magic links and operational notices. | `INFERRED` relevant | Do not claim compliance. Email vendor D-004 open. | Require documented `consent_basis` before every operational email. Revocation stops future sends. Bounce/delivery webhooks update `delivery_status` only. | Claim email-law compliance. Marketing mail. Send without `consent_basis`. |
| VA / federal veteran-record APIs | A veteran-support product *could* later integrate VA benefits, health, or identity APIs. | `NOT_COMPUTABLE` | No VA integration in MVP | None. Do not invent a VA client. | Add VA API clients. Claim a VA partnership. Collect DD-214 / service-record dumps ([PRIVACY.md](PRIVACY.md)). |
| Medi-Cal / CMS billing | A later funding path *could* involve Medi-Cal or CMS billing. | `FUTURE` | Not coupled to dispatch | Settlement records coordination outcomes only. Billing adapter is `FUTURE` ([SETTLEMENT.md](SETTLEMENT.md)). | Assert billability. Add clearinghouse / X12 / Medi-Cal clients. Store payment-card data. |
| Emergency / 911 / PSAP APIs | Red-state and veteran-initiated emergency flows exist as **display + human review**, not dispatch. | `OBSERVED` product non-goal | Out of scope | Surface approved crisis-resource copy (D-012). Prioritize human review. No automated emergency dispatch ([SAFETY.md](SAFETY.md)). | Automated 911 / PSAP calling. Imply SUAS replaces emergency services. Invent safety copy before D-012. |
| SB 903 / peer-support register | Rev 3 build direction references peer-support operating questions that **might** intersect a statute or register described as `SB 903`. The legal status of that regime and its applicability to SUAS are not established in this stack. | `NOT_COMPUTABLE` | Open. This row is a register note only; it is **not legal advice**. | Keep peer support framed as coordination, not a legal classification. Keep legal-entity, reporting, and volunteer-screening questions open in [DECISIONS.md](DECISIONS.md). | Claim SB 903 is law, claim SUAS is inside or outside it, or claim SUAS is compliant with it. |
| SOC 2 / ISO 27001 | Operators sometimes ask for these attestations. | `NOT_COMPUTABLE` | No claim | Controls in [SECURITY.md](SECURITY.md) exist as product rules, not as an audit report. | Claim SOC 2 or ISO 27001. Display a certification badge. |
| Breach-notification statutes | A security incident *might* trigger statutory notice (federal and/or California). Deadlines depend on classification (D-006) and facts. | `DECISION_PENDING` counsel | Open | [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) defines detect → contain → preserve → notify authorized owners → remediate → review → close. | Invent statutory deadlines. Notify unconsented contacts. Treat the incident file as a legal filing. |

---

## 5. Vendor terms and BAA

1. Do **not** execute a Business Associate Agreement (BAA) *as if* HIPAA applies until **D-006** is closed.
2. If D-006 later records that HIPAA applies, BAAs become **required** for relevant vendors (auth, SMS, email, host, database, and any other party that would meet the then-decided definition). That requirement is not in force today.
3. Until D-006 closes, still require **written data-processing terms** with any vendor that will process veteran support data. This is an `INFERRED` operational control (least-privilege contracting), **not** a legal conclusion that a particular statute applies.
4. Vendor selection remains [D-001](DECISIONS.md) through [D-005](DECISIONS.md). Do not encode a vendor name as a compliance decision.

---

## 6. SMS and email

Every SMS or EMAIL send records `consent_basis` (Consent Grant id or a documented system basis). Revocation stops future sends. Preferences cannot authorize a send.

See [NOTIFICATIONS.md](NOTIFICATIONS.md) and [CONSENT.md](CONSENT.md).

OTP / magic-link challenges use a documented system basis (enrollment or authentication), still recorded on the Notification row. Operational notices to Trusted Contacts require a matching `can_receive` grant at the relevant Support Signal level.

If D-003 or D-004 is still open in an environment, that channel is `UNAVAILABLE`. Do not fake-send. See [ONBOARDING.md](ONBOARDING.md) and [APIS.md](APIS.md).

---

## 7. Safety copy (D-012) as a compliance-adjacent control

Approved crisis-resource text is [D-012](DECISIONS.md) `DECISION_PENDING`. Until closed:

- Red-state must still **not** imply that SUAS replaces 911 ([SAFETY.md](SAFETY.md)).
- Do not invent official crisis-resource wording for veterans.
- Admins see a blocked/incomplete banner when the slot is unset ([ONBOARDING.md](ONBOARDING.md)).

D-012 is a **compliance-adjacent control**: crisis resources must not imply SUAS replaces emergency services. Closing D-012 is not a legal classification.

---

## 8. Pilot gate — D-013

Counsel must review **this register** before operating the 25–50 veteran Santa Clara County pilot.

```
D-013  Counsel review of COMPLIANCE.md regime register before pilot
Status: DECISION_PENDING
```

See [DECISIONS.md](DECISIONS.md) and [PILOT.md](PILOT.md). Closing D-013 is a recorded review of this register. It is **not** a claim that SUAS is compliant with any row in §4.

Pilot readiness remains `NOT_READY` until the gates in [STATUS.md](STATUS.md) pass **and** D-013 is closed. Do not treat draft specs as permission to operate.

---

## 9. Non-goals

- Legal opinions
- Regulatory filings
- Certifications (SOC 2, ISO 27001, HIPAA, CCPA, or any other)
- Invented partner agreements
- Invented statutory deadlines
- Invented VA, county, or Medi-Cal relationships
- Product copy that claims compliance

---

## 10. Actors

| Actor | Role in this register |
|---|---|
| Counsel | Owns legal classification (D-006) and review of this register (D-013) |
| SUAS System Administrator | Operates controls; does not declare legal status |
| Organization Administrator | Tenant-scoped ops; same prohibition on compliance claims |
| Implementation (`SUAS`) | Encodes controls; string-forbids compliance claims in UI |
| Specification (`SUAS-specs`) | Canonical register; not a certificate |

---

## 11. Testability

| Check | Pass condition |
|---|---|
| UI string forbid | Product UI, onboarding, and admin consoles contain no substring `HIPAA compliant` or `CCPA compliant` (case-insensitive). Same for `TCPA compliant`. |
| No forbidden clients | MVP has no 911 / PSAP, VA, or Medi-Cal / clearinghouse / X12 API clients ([APIS.md](APIS.md)). |
| SMS/EMAIL path | Every send path requires `consent_basis`; missing basis is rejected ([NOTIFICATIONS.md](NOTIFICATIONS.md)). |
| BAA gate | No BAA-as-if-HIPAA workflow is enabled while D-006 is open. |
| Safety copy | Unset D-012 does not present invented crisis copy to veterans; does not imply SUAS replaces 911. |
| Register ≠ certificate | This file is linked as a register in [README.md](README.md) / [STATUS.md](STATUS.md); no "compliant" badge is specified. |

---

## 12. Links

[SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [DECISIONS.md](DECISIONS.md), [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md), [CONSENT.md](CONSENT.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [SAFETY.md](SAFETY.md), [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md), [SETTLEMENT.md](SETTLEMENT.md), [PILOT.md](PILOT.md), [ONBOARDING.md](ONBOARDING.md), [APIS.md](APIS.md), [AUTH.md](AUTH.md), [DEPLOYMENT.md](DEPLOYMENT.md)
