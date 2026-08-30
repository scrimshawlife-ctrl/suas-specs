# PRODUCT.md — Shut Up and Serve (SUAS) v0.1

**Related:** [README.md](README.md), [GLOSSARY.md](GLOSSARY.md), [SAFETY.md](SAFETY.md), [PILOT.md](PILOT.md), [SETTLEMENT.md](SETTLEMENT.md), [DECISIONS.md](DECISIONS.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), [MVP_REFERENCE.md](MVP_REFERENCE.md)

**Status:** `draft` / `0.1.0` / not implementation authority.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).  
**SPEC-001 status:** `READY_FOR_REVIEW` (not `accepted`; not `released`; see [SPEC-001.md](SPEC-001.md))

---

## 1. Mission

Coordinate the shortest safe and consented path between a veteran's current need and an available human or material support resource.

"Shortest" means the fewest consented steps that produce a confirmed Fulfillment or an explicit Settlement of why fulfillment did not occur. It does not mean skipping Consent, human review on red-state, or confirmation.

"Safe" means: follow [SAFETY.md](SAFETY.md); do not automate emergency dispatch; do not diagnose; do not use generative models for safety-critical decisions.

"Consented" means: every share, notify, assign-outside-consent-scope, and trusted-contact alert requires a matching Consent Grant. See [CONSENT.md](CONSENT.md).

---

## 2. Product identity

| Field | Value |
|---|---|
| Product name | Shut Up and Serve |
| System identifier | SUAS |
| Kind | Consent-governed veteran support coordination platform |
| Spec authority | `SUAS-specs` |
| Implementation | `https://github.com/scrimshawlife-ctrl/SUAS` (must conform to released specs) |
| Client inventory | [REPOS.md](REPOS.md) — `suas` (web + API), `suas-ios`, `suas-android` |

---

## 3. Who it serves

Primary v0.1 operating population: Veterans enrolled in the Santa Clara County pilot.

Operational users: Responders, Organization Administrators, Service Providers, Trusted Contacts, SUAS System Administrators.

The 25–50-veteran pilot is an operating scope, not a product-definition or production-architecture ceiling. Future adoption beyond the pilot requires the applicable readiness and release gates; it does not require redefining the core product mission. See [SCALING.md](SCALING.md).

SUAS does not serve clinicians-as-clinicians. A Responder who happens to hold a clinical license is still a Responder in this product. Clinical practice is out of scope.

---

## 4. Roles

### 4.1 Veteran

The person whose need is coordinated. Owns Check-Ins, Consent Grants, Trusted Circle membership, and the right to revoke consent. May open or confirm needs, confirm or dispute Fulfillment, and complete Follow-Up responses when asked. Authentication: passwordless (see [AUTH.md](AUTH.md)).

MVP enrollment (D-016 `DECIDED` v0.1 default): self-attested veteran status plus a working email and/or phone via passwordless auth. No VA identity API, no DD-214 upload, and no in-person proofing are required for the 25–50 Santa Clara County pilot. Do not invent a VA partnership. A later proofing step would require a new released decision. See [ONBOARDING.md](ONBOARDING.md), [PILOT.md](PILOT.md), [AUTH.md](AUTH.md).

MVP visibility (D-015 `DECIDED` v0.1 default): the Veteran can see their own Check-Ins, their own Service Request status, Settlement fields written for them, and Follow-Up prompts addressed to them. The Veteran cannot see full Case Notes, other veterans, responder internal queue fields, or other Organizations. This is not a clinical chart. See [CASES.md](CASES.md) section 8.

### 4.2 Responder

A human coordinator. Claims or is assigned Support Cases. Performs actions in [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md). Must have MFA. Authorization is least-privilege and organization-scoped unless a SUAS System Administrator role is separately granted (it must not be implicit).

### 4.3 Organization Administrator

Administers one Organization: membership, responder enablement/revocation, org-owned Resources, org notification defaults. Cannot administer other Organizations. Cannot change global signal rules, consent templates, or system config. Distinct from SUAS System Administrator. See [ADMIN.md](ADMIN.md).

### 4.4 Trusted Contact

A person invited by a Veteran into the Trusted Circle. Sees and receives only what Consent Grants allow. Membership alone grants no visibility. See [TRUSTED_CIRCLE.md](TRUSTED_CIRCLE.md).

