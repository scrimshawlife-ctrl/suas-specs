# ARCHITECTURE.md — Scalable modular monolith

**Related:** [PRODUCT.md](PRODUCT.md), [MVP_REFERENCE.md](MVP_REFERENCE.md), [DOMAIN_MODEL.md](DOMAIN_MODEL.md), [DATA_MODEL.md](DATA_MODEL.md), [EVENT_MODEL.md](EVENT_MODEL.md), [API.md](API.md), [APIS.md](APIS.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md), [DEPLOYMENT.md](DEPLOYMENT.md), [SAFETY.md](SAFETY.md), [SETTLEMENT.md](SETTLEMENT.md)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md). The former inline `draft` / `0.1.0` marker was stale; the manifest governs ([VERSIONING.md](VERSIONING.md) §1). Unsettled cloud/queue/cache/provider choices remain `DECISION_PENDING`.

---

## 1. Purpose

SUAS uses a **scalable modular monolith** for the controlled pilot and early growth. Scale first through stateless application instances, PostgreSQL, durable jobs, provider-neutral capability ports, bounded APIs, backpressure, and observability.

Pilot scope may be small. Architectural ceilings should not be. Microservices require measured need and a later released architecture change.

---

## 2. High-level shape

```text
Veteran / Responder / Admin clients
              |
              v
      Stateless SUAS API tier
      (modular monolith)
              |
       +------+----------------+
       |                       |
       v                       v
   PostgreSQL              Durable Jobs
       |                       |
       |                       v
       |                    Workers
       |                       |
       |       +---------------+----------------+
       |       |        |       |       |        |
       |       v        v       v       v        v
       |      SMS     Email   Provider  Follow-  Signal/
       |                      Adapters   Up       Reconcile
       |
       v
 Domain + Audit Events
```

The referenced MVP remains the visual/interaction authority subject to [MVP_REFERENCE.md](MVP_REFERENCE.md).

---

## 3. Architecture invariants

1. One logical deployable application architecture; many stateless instances may run.
2. One logical PostgreSQL system of record per environment unless a later released spec changes topology.
3. Module boundaries are code/data-ownership/authorization boundaries, not network boundaries.
4. Correctness-critical state is never process-local truth.
5. Production-critical async work survives process/worker restart.
6. External services use capability ports; vendor SDKs/payloads stay adapter-local.
7. Manual service coordination is first-class.
8. Contested state transitions have deterministic atomic winners.
9. Externally consequential retries are idempotent.
10. Growing API collections are bounded/paginated.
11. Tenant isolation survives horizontal scaling, jobs, callbacks, caches, and reporting.
12. Historical business facts are preserved; current projections are deterministic, not insertion-order accidents.
13. Service extraction requires measured need + released spec + migration/rollback plan.

---

## 4. Clients

| Client | Users | Primary role |
|---|---|---|
| Veteran PWA | Veteran | Check-In, consent, support requests/status, trusted circle, fulfillment confirmation |
| Responder console | Responder / Org Admin | Coordination/QRF console, not an EHR |
| Admin console | SUAS Admin / scoped Org Admin | Governance and operations |
| Native mobile client | Veteran (Responder/Admin conditionally) | Installed client of the identified opt-in platform; consumes `/api/v0` as an ordinary authenticated client and holds no provider credential ([MOBILE_SURFACE.md](MOBILE_SURFACE.md), D-033) |

All production clients conform to [MVP_REFERENCE.md](MVP_REFERENCE.md).

A client is a consumer of the released product API. Adding one does not add a domain concept, state, event, capability, or API selector, and does not change this architecture.

---

## 5. Module catalog

### 5.1 Auth
Owns authentication challenges, sessions, MFA/recovery. Session validity works across app instances. External implementation may sit behind `AuthPort`.

### 5.2 Veteran Profiles
Owns `VeteranProfile`, `PilotEnrollment`.

### 5.3 Check-ins
Owns questionnaire versions, Check-Ins, responses. Check-In completion commits synchronously; signal computation is durable async work.

### 5.4 Support Signals
Owns deterministic/versioned `SupportSignal` settlement and effective-signal projection. Duplicate/replayed compute jobs reuse the same logical computation identity. No generative primary signal.

