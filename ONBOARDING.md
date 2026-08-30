# ONBOARDING.md — Admin first-run and first-time user experience (SUAS v0.1)

**Related:** [ADMIN.md](ADMIN.md), [AUTH.md](AUTH.md), [PILOT.md](PILOT.md), [SAFETY.md](SAFETY.md), [CONSENT.md](CONSENT.md), [CHECKINS.md](CHECKINS.md), [RESOURCES.md](RESOURCES.md), [COMPLIANCE.md](COMPLIANCE.md), [APIS.md](APIS.md), [API.md](API.md), [DEPLOYMENT.md](DEPLOYMENT.md), [DECISIONS.md](DECISIONS.md), [FRICTION.md](FRICTION.md)

**Status:** `draft` / `0.1.0`. First-run is a **gated bootstrap**, not a growth tour.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).

**Actors:** SUAS System Administrator, Organization Administrator, Responder, Veteran, Trusted Contact, Service Provider.

---

## 1. Purpose

Specify how an **empty system** becomes operable, and how each role completes first-run.

The modular monolith must not present an empty, unusable console with no next action. Bootstrap is **gated**, **persisted**, and **auditable**. It is not a hidden flag and not a demo seeder.

Do not invent partners, vendors, or legal status. Use `PARTNER_ORG_001` until D-008. Do not claim HIPAA or any other compliance during onboarding copy ([COMPLIANCE.md](COMPLIANCE.md)).

---

## 2. Environment rule

First-run runs **once per environment**, separately:

`LOCAL` | `TEST` | `STAGING` | `PRODUCTION`

See [DEPLOYMENT.md](DEPLOYMENT.md). Checklist state does **not** copy across environments. Completing bootstrap in STAGING does not bootstrap PRODUCTION.

The environment class **must be visible** on every admin and responder surface (banner or equivalent). Never operate PRODUCTION thinking it is STAGING.

---

## 3. First-run state machine

Suggested states for a user, an organization, and the environment bootstrap checklist. Names are canonical for this spec. Do not alias them.

```
NOT_STARTED → AUTHENTICATED → MFA_ENROLLED → PROFILE_COMPLETE → ORG_BOUND → CHECKLIST_COMPLETE → ACTIVE
```

Exceptional: `SUSPENDED`, `REVOKED` (from [AUTH.md](AUTH.md)). Those states exit the happy path; they are not first-run steps.

| State | Meaning |
|---|---|
| `NOT_STARTED` | No successful verify in this environment for this actor / checklist. |
| `AUTHENTICATED` | Session exists; privileged elevation may still be incomplete. |
| `MFA_ENROLLED` | MFA factor enrolled. **Required** before any other admin or responder privileged action. |
| `PROFILE_COMPLETE` | Required profile fields for the role are present. |
| `ORG_BOUND` | An `OrganizationMembership` with `status=ACTIVE` exists (org-scoped roles). SUAS-admin is globally bound, not org-bound. |
| `CHECKLIST_COMPLETE` | Environment bootstrap checklist is closed (SUAS-admin) **or** the role-specific first-run checklist is closed. |
| `ACTIVE` | Actor may perform in-role actions subject to authz + consent. |
| `SUSPENDED` | Temporary halt. Sessions invalidated per [AUTH.md](AUTH.md). |
| `REVOKED` | Permanent halt for that user or membership. |

### 3.1 Skip rules

| Actor | May skip | Must not skip |
|---|---|---|
| Veteran | Trusted Circle invites | Auth; Pilot enrollment (consent to participate); seeing what SUAS is and is not (approved copy or the standing non-goal statements) |
| Responder | Queue tour acknowledgment may be deferred **after** MFA + membership, but queue **actions** require MFA + `ACTIVE` membership | MFA; org membership |
| Organization Administrator | — | MFA; org profile review; cannot publish global questionnaire or signal rules |
| SUAS System Administrator | — | MFA; environment-class confirmation; first Organization; first org-admin membership; QuestionnaireVersion publish; signal-rule version (or labeled unreleased fixture); minimum Resource catalog; notification template/channel config; safety-copy slot **acknowledgment**; Pilot config; checklist close |
| Trusted Contact | — | Accept invite; first-run **must** display actual grants |
| Service Provider | App-store style onboarding (not in MVP) | Acceptance of an assignment (`ACCEPTED`) when they act |

