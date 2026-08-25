# DATA_MODEL.md — Logical schema (SUAS v0.1)

**Related:** [DOMAIN_MODEL.md](DOMAIN_MODEL.md), [EVENT_MODEL.md](EVENT_MODEL.md), [ARCHITECTURE.md](ARCHITECTURE.md), [AUTH.md](AUTH.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [CONSENT.md](CONSENT.md), [CHECKINS.md](CHECKINS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [SETTLEMENT.md](SETTLEMENT.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md)

**Status:** `draft` / `0.1.0`. Normalized logical schema only; physical migrations remain implementation work after release. SPEC-006 remains dependency-blocked; this is cross-stage draft reconciliation, not acceptance.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).

---

## 1. Conventions

- PKs use `*_id` UUID unless a version key is textual.
- Tenant-owned rows carry `tenant_id`.
- Server-authoritative timestamps record lifecycle facts.
- Historical business meaning is never silently rewritten.
- Current projections are deterministic over durable history; insertion order alone is not authority.

---

## 2. Identity, authentication, organization

### users
`user_id`, tenant scope, nullable email/phone, status `INVITED|ACTIVE|SUSPENDED|REVOKED`, timestamps/deleted_at.

### auth_challenges
- PK `auth_challenge_id`; `tenant_id` nullable where pre-tenant enrollment applies; normalized destination/account lookup reference; challenge method; hashed/opaque secret material; status `ISSUED|CONSUMED|EXPIRED|REVOKED`; attempt counters/limits; issued/expires/consumed timestamps.
- Single-use consumption must be atomic. Secret/plain OTP/token value is never persisted in recoverable plaintext.

### sessions
- PK `session_id`; FK user; tenant/org context; opaque credential hash/reference; MFA/elevation state; issued/last-seen/expires/revoked timestamps; optional revocation/version metadata.
- Session validity/revocation is shared authoritative state across app instances; process-local cache is non-authoritative.

### organizations / organization_memberships / responder_profiles
Canonical organization, role, membership status, queue-availability fields and timestamps. Active membership/role is authoritative at mutation time.

### suas_admin_grants
The global SUAS-admin role is an auditable grant record (0.1.4), not a boolean on the user row: `admin_grant_id`, `user_id`, `granted_by`, nullable `revoked_by`, `status = ACTIVE|REVOKED`, and grant/revoke timestamps. "Who made this person a SUAS admin, and when" is answerable from history; a user is a SUAS admin iff they hold an `ACTIVE` grant. See [AUTH.md](AUTH.md) §6.

---

## 3. Questionnaire / Check-In

### questionnaire_versions / questions / answer_options
Version-bound questionnaire content; published versions immutable and atomically visible.

### check_ins
PK, veteran/questionnaire links, tenant, status `STARTED|IN_PROGRESS|COMPLETED|ABANDONED|INCOMPLETE`, lifecycle timestamps. Logical completion idempotent.

### check_in_responses
Check-In/question links, answer/free-text, timestamp; completed history preserved.

---

## 4. Support Signals

### support_signals
- PK; veteran; nullable Check-In; tenant.
- `computation_kind = PRIMARY|OVERRIDE`; stable `computation_key`; `source_type = CHECK_IN|EXPLICIT_NEED`; stable source identity.
- level `GREEN|YELLOW|ORANGE|RED`; signal/questionnaire versions; computed time; basis; override linkage/reason.
- immutable.
- Primary uniqueness by logical computation identity; explicit-need sources cannot use nullable Check-In as identity.

### effective signal projection
Deterministic and efficient projection/current pointer over durable signal history; never insertion-order-only. The deterministic rule (0.1.4, reconciled from [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §7.1): the effective signal is the most recent by `computed_at`, ties broken by `support_signal_id` descending, with an `OVERRIDE` superseding the signal it overrides. Two overrides of the same target both remain candidates and recency (then id) wins; a sequential override chain excludes each named target. This is selection, not scoring, and is independent of the D-011 threshold decision.

---

## 5. Consent / Trusted Circle

`trusted_contacts`, `consent_grants`, and immutable `consent_events` represent first-class purpose-scoped use-time authorization with tenant/grantee/version/timestamp state.

---

## 6. Cases / assignments / contact / Follow-Up

### support_cases
Case identity/veteran/tenant/status/priority/lifecycle timestamps plus nullable `current_settlement_id` convenience projection. MVP one-active-case exclusivity enforced transactionally/constraint-backed where required.

Nullable `priority_signal_level` (0.1.4) tracks the effective Support Signal level (`GREEN|YELLOW|ORANGE|RED`) as a queue-filter fact only. It is a filterable projection, not a score. `APPLY_EFFECTIVE_SIGNAL` writes `RED` from a settled effective Support Signal ([SIGNAL_SCORING.md](SIGNAL_SCORING.md) G-I-28; [SAFETY.md](SAFETY.md) §3.2). Non-RED signals do not write this field.

### case_assignments
Case/responder/status history. At most one active exclusive owner where required. The current-assignment projection (0.1.4) is the single row with `status = ACTIVE`; there is at most one `ACTIVE` assignment per Case, and it is the deterministic current owner. See [DISPATCH.md](DISPATCH.md) §6.

### case_notes / contact_attempts
Separate first-class notes/contact-log history.

### follow_ups
- PK; case; nullable request; nullable `referral_id` FK (0.1.4) when the Follow-Up is the check-back for a Referral ([REFERRALS.md](REFERRALS.md)); tenant; `due_at`; stable/monotonic `schedule_version`; `responsible_type` + `responsible_id`.
- `responsible_type` is the closed set `RESPONDER|VETERAN|ORG_ADMIN|SYSTEM` (0.1.4); `responsible_id` references the corresponding actor.
- status `SCHEDULED|DUE|COMPLETED|RESCHEDULED|OVERDUE|ESCALATED|CANCELLED`.
- `coordination_attempt_count` distinct from notification/job retries.
- `resolution_disposition = BLOCKING|CARRIED_FORWARD` while unresolved.
- due/overdue jobs compare expected schedule version before mutation.

---

## 7. Requests / providers / Fulfillment

### service_requests
Case/tenant/category/canonical status/details/timestamps. Current provider/assignment presentation derives deterministically from durable assignment/attempt history.

### service_providers / service_offers / resources
Provider/resource catalog entities with org/tenant/category/integration-mode/freshness metadata and no embedded provider credentials. Resource freshness is not live provider availability.

### provider_adapter_configurations
Tenant/provider/capability/opaque adapter id/integration mode/enabled/coverage/priority/timestamps. No secrets.

### fulfillment_attempts
Request/tenant/capability/adapter/provider/integration mode/stable external idempotency key/normalized attempt status/external ref/check/failure/timestamps. Retry same attempt reuses identity; reroute inserts new attempt.

Reconciliation sub-state (0.1.4): an attempt whose external outcome is ambiguous carries `PROVIDER_UNKNOWN` plus the reconciliation bookkeeping it needs to be resolved later — a reconciliation status, the last reconciliation check time, and the external reference used to reconcile — and must reconcile to a definite outcome before any duplicate-risk retry ([RESILIENCE.md](RESILIENCE.md); §14 rule 8).

### service_fulfillments
Request/tenant/optional FulfillmentAttempt, canonical fulfillment state/timestamps/confirmation/reason. History stays inspectable via durable row/event semantics. A Service Request has at most one `ServiceFulfillment` (0.1.4), which may have many `FulfillmentAttempt`s over its lifecycle.

---

## 8. Referrals / Settlement

### referrals
Case/request/consent/follow-up/destination/method/status/result/timestamps. Logical send uses persistent command idempotency.

### settlements
- PK `settlement_id`; FK Case; tenant; case-local `resolution_cycle`; required requested/occurred/fulfilled/unresolved summaries; responder confirmation/time; optional veteran confirmation; remaining Follow-Up references; `settled_at`.
- unique Case + resolution cycle.
- once used for `RESOLVED`, historical meaning is immutable; reopen creates a later cycle on later resolution.
- current/latest Settlement projection is deterministic; `support_cases.current_settlement_id` may cache it without replacing history.

---

## 9. Notifications

### notification_preferences
User/channel/enabled state.

### notifications
- PK `notification_id`; tenant; recipient; reason/policy key; channel; consent/system basis; template version.
- `dedupe_key`/logical-send identity when generating policy can be delivered more than once.
- optional subject reference `subject_type` + `subject_id` (0.1.4) linking a logical send to the workflow entity it was sent for; `subject_type` is one of the canonical entity-type names `SupportCase|ServiceRequest|Referral` (matching the aggregate-type naming used on Domain/Audit Events) and `subject_id` is that entity's id in the same tenant. Additive and nullable; existing sends and dedupe are unchanged.
- canonical delivery status `QUEUED|SENT|FAILED|DELIVERED|BOUNCED|UNDELIVERABLE`; attempt count/last attempt/sent timestamps.
- one row per logical send; transport attempt history lives in immutable Audit Events under current contract.
- dedupe uniqueness is scoped by tenant + recipient/channel/reason/policy as defined by the generating policy; deliberate reminder/escalation gets a new logical identity.
- the subject reference is what MVP `RESPONDER_NOTIFIED` requires to be truthfully reachable: without a delivery linked to the Service Request the QRF surface rests on `SEARCHING` ([MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2).

---

## 10. Command idempotency

### command_idempotency_records
- PK; tenant; idempotency key; command scope; canonical request fingerprint; state `RESERVED|COMPLETED|FAILED_RETRYABLE|FAILED_FINAL`; bounded result/reference; linked aggregate/event ids; created/completed/expiry metadata.
- unique logical key in scope; same key/same request replays result; same key/conflicting request fails.
- supplements domain uniqueness and FulfillmentAttempt idempotency.

---

## 11. Immutable event stores

### domain_events
Immutable event identity/type/aggregate/tenant/actor/time/schema/payload plus distinct conditional idempotency, correlation, causation, and request identifiers.

### audit_events
Immutable audit identity and request/action/target metadata; event/audit identity remains distinct from command idempotency.

### outbox/equivalent
Allowed physical mechanism for replay-safe required event publication; not a business entity.

---

## 12. Pilot / feedback

Canonical Pilot, PilotEnrollment, Feedback entities; pilot size is operating scope, not architecture ceiling.

---

## 13. Required access paths / constraints

Implementation must efficiently/atomically support:
- user/session/challenge lookup, single-use challenge consumption, session revocation across instances;
- tenant + status Case/Request/Follow-Up/attempt queries;
- Support Signal computation uniqueness/current projection;
- one-active Case/assignment winner constraints;
- Settlement Case+cycle/current projection;
- Follow-Up due/status/schedule-version pickup;
- provider reconciliation and FulfillmentAttempt idempotency;
- Notification logical-send dedupe and delivery worker pickup;
- command idempotency lookup;
- event/audit tenant/aggregate/time/correlation/idempotency queries.

Exact SQL index/constraint syntax is implementation-specific but must prove these invariants under concurrency and load.

---

## 14. Integrity rules

1. Tenant consistency across related domain rows.
2. Published questionnaire immutable/atomically visible.
3. One auth challenge consumed at most once.
4. Session revoke/membership revoke observed across horizontally scaled instances.
5. Primary Support Signal unique by logical computation identity; effective projection deterministic.
6. One-active Case/assignment winner where required.
7. Provider state never silently becomes Request/Fulfillment state.
8. `PROVIDER_UNKNOWN` reconciles before duplicate-risk retry.
9. Provider/Referral disclosure requires use-time consent/minimum necessary projection.
10. Follow-Up stale schedule jobs cannot mutate newer state.
11. Notification retries do not increment Follow-Up coordination count.
12. Duplicate generating event/job maps to one logical Notification when dedupe semantics match.
13. Case reopen preserves prior Settlement and later resolution creates later cycle.
14. Required Domain Event publication cannot be permanently lost after commit.
15. Command idempotency survives restart/horizontal instances and detects conflicting reuse.
16. Provider secrets never live in domain tables.

---

## 15. Non-goals

Physical migration syntax, vendor schemas, provider secrets, payment/billing columns, premature sharding, raw webhook payload retention as business data, event IDs as command-idempotency substitutes, process-local-only session/idempotency truth, insertion-order current projections, or one mutable Settlement row that destroys resolution history.