### 5.5 Consent
Owns `ConsentGrant`, `ConsentEvent`. All share/notify/provider-disclosure paths evaluate use-time authorization/basis.

### 5.6 Trusted Circle
Owns trusted-contact invitation/membership lifecycle. Membership alone grants no visibility.

### 5.7 Cases
Owns `SupportCase`, `CaseAssignment`, `CaseNote`, `ContactAttempt`. Case creation/claim/assignment/reassignment are atomic under contention. Cases reference current Settlement projection but do not own Settlement history.

### 5.8 Requests / Dispatch
Own `ServiceRequest` and canonical transition rules. Request state is independent of provider integration state. Matching remains responder/catalog driven unless later specified.

### 5.9 Resources
Owns `Resource`, `ResourceCategory`, `ServiceOffer`. Catalog freshness is distinct from live provider availability.

### 5.10 Referrals
Owns `Referral`. Logical send is idempotent and distinct from Fulfillment.

### 5.11 Fulfillment
Owns `ServiceFulfillment`, `FulfillmentAttempt`. External provider status supplies evidence; it cannot bypass canonical request/fulfillment transitions.

### 5.12 Provider Router / Adapters
Owns adapter configuration, health/routing references, and provider-neutral invocation. Does not own Service Request state. Ports: `TransportationPort`, `TemporaryShelterPort`, `FoodSupportPort`, `PeerSupportPort`. Manual Adapter required for MVP capability paths.

### 5.13 Follow-up
Owns `FollowUp`, schedule identity/version, business coordination-attempt count, and durable due/overdue processing. Notification retries/job redelivery are separate concerns.

### 5.14 Settlement
Owns first-class multi-cycle `Settlement` history and deterministic current/latest Settlement projection.

Rules:
- one resolution cycle creates one durable Settlement;
- Case reopen preserves the prior Settlement;
- later resolution creates a new cycle;
- Settlement used for a committed `RESOLVED` transition is historical business meaning and cannot be silently overwritten;
- Settlement is not Fulfillment and not a clinical outcome.

### 5.15 Notifications
Owns Notification and preference state. EMAIL/SMS/IN_APP MVP; delivery uses durable async work and channel capability ports.

### 5.16 Administration
Owns Organizations, memberships, pilot config, publication/configuration surfaces, and authorized provider-adapter configuration.

### 5.17 Command Idempotency
Owns persistent logical idempotency records for unsafe product commands that accept `Idempotency-Key`.

Rules:
- same scope/key + same request reuses authoritative outcome;
- same scope/key + conflicting request fails;
- persistence survives app restart/horizontal instances;
- it supplements, not replaces, domain uniqueness constraints and FulfillmentAttempt idempotency.

### 5.18 Audit / Event Layer
Owns immutable Domain/Audit Events and replay-safe publication semantics. Required domain state + event publication is atomic via same transaction/outbox/equivalent pattern. Event identity is distinct from command/job idempotency identity.

---

## 6. Database ownership / tenancy

- PostgreSQL is the logical system of record.
- Module-owned tables and write authority remain explicit.
- Tenant-owned rows carry tenant scope.
- Authorization = role + tenant + row + consent/basis.
- Normal UI paths do not load unbounded history.
- Current projections (effective signal, current assignment, current Settlement) must be deterministic and efficiently queryable.
- Historical facts remain durable behind projections.

Sharding is not an MVP requirement. Read replicas/partitioning/sharding are evidence-driven later choices.

---

## 7. Application statelessness

The following cannot exist only in process memory:

- session validity;
- consent/basis;
- Case/Request/Fulfillment/Settlement state;
- Follow-Up schedule identity;
- durable jobs;
- command idempotency records;
- FulfillmentAttempt/provider reconciliation state;
- correctness-critical locks/leases/current projections.

Process-local caches are disposable optimizations only.

---

## 8. Durable background work

| Work | Required properties |
|---|---|
| Support Signal computation | durable; stable computation identity; idempotent settlement/event |
| Follow-Up due/overdue | durable; schedule-version check; stale jobs no-op/audit |
| Notification send/retry | durable; consent recheck; bounded backoff; DLQ/visibility |
| Provider fulfillment action | durable; FulfillmentAttempt idempotency; unknown-outcome reconciliation |
| Provider reconciliation/webhook | authenticated/deduped/out-of-order safe |
| Resource freshness | lower priority; bounded |
| Auth/session expiry | idempotent |
| Event/outbox publication | replay-safe; cannot permanently lose required event after commit |