Admin cannot skip MFA, first org, questionnaire publish, or safety-copy slot **acknowledgment**. Acknowledgment means: either D-012 copy is set, or the admin has recorded that the slot is unset and veterans will not be shown invented copy.

---

## 4. SUAS System Administrator first-run (empty system)

Order is gated. A later step must not become available in a way that bypasses an earlier hard gate. Soft-parallelism (e.g. drafting resources while a questionnaire is in `DRAFT`) is allowed; **publish / close** still requires the gates below.

### 4.1 Steps

1. **Stronger auth + MFA enrolled** before any other admin action ([AUTH.md](AUTH.md)). No bootstrap writes without an elevated session.
2. **Confirm environment class is visible.** The admin explicitly acknowledges `LOCAL` / `TEST` / `STAGING` / `PRODUCTION`. Never operate PRODUCTION thinking it is STAGING.
3. **Create the first Organization.** Placeholder `PARTNER_ORG_001` until D-008. Do not invent a partner name.
4. **Create `OrganizationMembership`** for the first Organization Administrator (or the SUAS-admin acting as bootstrap). Org-admin ≠ SUAS-admin ([ADMIN.md](ADMIN.md)).
5. **Publish a `QuestionnaireVersion`.** Veterans cannot enroll without a published version ([CHECKINS.md](CHECKINS.md), [PILOT.md](PILOT.md)).
6. **Publish a support-signal rule version.** D-011 is still open: the published artifact may be an **unreleased fixture** labeled `UNRELEASED_FIXTURE`. Do not invent weights as policy ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [TESTING.md](TESTING.md)).
7. **Load or verify a minimum Resource catalog** for Santa Clara County with `last_verified_at`, covering `FOOD`, `TRANSPORTATION`, `SHELTER`, `PEER_SUPPORT`. Stale or unverified resources must be **visible as stale**, not silently used ([RESOURCES.md](RESOURCES.md)).
8. **Configure notification templates + channels.** SMS provider D-003 stays `DECISION_PENDING`. D-004 selects Resend as the sole EMAIL provider. If a channel has no valid configured provider, mark it `UNAVAILABLE`. Do not fake-send ([NOTIFICATIONS.md](NOTIFICATIONS.md), [APIS.md](APIS.md), [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md)).
9. **Set the environment to render the D-012 approved copy** in [SAFETY_COPY.md](SAFETY_COPY.md) (`SUAS_SAFETY_COPY_MODE=approved` per [ENVIRONMENT.md](ENVIRONMENT.md)). If the environment is not in `approved` mode: red-state still must **not** imply SUAS replaces 911; show a **blocked / incomplete banner to admins**; do **not** show invented copy to veterans ([SAFETY.md](SAFETY.md), [SAFETY_COPY.md](SAFETY_COPY.md)).
10. **Record `Pilot` + `PilotEnrollment` config** (approximately 25–50 veterans, Santa Clara County) ([PILOT.md](PILOT.md)).
11. **Persist the bootstrap checklist** and close it. Closing emits Audit Events. The checklist is readable via `GET /admin/bootstrap/status`.

### 4.2 Persistence and audit

Each completed step writes:

- checklist row (environment, step id, actor, `completed_at`, notes)
- Audit Event (who, what, when, environment class)

`POST /admin/bootstrap/commands/complete-step` is the command. Do not flip a boolean in config without the command. Replays use `Idempotency-Key` ([API.md](API.md)).