### 4.5 Service Provider

An organization or person that can fulfill a Service Request. May receive Referrals and Assignments. Does not automatically receive Case Notes, Check-In answers, or location.

A Service Provider does **not** need an API integration to be valid. API, webhook, deep-link, phone, email, referral-only, and manual-coordination paths may all be valid according to the later provider-integration contract. Specific provider brands are adapter/configuration decisions, not product-domain semantics. See [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md).

### 4.6 SUAS System Administrator

Global operator: users across orgs (with audit), questionnaire versions, signal-rule versions, consent templates, notification templates, pilot config, system config, cross-tenant incident response. Not an Organization Administrator. Must have MFA. Every privileged action emits an Audit Event.

---

## 5. Canonical loop

Defined also in [README.md](README.md). Repeated here as the product contract.

```text
SIGNAL → NEED → CONSENT → COORDINATION → FULFILLMENT → FOLLOW-UP → SETTLEMENT
```

### 5.1 SIGNAL

A Veteran completes a Check-In against a published `QuestionnaireVersion`, or a Veteran/Responder records an explicit need that still produces a Support Signal record for coordination priority.

The system computes a Support Signal: `GREEN` | `YELLOW` | `ORANGE` | `RED`.

Rules:

- Deterministic, inspectable, versioned, unit-tested, reproducible.
- No generative model for the primary signal.
- Record `signal_version`, `input_questionnaire_version`, `computed_at`, and basis.
- The signal is a coordination label, not a diagnosis.

See [CHECKINS.md](CHECKINS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md).

### 5.2 NEED

A concrete need is recorded as one or more Service Requests on a Support Case.

- **Support Case** = coordination around a Veteran.
- **Service Request** = a specific requested need.
- One case may contain multiple service requests.

Need categories in MVP: `FOOD`, `TRANSPORTATION`, `SHELTER`, `PEER_SUPPORT`.

See [CASES.md](CASES.md), [DISPATCH.md](DISPATCH.md).

### 5.3 CONSENT

Before any notification, data share, trusted-contact alert, or out-of-scope assignment, the system evaluates Consent Grants.

Consent is first-class, not a boolean. Grants are explicit, revocable, timestamped, versioned, auditable, and purpose-scoped. Revocation stops future use. Historical audit is preserved separately.

See [CONSENT.md](CONSENT.md).

### 5.4 COORDINATION

A Responder claims or is assigned the Support Case. Matching, contact, Referral, and Service Request assignment occur only through documented transitions.

See [CASES.md](CASES.md), [DISPATCH.md](DISPATCH.md), [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md), [RESOURCES.md](RESOURCES.md), [REFERRALS.md](REFERRALS.md).

### 5.5 FULFILLMENT

Acceptance, start, completion, and confirmation (veteran and/or responder). Assignment is not Fulfillment. Partial, failed, and cancelled outcomes are first-class. Funding is separate.

Provider-facing attempts are tracked separately as Fulfillment Attempts when an external/manual fulfillment route is used. A Fulfillment Attempt does not replace the canonical Service Request or Fulfillment record. See [FULFILLMENT.md](FULFILLMENT.md) and [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md).

### 5.6 FOLLOW-UP

First-class Follow-Up records with due dates, responsibility, retries, completion, reschedule, overdue, and escalation. Not hidden in Case Notes.

See [FOLLOWUP.md](FOLLOWUP.md).

### 5.7 SETTLEMENT

An explicit resolution record: what was requested, what occurred, what was fulfilled, what remains unresolved, who confirmed, when, remaining Follow-Up. Not a clinical outcome.

See [SETTLEMENT.md](SETTLEMENT.md).

---

## 6. Non-interchangeable concepts

Do not alias these in UI copy, API resources, or database table names that leak into contracts:

| Concept | Is not |
|---|---|
| Check-In | Support Signal, Support Case, Service Request |
| Support Signal | Diagnosis, Check-In, risk-of-suicide score |
| Support Case | Service Request, Referral, ticket-without-history |
| Service Request | Referral, Fulfillment, Fulfillment Attempt, Support Case |
| Referral | Service Request, Fulfillment |
| Assignment | Fulfillment |
| Fulfillment Attempt | Service Request, Fulfillment, provider-specific product state |
| Fulfillment | Assignment, Referral, Fulfillment Attempt, Settlement |
| Follow-Up | Case Note, Settlement |
| Settlement | Clinical outcome, Fulfillment |

