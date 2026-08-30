# AUTH.md — Authentication and session authorization (SUAS v0.1)

**Related:** [SECURITY.md](SECURITY.md), [ADMIN.md](ADMIN.md), [PRODUCT.md](PRODUCT.md), [API.md](API.md), [DOMAIN_MODEL.md](DOMAIN_MODEL.md), [ONBOARDING.md](ONBOARDING.md), [APIS.md](APIS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md)

**Actors:** Veteran, Responder, Organization Administrator, SUAS System Administrator, Trusted Contact (if enrolled), Service Provider user.

**Status:** `draft` / `0.1.0`. SPEC-007 is dependency-blocked; this is preflight reconciliation.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).

---

## 1. Purpose

Identify users, issue/revoke sessions, enforce MFA where required, and recover access without weakening least privilege.

Authentication is not authorization. Authorization remains role + tenant + row + consent/system basis.

---

## 2. Veteran authentication

Veterans use passwordless methods:

| Method | MVP |
|---|---|
| Magic link (email) | supported where email provider configured |
| Email OTP | supported where email provider configured |
| Phone OTP | supported where phone + SMS provider configured |

At least one usable enrolled channel is required for MVP enrollment under the D-016 `DECIDED` v0.1 default (self-attest + working passwordless contact; no VA/DD-214/in-person proofing). SMS provider selection remains D-003; EMAIL uses Resend under D-004.

No Veteran password or social login unless a later accepted spec adds it.

---

## 3. Challenge contract

A magic-link/OTP challenge is:

- single-use;
- time-bounded; exact TTL remains an explicit documented constant (`DECISION_PENDING`, with any recommendation labeled `INFERRED`);
- stored hashed/opaque, never plaintext secret material;
- rate-limited by address/account and network signal where appropriate;
- consumed atomically.

Concurrency rule: two simultaneous verifies of one challenge produce at most one successful consumption/session-establishment effect. A stale/replayed verify fails safely.

Challenge issuance/verification state and rate-limit counters that protect correctness/abuse controls must be shared across horizontally scaled app instances or use an equivalent distributed/persistent mechanism. Process-local counters are not authoritative production controls.

---

## 4. Responder / administrator authentication

Responders, Org Admins, and SUAS Admins:

1. identify through an accepted passwordless/email path unless a later spec adds another method;
2. complete MFA before privileged session elevation;
3. use an MFA factor type selected later; no vendor lock in the domain contract;
4. recovery cannot silently bypass MFA/least privilege.

SUAS-admin first-run MFA must complete before other privileged bootstrap writes.

---

## 5. Session model

Sessions are server-revocable or equivalently revocable opaque credentials.

Required logical state includes:
- `session_id`/opaque credential identity;
- `user_id`;
- tenant/org context as applicable;
- issued/last-seen/expiry metadata;
- privilege/MFA elevation state where relevant;
- revocation state/version.

### Horizontal-scaling invariant

Any healthy app instance must observe effective session revocation and membership/user status changes within the accepted security window. Session validity cannot depend on the process that originally issued the session.

A process-local cache may accelerate reads only if revocation correctness is preserved.

### Invalidation triggers

At minimum:
- logout;
- user `SUSPENDED`/`REVOKED`;
- relevant membership revoke;
- MFA/recovery reset where required;
- admin force logout;
- idle/absolute timeout according to accepted constants.

A revoked user cannot refresh or act. In-flight authorization after revocation must re-evaluate authoritative user/membership/session state rather than trusting stale client claims.

---

## 6. Organization membership / role inputs

- `User.status = ACTIVE` required.
- Org actions require active `OrganizationMembership` with the needed role.
- Roles: `RESPONDER`, `ORG_ADMIN`, `SERVICE_PROVIDER_USER`; global `SUAS_ADMIN` is distinct.
- Org-admin cannot become SUAS-admin by self-service role mutation.
- The global `SUAS_ADMIN` role is represented as an auditable grant record (0.1.4), not a boolean on the user row: a user holds the role iff they have an `ACTIVE` `suas_admin_grants` entry, and grant/revoke record `granted_by`/`revoked_by` and timestamps so "who made this person a SUAS admin, and when" is answerable ([DATA_MODEL.md](DATA_MODEL.md) §2).
- Tenant/org context is server-derived and audited for privileged cross-scope actions.

---

## 7. Recovery

| Actor | Contract boundary |
|---|---|
| Veteran | enrolled-channel recovery; lost-all-channel proofing process remains `DECISION_PENDING` and audited |
| Responder / Org-admin | privileged reset with MFA re-enrollment and audit |
| SUAS-admin | dual-control/break-glass details `DECISION_PENDING`; audit + post-review required |

Recovery is not enrollment and cannot create an undocumented identity-proofing bypass.

---

## 8. Audit / events

Audit challenge issuance/verification outcome, login success/fail, MFA changes, logout/session invalidation, recovery, user/membership revoke, and privileged elevation.

`VETERAN_ENROLLED` is an enrollment Domain Event, not a login event.

---

## 9. Provider-neutral delivery

External challenge delivery uses capability ports from [APIS.md](APIS.md). Provider delivery acknowledgement does not itself authenticate the user; only SUAS challenge verification settles authentication.

If a delivery provider is unavailable, that channel is unavailable. Do not fake success.

EMAIL delivery uses Resend exclusively under D-004 and [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md). Provider acceptance does not authenticate the user; only successful atomic challenge verification does.

### 9.1 Browser passwordless transport

The HTML `/app` surface may issue an `EMAIL_OTP` challenge for an already-enrolled address and exchange a valid code for the same opaque, server-revocable session used by the API.

- The deployment resolves tenant scope from `SUAS_BROWSER_TENANT_ID`; the browser does not submit or choose tenant authority.
- Challenge issuance returns the same public confirmation for enrolled and unenrolled destinations. An unenrolled destination receives no message.
- Verification sets the session credential only in a `Secure`, `HttpOnly`, `SameSite=Strict` cookie scoped to `/app`.
- `/api/v0` and native clients continue to use `Authorization: Bearer`; they do not use the browser cookie.
- Cookie-authenticated state-changing `/app` requests reject cross-origin submissions.
- Browser logout revokes the server session and clears the cookie.
- This path is sign-in, not enrollment. It creates no User, role, membership, PilotEnrollment, Veteran record, or Consent Grant.

---

## 10. Non-goals

- Veteran passwords by default;
- social login in MVP;
- shared responder accounts;
- long-lived unrevocable bearer credentials;
- process-local-only session revocation/rate-limit truth;
- impersonation without a later accepted break-glass contract.

---

## 11. Testability

AUTH tests include:
- passwordless challenge/verify on configured channel;
- same challenge verified concurrently → one success maximum;
- challenge replay after consume fails;
- responder/admin cannot elevate without MFA;
- user/membership revoke is observed across multiple app instances;
- stale cached session cannot act after authoritative revoke;
- distributed/shared rate limit rejects abuse across instance rotation;
- org-admin cannot operate as another org or SUAS-admin;
- enrollment does not require VA API/DD-214/in-person proofing under D-016 MVP default.