Closing the checklist (`CHECKLIST_COMPLETE` → environment first-run `ACTIVE`) is itself a command and an Audit Event. Re-opening a step after close is an audited admin action, not a silent edit.

### 4.3 Hard gates vs acknowledgment

| Step | Gate type |
|---|---|
| 1 MFA | Hard. No other admin action. |
| 2 Environment class | Hard acknowledgment. |
| 3 First Organization | Hard before org-scoped work. |
| 4 First org-admin membership | Hard before org-admin first-run. |
| 5 Questionnaire publish | Hard before veteran enrollment. |
| 6 Signal-rule version | Hard before Check-In completion can compute a signal. Fixture allowed if labeled. |
| 7 Minimum resources | Hard before referrals / matching in PRODUCTION. TEST/STAGING may use labeled fixture resources. |
| 8 Notification channels | Hard to mark each channel `AVAILABLE` or `UNAVAILABLE`. SMS/EMAIL may be `UNAVAILABLE`. |
| 9 Safety-copy slot | Hard **acknowledgment**. D-012 copy is released in [SAFETY_COPY.md](SAFETY_COPY.md); the environment may remain not-`approved` if the admin records that veterans will not see invented copy. |
| 10 Pilot config | Hard before enrollment. |
| 11 Checklist close | Hard before `Pilot` operations begin. D-013 (counsel review of [COMPLIANCE.md](COMPLIANCE.md)) remains a **pilot-operation** gate, not a bootstrap-UI gate. |

---

## 5. Organization Administrator first-run (per org)

Per Organization, after the SUAS-admin has created the org and membership:

1. Accept invite / complete passwordless auth.
2. Enroll MFA before any org-admin write ([AUTH.md](AUTH.md)).
3. Review org profile (name, counties, contact). Do not rename `PARTNER_ORG_001` to a real partner until D-008.
4. Invite / activate Responders (`OrganizationMembership` + `ResponderProfile`).
5. Verify org-owned Resources (`last_verified_at`, `verification_source`).
6. Cannot publish global questionnaire or signal rules (SUAS-admin only).
7. Cannot see other tenants.

Org-admin first-run state uses the same machine in §3, scoped to that org. Completing it does not close the environment bootstrap checklist.

---

## 6. Empty-state UX (responder console)

A responder console with **zero cases is valid**.

Show:

- Queue empty
- Environment class
- Next actions: verify resources; wait for enrollments; review filters ([RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md))

Do **not** seed fake veteran cases in `PRODUCTION`.

`TEST` / `STAGING` may use **clearly labeled fixture veterans**. Fixture records must be marked as fixtures in the UI and in data (`UNRELEASED_FIXTURE` or equivalent). They must not be copyable into PRODUCTION ([DEPLOYMENT.md](DEPLOYMENT.md): no prod data in non-prod, and the reverse — no fixture veterans promoted as real).

---

## 7. First-time user experience (other roles)

### 7.1 Veteran

1. **Passwordless auth:** magic link / email OTP / phone OTP where supported ([AUTH.md](AUTH.md)). Phone OTP depends on D-003; if SMS is `UNAVAILABLE`, do not offer phone OTP as if it worked.
2. **Enrollment into the Pilot.** This is consent **to participate** in the Pilot, not a Trusted Circle boolean and not a blanket share grant ([CONSENT.md](CONSENT.md), [PILOT.md](PILOT.md)).

   MVP identity-proofing (D-016 `DECIDED` v0.1 default): enrollment is **self-attested veteran status** plus a working email and/or phone via passwordless auth ([AUTH.md](AUTH.md)). No VA identity API, no DD-214 upload, and no in-person proofing are required for the 25–50 Santa Clara County pilot. Do not invent a VA partnership. A later proofing step would require a new released decision.