---

## 7. Service categories

### 7.1 MVP (in scope)

| Code | Meaning (operational) |
|---|---|
| `FOOD` | Food access coordination (meal, pantry referral, grocery support). |
| `TRANSPORTATION` | Rides or fare support to a stated destination/purpose. |
| `SHELTER` | Temporary shelter coordination. Not permanent housing placement. |
| `PEER_SUPPORT` | Peer/human support conversation or accompaniment. Not therapy. |

### 7.2 Future (out of MVP; do not implement as if present)

`BENEFITS`, `HOUSING`, `HEALTHCARE_NAVIGATION`, `COMMUNITY`, `OTHER`.

These names are reserved. Eligibility rules, partner coverage, and workflows are `NOT_COMPUTABLE` until specified.

---

## 8. Operational boundaries (non-goals)

SUAS is **not**:

1. A crisis-prediction application.
2. An electronic health record (EHR).
3. A medical diagnosis tool.
4. An automated emergency-dispatch platform.
5. A replacement for emergency services.
6. A suicide-prediction or suicidality-determination system.
7. A VA-integrated benefits system (`NOT_COMPUTABLE` / not specified).
8. A Medi-Cal eligibility or billing system (see §10).
9. A continuous location tracker.
10. A clinical-efficacy measurement product.

MVP operational focus: food, transportation, temporary shelter, peer/human support, responder coordination, resource referrals, trusted-circle communication, follow-up.

---

## 9. Pilot scope

- Approximately 25–50 veterans.
- Santa Clara County, California.
- Partner orgs: placeholders `PARTNER_ORG_001` … until D-008 is closed.
- Responder staffing: `DECISION_PENDING` (D-009).
- Pilot readiness: `NOT_READY`.

Pilot enrollment capacity above 50 remains a controlled-pilot decision; production architecture must not assume 50 is a system capacity ceiling. See [PILOT.md](PILOT.md) and [SCALING.md](SCALING.md).

---

## 10. Medi-Cal / billing boundary

**Status:** `FUTURE`. Do not assert that SUAS activities are Medi-Cal billable.

Product path (not implemented in MVP):

```text
Fulfillment → Funding Eligibility → Funding Source → Optional Billing Adapter
```

Possible future funding sources (names only; no eligibility claimed): sponsor, donation, nonprofit, county program, grant, reimbursable program.

Funding is not Fulfillment. A Service Request may be `FULFILLED` / `CONFIRMED` with `funding_source = none`.

See [SETTLEMENT.md](SETTLEMENT.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 11. Governing production principles

These are product/architecture principles, not acceptance of the later detailed contracts:

- preserve the referenced MVP's recognizable interaction identity subject to safety, consent, privacy, authentication, accessibility, and canonical-domain overrides;
- preserve provider-neutral service fulfillment and manual-provider viability;
- do not encode avoidable pilot-only architecture ceilings;
- preserve canonical Service Request/Fulfillment semantics regardless of provider integration.

Detailed conformance semantics remain governed by later roadmap artifacts such as [MVP_REFERENCE.md](MVP_REFERENCE.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), and [RESILIENCE.md](RESILIENCE.md), which remain `draft` until their own stages are accepted/released.

---

## 12. Assumptions

- A Veteran can be reached by at least one consented channel (email and/or phone) during the pilot. Device-push is `FUTURE`.
- Responders are humans operating a coordination console, not an EHR.
- Resources in the catalog may be stale; freshness bands are operational recommendations, not legal coverage claims. See [RESOURCES.md](RESOURCES.md).
- Exact signal scoring is D-011 `DECISION_PENDING`.
- Approved safety copy is D-012 `DECIDED` in [SAFETY_COPY.md](SAFETY_COPY.md) (copy approval only; not production-operating approval).

---

## 13. Authority

- This file is the product contract for mission, roles, loop, categories, non-goals, and the governing production principles in §11.
- [GLOSSARY.md](GLOSSARY.md) is the terminology authority.
- Released specs in `SUAS-specs` bind `SUAS`.
- Draft specs do not authorize implementation.
