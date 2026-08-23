# TESTING.md — Test suites and production-readiness gates (SUAS v0.1)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.1.3.md](RELEASE_MANIFEST-0.1.3.md)
**Related:** [STATUS.md](STATUS.md), [API.md](API.md), [AUTH.md](AUTH.md), [MVP_REFERENCE.md](MVP_REFERENCE.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md), [CASES.md](CASES.md), [DISPATCH.md](DISPATCH.md), [SETTLEMENT.md](SETTLEMENT.md), [FOLLOWUP.md](FOLLOWUP.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [CONSENT.md](CONSENT.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [SAFETY.md](SAFETY.md), [SECURITY.md](SECURITY.md)

---

## 1. Purpose

Define evidence required before any domain, MVP, or production release can be claimed conformant/ready. Tests use released specs as authority.

---

## 2. Test layers

| Layer | Proves |
|---|---|
| Unit | pure validation/signal/freshness/provider-normalization functions |
| Domain/state-machine | only documented Case/Request/Fulfillment/Follow-Up transitions |
| Concurrency/idempotency | one-winner contested actions and replay-safe commands/jobs |
| Authorization/tenant | role × tenant × row × consent/basis; no cross-tenant leakage |
| Integration | PostgreSQL module boundaries, durable jobs, outbox/equivalent, provider ports |
| API contract | paths/errors/pagination/version/idempotency/Settlement cycles |
| Auth | single-use challenges, MFA, shared session revoke/rate controls |
| Provider adapter | vendor-neutral capability conformance |
| Notification | logical-send dedupe, consent recheck, retry/callback safety |
| Security/privacy | threat controls, provider projection, webhook auth, log minimization |
| Migration/restore | schema changes/restore on representative fixture volume |
| End-to-end | Veteran + Responder + Admin surfaces/workflow |
| Visual/accessibility | MVP conformance + WCAG 2.2 AA target |
| Load/performance | D-021/D-023 workload profiles |
| Resilience/failure drill | crash/replay/stale/dependency/restore scenarios |
| Pilot simulation | synthetic full loop; no production veteran data |

---

## 3. Critical correctness suites

### 3.1 Support Signal
- same source + signal/questionnaire versions → same level/basis;
- duplicate/replayed compute job settles one logical primary SupportSignal;
- effective projection deterministic, not insertion-order dependent;
- override inserts history; no mutation of prior signal;
- required event publication recovers safely after post-commit publisher failure;
- no generative primary compute path.

### 3.2 Consent/privacy
- revoke stops future view/notify/referral/provider disclosure;
- provider projection contains minimum required fields only;
- whole Check-In/Case Notes/Trusted Circle/unrelated requests excluded by default;
- history remains auditable.

### 3.3 Case / Request / responder concurrency
- illegal transitions fail;
- concurrent one-active Case creation resolves to one logical Case under MVP policy;
- two concurrent `CLAIM_CASE` operations produce one winner and deterministic conflict;
- assignment/reassignment preserves history;
- stale queue/browser state cannot override mutation-time authority;
- provider callbacks cannot bypass Request/Fulfillment transitions;
- Assignment ≠ Fulfillment.

### 3.4 Settlement / Follow-Up
- resolve without required Settlement/prerequisites fails;
- same resolve request + same idempotency key returns one Settlement/cycle;
- conflicting idempotency reuse fails;
- reopen preserves prior Settlement;
- later resolve creates a later `resolution_cycle`;
- deterministic current/latest Settlement projection matches history;
- stale Follow-Up due/overdue job after reschedule no-ops/audits;
- blocking Follow-Up prevents resolution; carried-forward Follow-Up remains visible/owned after resolution;
- notification retry does not increment Follow-Up coordination-attempt count.

### 3.5 Events / command idempotency
- Domain/Audit Events immutable;
- `event_id` distinct from command idempotency key;
- domain commit + required event cannot permanently diverge under crash/replay;
- same API idempotency key/request replays authoritative outcome across app restart/instance change;
- same key/conflicting request → `409 IDEMPOTENCY_CONFLICT`;
- duplicate consumer delivery produces one logical downstream effect.

---

## 4. AUTH suite

Required:
- configured passwordless challenge/verify works;
- same challenge verified concurrently → one success maximum;
- consumed challenge replay fails;
- responder/admin cannot elevate without MFA;
- user/membership/session revoke on instance A is enforced on instance B;
- process restart/cache loss does not revive revoked session;
- correctness-critical rate limit cannot be bypassed by rotating app instances;
- org-admin cannot cross tenant or self-elevate to SUAS-admin;
- D-016 MVP enrollment does not require VA API/DD-214/in-person proofing.

---

## 5. Provider-adapter conformance suite

Every enabled adapter proves:
1. no provider SDK types in domain packages;
2. provider payload maps to bounded SUAS shapes;
3. fake adapters swap without domain change;
4. Manual Adapter works for each enabled MVP capability;
5. same FulfillmentAttempt idempotency key produces one logical external mutation;
6. deliberate provider switch creates a new attempt;
7. timeout after possible acceptance → `PROVIDER_UNKNOWN`, reconcile before risky retry;
8. duplicate/out-of-order webhook safe; unauthenticated callback rejected;
9. provider status cannot bypass canonical transitions;
10. minimum-necessary disclosure enforced;
11. provider outage preserves Request and supports configured alternate/manual path;
12. rate-limit/backoff/circuit behavior observable;
13. unsupported provider capability is reported unsupported, not faked;
14. disabling/replacing adapter preserves historical attempts.

D-017 Uber Guest Rides deterministic adapter matrix uses synthetic data/fakes and must not create real rides or contact real riders/drivers:

| Case | Deterministic assertion |
|---|---|
| OAuth scope/secret | adapter requests only `guests.trips`; missing/malformed client secret fails closed; secret absent from logs/client fixtures |
| API path mapping | estimates use `POST /v1/guests/trips/estimates`; create uses `POST /v1/guests/trips`; get uses `GET /v1/guests/trips/{request_id}`; cancel uses `DELETE /v1/guests/trips/{request_id}`; receipt uses `GET /v1/guests/trips/{request_id}/receipt` |
| Provider replaceability | domain tests pass with fake/manual adapter and contain no Uber SDK/status/payload types |
| Local idempotency | same FulfillmentAttempt and request fingerprint produce one logical create intent across process restart and multiple workers |
| Conflicting idempotency | same attempt key with different request fingerprint fails before provider call |
| Unknown create outcome | timeout/lost response after possible acceptance records `PROVIDER_UNKNOWN` and reconciles by stored request reference/status before retry |
| Provider idempotency gap | tests do not assert or rely on provider-native create idempotency because it was not confirmed |
| Rate limit/backoff | 429/limit response enters rate-limited/circuit path with bounded jittered retry and operator visibility |
| Manual fallback | fallback creates a deliberate new attempt only when policy permits and preserves original unknown outcome audit |
| Webhook HMAC | if webhook ingress exists, valid HMAC over raw body is required; invalid/missing/replayed/duplicate webhooks have no second domain effect |
| Receipt handling | receipt fetch/projection is adapter-local and redacted from ordinary logs |

D-018 Amadeus shelter deterministic adapter matrix uses synthetic data/fakes and must not access scarce real inventory, contact real properties/guests, create holds/reservations, or incur charges:

| Case | Deterministic assertion |
|---|---|
| Provider replaceability | Domain tests pass with Amadeus fake and `ManualShelterAdapter`; no Amadeus SDK, property/rate/offer status, or reservation types enter domain packages |
| Field-level projection | Only the released shelter projection is transmitted; Case Notes, Check-In answers, Support Signal basis, military/medical records, unrelated requests, and raw payment-card data are absent |
| Ranking determinism | Same normalized offers + same versioned explicit inputs produce the same order and reason codes; ties use a stable documented tie-breaker |
| Ranking explainability | Each result records bounded reason codes based on explicit availability, location/coverage, stay window, accessibility fit, cancellation terms, and informational cost; no clinical/hidden-eligibility/ability-to-pay inference |
| Mandatory manual path | `ManualShelterAdapter` remains available when search is unavailable, degraded, unsupported, or payment-blocked |
| Payment boundary | Payment-dependent reservation fails before provider mutation as `BLOCKED_BY_PAYMENT_ARCHITECTURE`; fixtures/logs contain no card number, security code, raw payment token, or provider payment form |
| Card-free contract gate | `card_free_enterprise` mode fails startup/operation without the required owner-approved deployment record; configuration alone cannot enable it |
| Local idempotency | Same FulfillmentAttempt and request fingerprint produce one logical hold/reserve/cancel intent across restart and multiple workers |
| Conflicting idempotency | Same attempt key with a different request fingerprint fails before provider call |
| Unknown mutation outcome | Timeout/lost response after possible hold/reservation/cancel records `PROVIDER_UNKNOWN` and reconciles before retry |
| Health and fallback | Auth failure, 429, timeout, malformed response, unavailable inventory, and circuit-open states are observable and preserve the Request/manual fallback |
| Status isolation | Provider availability/reservation status cannot directly transition canonical Service Request or Fulfillment state |
| Cancellation | Cancellation support/terms are represented truthfully; unsupported cancellation fails to a human rather than reporting success |

---

## 6. Notification suite

Required:
- one Notification row per logical send;
- duplicate generating event/job maps to one Notification when dedupe identity matches;
- deliberate reminder/escalation creates new logical identity;
- consent/basis rechecked before each external attempt;
- revoke between enqueue/send prevents send;
- duplicate worker delivery does not create duplicate logical message/effect;
- each actual transport attempt appends immutable Audit Event;
- duplicate/out-of-order delivery callbacks are safe;
- provider outage leaves truthful delivery state/ops visibility;
- Notification retry count is independent of Follow-Up coordination attempts.

---

## 7. UI / MVP-reference suite

Deterministic synthetic fixtures cover:
- landing `TAKE ACTION` hierarchy;
- role/enrollment;
- Veteran support home;
- QRF request/searching/pending;
- QRF no-responder/degraded state;
- immediate resources;
- category surface;
- Resource list/detail;
- responder on-duty/dashboard/Quick Resource Share;
- active needs/alerts;
- Chat/Home navigation;
- Admin overview.

Required assertions:
- `I NEED SUPPORT` / `I WANT TO SERVE` hierarchy remains recognizable;
- production enrollment does not preserve contradictory `No email` copy;
- QRF does not guarantee nearby/immediate responder contact without evidence;
- QRF does not require continuous GPS;
- Call/Message only appear with an authorized contact path;
- future Counseling/Community/Job Training reference cards do not create hidden released workflows;
- Resource facts come from verified fixture data, not hard-coded prototype truth;
- placeholder dashboard metrics are not presented as real facts;
- accessibility target: WCAG 2.2 AA, keyboard/focus/reflow/touch/semantic naming/non-color-only signals.

Visual review detects hierarchy/navigation/density/responsive/product drift; pixel equality not required.

---

## 8. API/pagination suite

- `/api/v0` is the sole canonical v0 version selector;
- list endpoints enforce bounded page size and deterministic/keyset-safe ordering;
- tenant/auth filtering occurs before result exposure;
- normal UI does not download complete growing history;
- large fixtures reveal no N+1 critical queue/resource path;
- stale transition → deterministic conflict/no partial state;
- resolve is atomic/idempotent and creates one Settlement cycle;
- request correlation propagates without PII leakage.

---

## 9. Scale/performance suite

D-021 defines release workload envelope; D-023 defines relevant SLO/alerts. No unsupported numeric target is inferred from this spec.

Profiles:

### Steady state
Representative mixed release workload.

### Burst
Support/QRF requests + contested claims + notifications + provider calls/webhooks. Backpressure visible; urgent work not starved by maintenance.

### Degraded dependency
One provider/channel slow/rate-limited/unavailable; core state remains correct.

### Horizontal correctness
At least two app instances: session revoke, idempotency, contested claims, signal settlement, Settlement resolve, and tenant isolation remain correct independent of instance routing.

### Concurrency stress
Simultaneous claim/assign/resolve/FulfillmentAttempt creation plus duplicate command/job delivery.

Test artifacts record workload dimensions/environment/results/caveats.

---

## 10. Resilience/failure-drill suite

Staging synthetic drills include:
1. notification provider outage;
2. fulfillment timeout after possible acceptance;
3. duplicate/out-of-order provider webhook;
4. worker restart with queued work;
5. queue backlog/burst;
6. DB connection loss/commit uncertainty;
7. provider rate limiting/manual fallback;
8. duplicate API retry after lost response;
9. concurrent Settlement resolve;
10. Follow-Up reschedule + stale due job;
11. session/membership revoke + request on another instance;
12. event/outbox publisher crash after commit;
13. restore with pending/unknown provider attempts + idempotency history.

Pass conditions come from [RESILIENCE.md](RESILIENCE.md). D-024 recovery targets must be set for the release before the gate can be READY.

---

## 11. Readiness gates

| Gate | Minimum evidence |
|---|---|
| **AUTH** | §4 green |
| **CONSENT** | use-time grant/provider-disclosure suites green |
| **CHECK-IN** | questionnaire + signal deterministic/replay suites green |
| **COORDINATION** | Case/Request/responder concurrency/state suites green |
| **EXTERNAL_FULFILLMENT** | provider adapter/manual/idempotency/reconciliation suites green |
| **UI_CONFORMANCE** | MVP behavior/visual/accessibility suite green |
| **SAFETY** | red-state/human-review/no-auto-dispatch/no-diagnosis tests green |
| **PRIVACY** | minimization/log/provider projection/non-prod-data tests green |
| **SCALE** | D-021/D-023 release profiles + horizontal/backpressure/tenant-fairness evidence green |
| **RESILIENCE** | §10 + restore/replay evidence green with D-024 set |
| **OPERATIONS** | staffing/queue/resource/provider/incident/recovery runbooks and exercised duties |
| **REPORTING** | allowed operational metrics reproducible; forbidden clinical claims absent |

All remain `NOT_READY` unless [STATUS.md](STATUS.md) records accepted evidence.

---

## 12. Fixtures / non-goals

- synthetic veterans only;
- D-011 golden vectors for `qv-001` + `sv-001` are released in [SIGNAL_SCORING.md](SIGNAL_SCORING.md) B4; other version pairs remain `UNRELEASED_FIXTURE` until released;
- D-012 uses `TEST_SAFETY_COPY` until approved;
- fake provider adapters until decisions close;
- no production veteran data in non-prod tests;
- no unnamed vendor SLA/clinical validation/pixel-perfect clone/specific cloud-broker requirement;
- small pilot fixtures are not sufficient scale evidence.

---

## 13. Handoff

A release/pilot readiness claim must cite evidence for every applicable gate. Passing tests against draft specs does not create implementation authority before SPEC-016.