3. **Explain what SUAS is and is not:** not 911, not an EHR, not a diagnosis tool. Crisis/safety wording is the D-012 approved copy in [SAFETY_COPY.md](SAFETY_COPY.md). Use the standing non-goal statements from [PRODUCT.md](PRODUCT.md) / [SAFETY.md](SAFETY.md) for everything else — do not invent marketing or compliance claims. Do not claim HIPAA.
4. **First Check-In after enrollment.** The veteran **can abandon**. Incomplete / abandoned is handled per [CHECKINS.md](CHECKINS.md). A Check-In is not a Support Signal.
5. **Optional Trusted Circle invites.** Not required to complete first-run.
6. **Service request without a completed Check-In** is allowed if the veteran **explicitly** requests help. NEED can start from an explicit request ([CASES.md](CASES.md), [DISPATCH.md](DISPATCH.md)).

Command: `POST /veterans/me/commands/complete-enrollment` ([APIS.md](APIS.md)). Authenticated. Not a public unauthenticated signup dump. Not auto-enroll.

Veteran skip: Trusted Circle. Veteran must not be auto-enrolled.

### 7.2 Responder

- **Invite-only.** No self-serve responder signup.
- **MFA required** before queue access.
- First-run after MFA + `ACTIVE` membership:
  - Org context (which Organization, which tenant)
  - Queue tour (filters in [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md))
  - Assignment is **not** fulfillment
  - Red-state: surface crisis resources + human review; **no 911 dispatch** ([SAFETY.md](SAFETY.md))
- Cannot act until MFA + membership `ACTIVE`.

### 7.3 Trusted Contact

- Invite → accept → see **only granted objects**.
- First-run **must show the actual grants** (`can_receive` / `can_view` and their scopes), not “you are in the circle.”
- Membership grants no visibility ([TRUSTED_CIRCLE.md](TRUSTED_CIRCLE.md), [CONSENT.md](CONSENT.md)).
- How to revoke is the **Veteran’s** action, not the contact’s. The contact’s first-run may say that the veteran can revoke; it must not offer the contact a revoke-of-grant control.

### 7.4 Service Provider

- **Not** a self-serve consumer signup in MVP unless a later spec says so.
- Organization Administrator or SUAS System Administrator records the provider.
- First-run is **acceptance of an assignment** (`ACCEPTED` on the Service Request / fulfillment path), not an app-store onboarding ([FULFILLMENT.md](FULFILLMENT.md), [DISPATCH.md](DISPATCH.md)).

---

## 8. Copy rules

Onboarding copy must not:

- Claim "HIPAA compliant", "CCPA compliant", or any compliance badge ([COMPLIANCE.md](COMPLIANCE.md))
- Imply SUAS replaces 911
- Invent partner names
- Invent safety / crisis-resource wording other than [SAFETY_COPY.md](SAFETY_COPY.md) (non-`approved` environments: admin banner only)
- Use marketing language forbidden in [README.md](README.md) ("AI-powered", "smart matching", "seamless", "intelligent", "automatically handles")
- Dark-pattern the veteran into Trusted Circle, SMS, or shares

Approved explainer copy, when written, is versioned like other templates (`DECISION_PENDING` exact text). Until then, use the standing non-goals.

---

## 9. APIs

Commands, not hidden flags. Contract conventions in [API.md](API.md). Inventory in [APIS.md](APIS.md).

| Method / path | Actor | Effect |
|---|---|---|
| `GET /admin/bootstrap/status` | SUAS-admin, MFA elevated | Checklist for **this** environment: steps, states, actors, timestamps. |
| `POST /admin/bootstrap/commands/complete-step` | SUAS-admin, MFA elevated | Persist a step; emit Audit Event. Body names the step id from §4.1. |
| `POST /veterans/me/commands/complete-enrollment` | Veteran, authenticated | Complete Pilot enrollment. Requires published QuestionnaireVersion and Pilot config. |

Do not invent a public unauthenticated signup dump. Enrollment and bootstrap are authenticated commands.

Illegal: completing enrollment without a published questionnaire → `409` or `400` with a non-leaky error. Completing a bootstrap step without MFA → `403`.

---

## 10. Events