Exact durable job product remains D-022.

---

## 9. Sync vs async

**Synchronous:** auth verification, consent evaluation, reads, canonical transition commit, admin commands whose success must be known immediately.

**Asynchronous:** notifications, provider actions where contract permits pending execution, signal compute, Follow-Up timers, provider reconciliation, freshness work.

A client command must not report success for canonical state that has not committed.

---

## 10. Concurrency / idempotency

Atomic/idempotent handling is required for:

- one-active Case creation;
- Case claim/assignment/reassignment;
- Service Request assignment/transitions;
- FulfillmentAttempt creation/external action;
- one-time auth challenge verification;
- command idempotency reservation;
- Support Signal primary settlement;
- Settlement resolution-cycle creation/current pointer update;
- Follow-Up reschedule vs stale due job.

Retries with external consequences use stable logical identity. Ambiguous provider outcomes reconcile before duplicate-risk retry.

---

## 11. Provider-neutral services

Infrastructure ports: `AuthPort`, `SmsPort`, `EmailPort`.

Fulfillment ports: `TransportationPort`, `TemporaryShelterPort`, `FoodSupportPort`, `PeerSupportPort`.

Provider Router selects configured adapters through explicit operational policy. Manual coordination is valid. Vendor status/payload types stay adapter-local.

D-017 selects Uber Guest Rides as the first API-backed `TRANSPORTATION_FULFILLMENT` adapter family for implementation only. Uber remains replaceable: no Uber SDK type, OAuth token shape, trip status, request identifier, estimate field, receipt field, webhook payload, or error code may enter domain models, public SUAS APIs, readiness gates, or canonical state names. The adapter stores only SUAS-owned FulfillmentAttempt identity plus the minimum adapter-local external references needed for reconciliation. Provider-native create idempotency was not confirmed in the released evidence and must not be invented; SUAS-side persistent FulfillmentAttempt idempotency is therefore mandatory before estimates/create/cancel and across process restart/horizontal instances.

Uber OAuth client secrets are server-side adapter secrets only. They are loaded through the approved secret mechanism for the environment, never committed, never exposed to browser/mobile clients, never echoed in health checks or logs, and rotated/revoked as adapter configuration. The adapter requests only the official Guest Rides token scope `guests.trips` unless a later released decision authorizes additional scopes.

---

## 12. Scaling doctrine

1. Measure.
2. Remove inefficient queries/work.
3. Add stateless app/worker capacity.
4. Tune PostgreSQL/indexes/pooling.
5. Apply backpressure/adapter concurrency limits.
6. Add cache/read replica/partitioning only from evidence.
7. Extract services only from measured module-specific need.

Capacity bands are test envelopes, not adoption forecasts.

---

## 13. Resilience doctrine

Required: finite timeouts, bounded/backoff retry, provider rate-limit handling, circuit breaking, failed-work visibility, duplicate job/webhook safety, unknown-outcome reconciliation, manual fallback, backpressure, and backup/restore testing.

---

## 14. Observability

Production telemetry covers API/DB/queue/worker health, notification delivery, provider latency/errors/rate limits/circuit state, webhook lag, claim conflicts, stale job suppression, idempotency conflicts, signal deduplication, Settlement-cycle creation, reconciliation, event/outbox lag, audit growth, and tenant noisy-neighbor effects.

Correlation identifiers must avoid unnecessary veteran PII.

---

## 15. Security / AI / funding boundaries

- Authentication is not authorization.
- Provider disclosure uses minimum-necessary projection and authenticated callbacks.
- No safety-critical generative AI.
- No automated emergency dispatch.
- Funding/billing remains `FUTURE`; no payment-card checkout architecture in MVP.

---

## 16. Non-goals

- microservices by default;
- volatile process-local production queues;
- vendor-specific domain types;
- event sourcing as the only system of record;
- multi-region active-active without measured need;
- one mutable Settlement record that destroys reopen history;
- process-memory-only command idempotency;
- insertion-order current projections.
