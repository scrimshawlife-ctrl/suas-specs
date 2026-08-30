# ADMIN_SURFACE_DESIGN.md — Web administration surface

**Lifecycle:** `draft` / implementation plan. Not a version bump, release manifest, readiness advance, or production-operating authority.

**Authority boundary:** [ADMIN.md](ADMIN.md), [AUTH.md](AUTH.md), [API.md](API.md), [ONBOARDING.md](ONBOARDING.md), and the current release manifest remain authoritative. This file fully specifies the intended web experience and records API work that must return to the canonical contract before implementation. Where this file conflicts with a released contract, the released contract wins.

**Related:** [PRODUCT.md](PRODUCT.md), [MVP_REFERENCE.md](MVP_REFERENCE.md), [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [OPERATIONS.md](OPERATIONS.md), [TESTING.md](TESTING.md), [RESOURCES.md](RESOURCES.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md)

---

## 1. Finding and scope

The released stack defines admin actors, authority boundaries, MFA, audit, bootstrap, a minimum admin API, provider configuration, and operational reads. It does **not** define a coherent web information architecture, page-level behavior, interaction states, or a complete API for every allowed admin responsibility.

The web implementation observed at `suas` commit `d98eb2c70822ce7901465e19cd3c1e443869865e` contains `/app/admin` as a partial overview with provider configuration, capability/readiness summaries, and open decisions. That is a valid module, not the complete administration surface described by [ADMIN.md](ADMIN.md).

This design covers two separate workspaces:

1. **SUAS Admin** — global system operations and explicitly audited cross-tenant administration.
2. **Organization Admin** — one-organization membership, coverage, resource, routing, and operational management.

It does not create a native-admin requirement. Native responder/admin experiences remain governed by [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §9; the complete administration console is a web surface.

### 1.1 Epistemic labels

| Label | Meaning |
|---|---|
| `RELEASED` | Required by an owner-released canonical contract. |
| `OBSERVED` | Present in the cited implementation revision; not authority by itself. |
| `PROPOSED` | UX design in this draft. |
| `API_GAP` | UI must not ship an enabled control until an authoritative `/api/v0` contract exists. |
| `DECISION_BLOCKED` | A named open decision prevents the action from becoming operational. |

---

## 2. Product principles

1. **Role clarity over convenience.** `ORG_ADMIN` and `SUAS_ADMIN` are distinct. A person holding both chooses an explicit workspace; permissions are never inferred from the page they reached.
2. **Scope is always visible.** Environment class, workspace role, and current organization or global scope remain visible in the shell and confirmations.
3. **Read before mutate.** Overview pages lead with state, freshness, consequences, and prerequisites. They do not present a grid of unlabeled destructive controls.
4. **Commands, not hidden flags.** Mutations use the command semantics and idempotency rules in [API.md](API.md). A client-side toggle is never authority.
5. **No false readiness.** Missing, unavailable, blocked, degraded, stale, and decision-pending are distinct from configured or healthy.
6. **Minimum necessary data.** Lists default to identifiers and operational summaries. Veteran content and sensitive cross-tenant data do not appear in overview cards.
7. **History is durable.** Published artifacts, Audit Events, prior configuration, and Fulfillment Attempts are not edited away.
8. **Recovery remains explicit.** There is no silent impersonation, hidden tenant switch, ordinary data export, or bypass around MFA/consent.

---

## 3. Authorization and workspace matrix

Every route requires an authenticated, MFA-elevated privileged session. The server re-evaluates active user, grant/membership, scope, and row authority for every read and mutation.

| Capability | Organization Admin | SUAS Admin |
|---|---:|---:|
| View own organization operational overview | Allow | Allow through explicit audited org scope |
| Manage own organization memberships | Allow | Allow through explicit audited org scope |
| Set responder `active_for_queue` in own organization | Allow | Allow through explicit audited org scope |
| Manage/verify own organization Resources and Service Offers | Allow | Allow through explicit audited org scope |
| View own organization queue health | Allow | Allow through explicit audited org scope |
| Configure delegated org routing for globally enabled adapters | Conditional | Allow |
| Create/suspend/archive organizations | Deny | Allow |
| Administer memberships across organizations | Deny | Allow |
| Manage user status/session recovery/force logout | Deny; organization membership actions only | Allow |
| Publish questionnaire/signal/consent/notification artifacts | Deny | Allow where released prerequisites are satisfied |
| Configure provider adapters globally | Deny | Allow for accepted capabilities only |
| View global platform operations | Deny | Allow |
| View global Audit Events | Deny | Allow, bounded and audited where sensitive |
| Grant/revoke `SUAS_ADMIN` | Deny | `API_GAP`; dual-control/break-glass policy is unresolved |
| Routine Case ownership or responder work | Deny in admin surface | Deny in admin surface |
| Break-glass Case read/repair | Deny unless later accepted policy says otherwise | `DECISION_BLOCKED`; no enabled UI now |
| View/write provider secret values | Deny | Deny |

An authorization denial must not disclose another tenant's existence or data. Navigation omission is a convenience only; server authorization remains mandatory.

---

## 4. Information architecture

### 4.1 Stable web routes

These are proposed HTML routes under the existing `/app` browser surface. They do not create a second product API.

| Route | Workspace | Page |
|---|---|---|
| `/app/admin` | SUAS Admin | Overview and readiness |
| `/app/admin/organizations` | SUAS Admin | Organizations |
| `/app/admin/access` | SUAS Admin | Users, memberships, and sessions |
| `/app/admin/artifacts` | SUAS Admin | Published configuration artifacts |
| `/app/admin/providers` | SUAS Admin | Provider adapters and routing |
| `/app/admin/operations` | SUAS Admin | Platform operational state |
| `/app/admin/audit` | SUAS Admin | Audit-event explorer |
| `/app/org-admin` | Organization Admin | Organization overview |
| `/app/org-admin/people` | Organization Admin | Memberships and responder coverage |
| `/app/org-admin/resources` | Organization Admin | Resources and Service Offers |
| `/app/org-admin/operations` | Organization Admin | Queue and operational health |
| `/app/org-admin/providers` | Organization Admin | Delegated routing, when allowed |

Resource detail may use an opaque identifier appended to the collection route. IDs are never sequential or tenant-disclosing. Query parameters may carry bounded filters, not authorization scope.

### 4.2 Global shell

Every page contains, in reading and focus order:

1. skip link;
2. product and workspace name;
3. environment banner (`LOCAL`, `TEST`, `STAGING`, or `PRODUCTION`);
4. current scope chip (`Global SUAS` or organization display name plus opaque identifier);
5. primary navigation allowed for the current workspace;
6. session/elevation state and sign-out;
7. page title, purpose, freshness, and health summary;
8. page content;
9. build/spec provenance without secrets or veteran PII.

Production uses a persistent, non-color-only environment label. The page never permits the browser to choose tenant authority. A scope change is server-authorized, explicit, and reflected in the URL/breadcrumb before data loads.

### 4.3 Shared page states

Every module specifies and tests:

- loading with a named region and no fake data;
- empty with an explanation and only authorized next actions;
- partial/degraded with stale or unavailable sections labeled independently;
- permission denied without resource-existence leakage;
- expired/revoked session with no retained sensitive content;
- validation error attached to the field and summarized at the top;
- stale-state/idempotency conflict with the authoritative current state;
- server/dependency failure with a safe retry where applicable;
- success with the resulting state and Audit Event reference when returned.

Optimistic UI may show progress but must not claim a command succeeded before the authoritative response.

---

## 5. SUAS Admin page contracts

### 5.1 Overview and readiness

Purpose: answer “what environment am I operating, what is blocked, and where is attention required?” without exposing sensitive records.

Sections, in priority order:

1. **Environment and bootstrap:** persisted checklist state, required incomplete steps, specification/manifest/app provenance, and explicit safety-copy status.
2. **Critical degradation:** audit append, durable jobs, database/app readiness, notification delivery, provider/manual paths, and reconciliation backlog.
3. **Capability matrix:** each capability as `AVAILABLE`, `DEGRADED`, `UNAVAILABLE`, `BLOCKED`, or `DECISION_PENDING`, with basis and last check.
4. **Operational work:** bounded counts and oldest age for actionable failures; no clinical/outcome ranking.
5. **Configuration changes:** recent privileged changes with actor, scope, time, result, and link to the Audit Event.

The page must not aggregate a “green” overall status if any hard bootstrap prerequisite is incomplete. A readiness label is descriptive evidence, never pilot or production authorization.

### 5.2 Organizations

List fields: display name, opaque organization ID, lifecycle state, membership counts by role, responders active for queue, resource freshness summary, provider/manual capability summary, and last privileged change.

Filters: lifecycle state and capability degradation. Search matches organization name or exact opaque ID. Results use `cursor` + `limit` and never reveal hidden organizations to an unauthorized actor.

Detail sections:

- profile and lifecycle;
- memberships and responder availability;
- Resources/Service Offers freshness;
- delegated routing;
- queue/operational indicators;
- recent organization-scoped Audit Events.

Create, suspend, and archive are separate commands. Suspend/archive confirmation names the organization, environment, consequences, and affected capabilities. Archive is not delete. Re-enable behavior requires a canonical command before the UI exposes it.

**Status:** authority is `RELEASED`; complete read/write API is `API_GAP`.

### 5.3 Access: users, memberships, and sessions

The default view is a bounded user/membership directory. It shows minimum operational identity: display label, masked destination where needed, user status, organization memberships/roles, SUAS-admin grant presence, MFA enrollment/elevation eligibility, active-session count, and last access change. It does not show challenge secrets, recovery factors, session credentials, or authentication provider payloads.

Allowed flows:

- invite or add an organization membership;
- suspend/revoke a membership;
- suspend/revoke a user where policy permits;
- force logout/revoke sessions;
- start a documented recovery flow without bypassing MFA;
- inspect grant history.

Every confirmation distinguishes user status, membership status, session revocation, and admin grant status; changing one must not silently change another. Self-revocation and last-admin protections require an accepted policy. Silent impersonation is absent.

**Status:** authority is `RELEASED`; complete read/write API and last-admin/dual-control rules are `API_GAP` or `DECISION_BLOCKED`.

### 5.4 Published artifacts

One index contains four independently filterable collections:

| Artifact | Allowed lifecycle | Required display |
|---|---|---|
| Questionnaire version | draft → published → superseded | version, state, author, created/published time, compatibility/basis |
| Signal-rule version | accepted artifact → published → superseded | version, accepted decision/release basis, state, publisher |
| Consent template | draft → published → superseded | purpose/scope, version, locale, effective time, publisher |
| Notification template | draft → published → superseded | channel, purpose, locale, version, state; no safety logic |

Published content is read-only. “Create next version” copies allowed structure into a new draft; it never edits the prior row. Publish opens a review screen showing the immutable diff, dependencies, environment/scope, and warnings. The final command requires MFA elevation, an idempotency key, and explicit confirmation. Signal rules cannot publish without accepted artifacts and cannot bypass D-011.

If content preview could include unsafe markup, render it encoded/sanitized and in a constrained preview. No raw HTML execution.

**Status:** questionnaire publish has a `RELEASED` minimum API. The remaining collections and draft/read/supersede operations are `API_GAP`; consent publication is explicitly missing from the current implementation contract.

### 5.5 Provider adapters and routing

The existing provider overview becomes this dedicated page.

Adapter list fields are limited to the projection authorized by [ADMIN.md](ADMIN.md) §3: opaque adapter ID, capability, integration mode, tenant/org scope, enabled state, coverage/routing priority, normalized health/circuit/degraded state, last health/reconciliation metadata, credential presence (`CONFIGURED|MISSING`), and shelter capability state.

Flows:

- enable an accepted adapter for an allowed scope;
- disable without deleting or rewriting FulfillmentAttempt history;
- set bounded coverage and routing priority;
- inspect normalized health and reconciliation backlog;
- confirm Manual Adapter coverage/fallback;
- show a blocking prerequisite when decision, credentials, payment architecture, or environment policy is unsatisfied.

The page never displays or accepts secret values, raw provider payloads, payment-card data, or provider-specific state as canonical SUAS state. `ManualShelterAdapter` remains visible and mandatory. Disable confirmation explains current routing impact and open-work handling; it does not promise cancellation of provider-side effects.

**Status:** provider projection and restrictions are `RELEASED`; the observed web/API module is partial and must be reconciled with the canonical inventory.

### 5.6 Platform operations

This is a read-first operational surface, not a generic metrics dashboard.

| Module | Required data |
|---|---|
| Durable work | queue depth, oldest age, failed/dead-letter/quarantined counts, freshness |
| Notifications | failure counts by channel/reason class, backlog, provider availability; no message bodies by default |
| Providers | normalized circuit/health, rate-limit/degradation, reconciliation backlog, manual fallback |
| Audit/events | append health, publication lag/backlog, no mutable log controls |
| Restore/drills | last test time, environment, result, evidence reference; no unsupported RTO/RPO claim |
| Load/backpressure | tenant-scoped saturation/backpressure indicators without outcome scoring |

Actions such as replay, reconcile, kill switch, or restore are not implied by the read surface. Each requires a separately released command, authorization, idempotency, consequence review, and audit contract. Until then, link to the owned runbook without an enabled button.

**Status:** read authority is `RELEASED`; exact API projections and action commands are `API_GAP`.

### 5.7 Audit explorer

Default order is newest first. Filters are time range, actor, action/event class, scope, resource type/opaque ID, and result. Lists are cursor-paginated with a maximum page size from [API.md](API.md). Each row shows event identity, actor, effective role, environment, tenant/org scope, action, target reference, outcome, and recorded time.

Detail shows structured redacted metadata and correlation/idempotency references where authorized. It never exposes credentials, raw notification destinations beyond policy, or unrestricted before/after veteran content. There is no edit or delete action.

Ordinary CSV/data export is absent because sensitive aggregate reporting and production-to-nonproduction export are not authorized. An accepted later export contract must define columns, purpose, scope, audit, delivery, expiry, and environment boundary.

**Status:** bounded `GET /admin/audit-events` is `RELEASED`; exact filters/projection are `API_GAP`.

### 5.8 Case/request incident access

No general case browser appears in the SUAS Admin navigation. Admins use responder workflows for routine coordination only when separately granted and acting in that role.

A future break-glass/repair surface must not be implemented until the canonical contract defines reason codes, scope, time bound, approvals/dual control, allowed fields/actions, notification/post-review, audit detail, and revocation. Until then the UI presents no control and no claim that access exists.

**Status:** `DECISION_BLOCKED`.

---

## 6. Organization Admin page contracts

### 6.1 Organization overview

Shows one server-derived organization only: environment, organization identity, first-run/checklist state, responders active for queue, current queue depth/oldest age, overdue follow-up summary, resource freshness, delegated capability/manual-path state, and recent scoped changes.

It never includes cross-organization comparison, global platform controls, global artifact publication, or sensitive outcome analytics.

### 6.2 People and responder coverage

List fields: member display label, role, membership status, `active_for_queue` where applicable, MFA readiness necessary to act, and last membership/availability change. Destinations are masked unless a support task authorizes more.

Flows:

- invite/add a member using an accepted identity path;
- suspend/revoke membership;
- set responder `active_for_queue` through an explicit command;
- view the operational effect on coverage without claiming 24/7 availability.

Bulk role/status changes are excluded initially. The page cannot mutate global user status, other organizations, or `SUAS_ADMIN` grants.

### 6.3 Resources and Service Offers

The page provides bounded search/filter by category, freshness, verification state, and coverage. Rows show ownership, capability/category, verified time/by, freshness/expiry, coverage, availability truth, and allowed contact/action summary.

Create/edit remains scoped to organization-owned records. Verify is an explicit command with verifier and time. Stale/unverified entries are visibly distinct and are not silently selected. Destructive delete is absent unless the domain contract defines historical and referral effects; archive/unpublish may be proposed through a later command.

### 6.4 Organization operations

Shows queue depth/oldest age, responders active for queue, overdue follow-ups, failed/unknown fulfillment requiring human attention, resource freshness, and notification/provider degradation in the organization. Counts link to existing authorized responder workflows where available; the admin page does not become a second Case workflow.

No responder score, rating, clinical outcome, or fabricated performance metric appears without an accepted definition and data basis.

### 6.5 Delegated provider routing

This page exists only when accepted policy delegates the capability and the underlying adapter is already enabled for the organization. Org Admin may select only from allowed adapter/manual routes and bounded coverage/priority fields. Global enablement, credentials, raw health payloads, and provider onboarding remain unavailable.

**Status for §6:** role boundaries are `RELEASED`; most page reads and commands are `API_GAP`.

---

## 7. Interaction contract for privileged changes

Every privileged write follows this sequence:

1. **Eligibility:** server returns current state, actor authority, MFA elevation, prerequisites, and allowed command.
2. **Edit:** client collects only contract fields and performs local format validation without inventing authority.
3. **Review:** page shows actor role, environment, scope, target, current state, proposed state, consequences, and irreversible effects.
4. **Confirm:** explicit action label names the mutation; risky actions require typed target confirmation only where it materially prevents scope mistakes.
5. **Execute:** send the canonical command with a stable `Idempotency-Key` across safe retries.
6. **Settle:** replace pending state with the authoritative response. Show Audit Event reference when returned.
7. **Conflict:** on `409`, preserve the attempted input, show current authoritative state, and require review before a new key/request.

Disabled controls must pair with a textual reason such as `MFA required`, `Decision D-019 pending`, `Credentials missing`, `Adapter not globally enabled`, or `API contract unavailable`. A tooltip alone is insufficient.

---

## 8. Data, privacy, and security contract

- The browser receives only the page's minimum projection; authorization is not implemented by hiding DOM elements.
- Sensitive values do not enter HTML, hydration payloads, logs, URLs, analytics, or client-visible errors.
- All rendered user/provider content is untrusted and encoded.
- State-changing browser requests retain the released `Secure`, `HttpOnly`, `SameSite=Strict` cookie and cross-origin rejection contract in [AUTH.md](AUTH.md) §9.1.
- Cache headers prevent shared/intermediary caching of authenticated admin pages and data.
- Browser history and page titles avoid veteran content and notification destinations.
- Focus returns to the changed row/summary after a command; live announcements contain no excess sensitive detail.
- Session expiry clears sensitive rendered state as far as the browser implementation permits and returns to authentication without replaying a mutation automatically.
- Audit identifiers may be copied; secrets, session tokens, OTP/MFA material, and raw provider payloads may not.
- Telemetry records route/module, outcome class, latency, and correlation identifiers only when permitted; it excludes form content and veteran/provider secret data.

---

## 9. Visual and responsive design

The admin console inherits the SUAS web visual language and the recognizable high-privilege distinction allowed by [MVP_REFERENCE.md](MVP_REFERENCE.md) §7.5. Terminology is `SUAS Admin` or `Organization Admin`, never “God Mode.”

Visual hierarchy:

- operational urgency uses explicit text/icon/state, never color alone;
- environment and scope remain more prominent than decorative branding;
- one primary action per module or review step;
- dense data uses readable rows/tables at wide viewports and labeled stacked records at narrow viewports;
- status chips use the canonical state text, not vendor-colored approximations;
- destructive or high-impact actions are visually separated from routine actions;
- empty space and section grouping preserve the action-first character of the reference without hiding operational detail.

Responsive behavior:

- at wide viewports, persistent navigation and bounded tables are allowed;
- below the table's readable width, each record becomes a labeled card/definition list; required columns are not silently dropped;
- navigation collapses to an accessible disclosure without covering environment/scope;
- filters move into a labeled drawer/disclosure and retain an always-visible active-filter summary;
- no horizontal page scroll at 320 CSS px except an intentionally scrollable data region with an accessible label;
- touch targets, zoom/reflow, focus visibility, reduced motion, keyboard operation, and screen-reader names meet WCAG 2.2 AA.

---

## 10. API gap ledger

The following are required before the corresponding enabled UI ships. Exact resources, bodies, projections, errors, audit events, and idempotency rules must be added to [API.md](API.md)/[APIS.md](APIS.md) and released; this draft does not invent them as authority.

| Gap | Needed surface | Minimum contract to resolve |
|---|---|---|
| A-01 | Organization directory/lifecycle | bounded reads; create/suspend/archive commands; scope and conflict rules |
| A-02 | User/session administration | bounded user/status/session projection; force-logout/recovery commands; masking and audit |
| A-03 | Membership and responder availability | invite/add/suspend/revoke and `active_for_queue` commands; last-admin/concurrency rules |
| A-04 | Resource/Service Offer administration | bounded admin reads and create/update/verify/archive semantics with freshness/history |
| A-05 | Artifact management | reads plus draft/publish/supersede for all four artifact types; immutable diff and dependency errors |
| A-06 | Consent template publication | versioned template contract and bootstrap hard-gate integration |
| A-07 | Provider administration | reconcile implemented adapter endpoints with the canonical inventory and routing/health projection |
| A-08 | Operational reads/actions | bounded projections and freshness; separately authorized replay/reconcile/kill-switch commands |
| A-09 | Audit explorer | exact redacted projection, allowed filters, sensitive-read audit, and cursor behavior |
| A-10 | Org-admin delegated routing | delegation policy, eligible adapter projection, and bounded command |
| A-11 | Break-glass/repair | owner decision covering approvals, reason, scope, expiry, post-review, and audit |
| A-12 | SUAS-admin grant governance | dual-control/last-admin/grant/revoke contract; self-grant remains prohibited |

Until a gap closes, the web may show truthful read-only absence/readiness information but must not fake success, mutate through undocumented flags, or call an implementation-only endpoint as if it were released authority.

---

## 11. Delivery slices

Implementation proceeds in dependency order; a later slice does not block safe completion of an earlier one.

1. **Shell and overview:** environment/scope, MFA/session state, bootstrap/readiness, navigation, common states.
2. **Provider module reconciliation:** move the observed provider controls into the dedicated contract, preserve manual fallback, close projection/endpoint drift.
3. **Organization Admin core:** people/coverage, Resources/Service Offers, scoped operations after A-03/A-04 APIs release.
4. **SUAS access and organizations:** lifecycle, membership, session revoke/recovery after A-01/A-02 release.
5. **Artifacts:** questionnaire first, then consent/signal/notification only as their APIs release.
6. **Operations and audit:** bounded read projections, then separately accepted action commands.
7. **Break-glass/grant governance:** only after the named decisions and contracts close.

Each slice includes authorization, audit, accessibility, responsive, empty/degraded/error states, deterministic fixtures, and browser tests. A placeholder navigation item is omitted rather than linked to a blank page.

---

## 12. Conformance and acceptance fixtures

Minimum deterministic fixtures:

1. SUAS Admin in TEST with incomplete bootstrap, unavailable SMS, configured email, one degraded provider, and Manual Adapter available.
2. SUAS Admin in STAGING with two organizations, one suspended membership, and no cross-tenant veteran content in overview responses.
3. Organization Admin with one organization, mixed responder availability, stale resources, and delegated routing absent.
4. Organization Admin with delegated routing present but adapter globally disabled; control is blocked with reason.
5. Published questionnaire and draft successor; published version is immutable.
6. Missing consent-template publication contract; no enabled publish control.
7. Provider credential `CONFIGURED` with no secret value anywhere in HTML/API/log fixture.
8. Concurrent/stale privileged mutation returning `409`; no partial state and no automatic new command.
9. Replayed command with the same key and payload returns one logical mutation/Audit Event effect.
10. Revoked membership/session observed before a subsequent action across app instances.
11. Cross-tenant guessed identifier denied without existence leakage.
12. 320 px, 200% zoom, keyboard-only, screen-reader landmarks/names, forced colors, and reduced motion.

Required automated evidence:

- role × route × action authorization matrix;
- MFA gate on every privileged write and sensitive read where specified;
- successful write → Audit Event; rejected write → no partial domain mutation;
- pagination bounds and stable cursor behavior;
- redaction snapshots for HTML, JSON, errors, logs, and telemetry;
- visual-regression fixtures for SUAS Admin overview, Provider configuration, Organization Admin overview, and one narrow viewport per page family;
- axe-equivalent automated checks plus manual keyboard/screen-reader review;
- build/spec/environment provenance visible and correct;
- no production or pilot readiness claim inferred from component health.

The admin surface is not conformant merely because `/app/admin` returns `200`. It is conformant per delivered slice only when the applicable page, API, authorization, audit, state, privacy, accessibility, and fixture contracts above all pass.

---

## 13. Explicit non-goals

- A second admin API outside `/api/v0`.
- Native parity with the complete web console.
- Clinical charting, diagnosis, billing, or Medi-Cal administration.
- Routine responder Case ownership inside admin pages.
- Silent impersonation or an undocumented “view as” mode.
- Raw secret entry/read, provider booking console behavior, or payment-card handling.
- Unbounded exports, sensitive aggregate reporting, or production-to-nonproduction data movement.
- Feature flags that redefine released domain semantics.
- Fabricated responder ratings, outcomes, readiness, staffing, provider success, or 24/7 availability.

---

## 14. Owner review needed before release

Owner review must decide whether this page/interaction design becomes implementation authority and must separately close or schedule A-01 through A-12. Accepting the UX design alone does not close authentication factor, break-glass, dual-control, staffing, provider, reporting, or production-readiness decisions.