| Event | When |
|---|---|
| Audit: bootstrap step completed | Each `complete-step` |
| Audit: bootstrap checklist closed | Environment first-run `CHECKLIST_COMPLETE` |
| Audit: environment class acknowledged | Step 2 |
| Audit: safety-copy slot set **or** acknowledged unset | Step 9 |
| `VETERAN_ENROLLED` | Veteran `complete-enrollment` ([AUTH.md](AUTH.md), [PILOT.md](PILOT.md)) |
| `CONSENT_GRANTED` | Participation / subsequent grants; not implied by enrollment alone except the documented participate-in-pilot purpose |
| `TRUSTED_CONTACT_INVITED` | Optional veteran first-run |
| Audit: fixture veteran created | TEST/STAGING only |

---

## 11. Non-goals

- Growth-hacking tours
- Dark patterns
- Auto-enrolling veterans
- Seeding PRODUCTION with demo cases
- Social login
- Claiming HIPAA (or any compliance) during onboarding copy
- Self-serve Service Provider consumer signup
- Invented partners, vendors, or legal status
- Copying checklist state across environments
- Fake-sending SMS/EMAIL when the channel is `UNAVAILABLE`

---

## 12. Testability

| Check | Pass condition |
|---|---|
| MFA gate | SUAS-admin / org-admin / responder cannot write privileged first-run steps without MFA. |
| Environment banner | Admin and responder surfaces show environment class; PRODUCTION acknowledgment is recorded. |
| Placeholder org | First org is `PARTNER_ORG_001` (or another `PARTNER_ORG_*`); no invented partner string required. |
| Questionnaire gate | `complete-enrollment` fails if no `PUBLISHED` QuestionnaireVersion. |
| Fixture label | Signal-rule fixture is labeled `UNRELEASED_FIXTURE`; not shippable as production `signal_version` policy. |
| Stale resources | Unverified / stale resources render as stale; not silently selected. |
| UNAVAILABLE channel | SMS or EMAIL without a provider is `UNAVAILABLE`; send path does not fake-send. |
| Safety copy | Non-`approved` / unset mode → admin blocked/incomplete banner; veteran red-state does not show invented crisis copy and does not imply SUAS replaces 911. |
| No prod seed | PRODUCTION has no fixture veterans / demo cases. |
| Veteran skip | First-run can complete without Trusted Circle invites. |
| Explicit NEED | Veteran can create a Service Request without a completed Check-In when they explicitly request help. |
| Trusted Contact grants | Accept first-run displays actual `can_receive` / `can_view` scopes; no “you are in the circle” as visibility. |
| Org-admin isolation | Org-admin cannot publish questionnaire / signal rules; cannot read other tenants. |
| Commands | Bootstrap and enrollment are the listed commands; no unauthenticated signup dump. |
| Enrollment proofing | `complete-enrollment` succeeds without a VA identity check, DD-214 upload, or in-person proofing step. Schema/API reject DD-214 and SSN fields ([PRIVACY.md](PRIVACY.md)). |
| UI string forbid | Onboarding copy has no `HIPAA compliant` / `CCPA compliant`. |
| Audit | Checklist close emits Audit Events; steps are readable on `GET /admin/bootstrap/status`. |

---

## 13. Links

[ADMIN.md](ADMIN.md), [AUTH.md](AUTH.md), [PILOT.md](PILOT.md), [SAFETY.md](SAFETY.md), [CONSENT.md](CONSENT.md), [CHECKINS.md](CHECKINS.md), [RESOURCES.md](RESOURCES.md), [COMPLIANCE.md](COMPLIANCE.md), [APIS.md](APIS.md), [API.md](API.md), [DEPLOYMENT.md](DEPLOYMENT.md), [DECISIONS.md](DECISIONS.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md), [TRUSTED_CIRCLE.md](TRUSTED_CIRCLE.md), [FULFILLMENT.md](FULFILLMENT.md), [PRIVACY.md](PRIVACY.md)
