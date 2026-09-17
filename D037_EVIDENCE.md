# D037_EVIDENCE.md — Evidence model, Run 001, measurements, budget, matrix

**Decision:** D-037  
**Status:** `proposed` / not release-authoritative  
**Extends:** [TESTING.md](TESTING.md), [skills/evidence-gate/SKILL.md](skills/evidence-gate/SKILL.md), [ANALYTICS.md](ANALYTICS.md), [EVENT_MODEL.md](EVENT_MODEL.md)  
**Does not replace:** product readiness gates or operational metrics

## 1. Existing evidence model

SUAS already has evidence surfaces:

- TESTING.md suites and twelve product readiness gates;
- evidence-gate skill states (`IMPLEMENTED`, `VERIFIED`, `ACCEPTED`, `RELEASED`, `NOT_READY`, `NOT_COMPUTABLE`, `DECISION_PENDING`);
- D-035 sandbox evidence hashes and owner settlement;
- ANALYTICS.md operational coordination metrics;
- EVENT_MODEL.md domain events;
- build provenance in ENVIRONMENT.md §8.

Those surfaces do not currently represent a sealed experimental run that includes operator intervention, cost, purpose class, and funding-reuse eligibility. D-037 extends them with `EvidenceRun` / `EvidenceArtifact` rather than renaming existing gates.

## 2. Evidence chain

```text
Scenario
  → Observation
  → Model/System Output
  → Confidence / Uncertainty
  → Operator Decision
  → System Action
  → Outcome
  → Telemetry
  → Evaluation
  → Evidence Artifact
```

Every artifact traces to its originating run. A run may terminate `FAILED`, `ABORTED`, or `PARTIAL` and still produce an artifact.

## 3. Evidence artifact fields

Schema version: `evidence-artifact.v0`.

Required when the architecture can produce the value. Optional otherwise. No phantom defaults.

| Field | Cardinality | Notes |
|---|---|---|
| `schema_version` | required | `evidence-artifact.v0` |
| `artifact_id` | required | immutable |
| `run_id` | required | parent EvidenceRun |
| `scenario_id` | required | |
| `recorded_at_utc` | required | |
| `suas_env` | required | `LOCAL\|TEST\|STAGING\|PRODUCTION` |
| `purpose_class` | required | `ENGINEERING\|CONTROLLED_EXPERIMENT\|DEMO\|FIELD` |
| `software_revision` | required | application commit |
| `spec_version` | required | released stack pin |
| `release_manifest` | required | |
| `configuration_revision` | optional | frozen experiment config hash when present |
| `model_provider_id` | optional | `NOT_COMPUTABLE` if unused |
| `model_version` | optional | |
| `input_provenance` | required | fixture/dataset id + hash or explicit `NONE` |
| `output_provenance` | required | digest or explicit `NONE` |
| `operator_ref` | optional | pseudonymous |
| `system_state` | optional | |
| `confidence` | optional | structured; omit if the surface has no uncertainty representation |
| `operator_action` | required | `ACCEPT\|REJECT\|MODIFY\|ABSTAIN_ACK\|ABORT\|NONE` |
| `intervention_state` | required | `NONE\|INTERVENED\|ABSTAINED\|UNAVAILABLE` |
| `latency_ms` | optional | end-to-end if measured |
| `errors` | optional | structured list |
| `recovery_events` | optional | |
| `resulting_state` | optional | canonical domain state names only |
| `evaluation_method` | optional | filled at evaluation time |
| `evaluator_ref` | optional | distinct from operator when evaluation is independent |
| `artifact_digest` | required at seal | |
| `lineage` | optional | predecessor artifact ids |
| `retention_class` | required | `UNRESOLVED` until D-007 closes |

Do not require model fields on runs that exercise only released coordination paths with fixture adapters.

## 4. SUAS-EVIDENCE-RUN-001

**Stable experiment identifier:** `SUAS-EVIDENCE-RUN-001`  
**Purpose:** demonstrate that a complete SUAS operator loop can be executed, observed, reconstructed, and evaluated on controlled infrastructure without real veteran data or real external effects.  
**Purpose class:** `CONTROLLED_EXPERIMENT`  
**Permitted env:** `TEST` or `STAGING`  
**Current state:** `PLANNED` as specification only. Not configured. Not run.

The operator loop exercised here is the released coordination loop, using synthetic fixtures and fake/manual/sink adapters:

```text
SIGNAL → NEED → CONSENT → COORDINATION → FULFILLMENT → FOLLOW-UP
```

plus an explicit operator decision on a system recommendation (accept / reject / modify / abstain). Settlement may be omitted when the frozen configuration declares it out of scope for Run 001.

This run is not a grant demonstration and not a production drill.

### 4.1 Preconditions

Include only actual prerequisites.

- authenticated privileged operator or test operator fixture;
- `SUAS_ENV` in `{TEST, STAGING}`;
- `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false`;
- known application commit, spec version, release manifest;
- synthetic dataset identity and hash recorded;
- telemetry/audit write path enabled for the run;
- required secrets for the chosen fake/sink/manual adapters configured;
- experiment configuration frozen and hashed;
- evidence destination available (object store, repo path, or equivalent declared later);
- no real veteran records addressable in the target environment.

Items that remain `NOT_COMPUTABLE` until later inventory: exact cloud project/account, exact evidence-store URI, exact observability vendor.

### 4.2 Happy path

1. Operator opens Run 001 with frozen configuration hash.
2. System loads synthetic scenario `SCN-FR-001-A` (one Veteran fixture, one Check-In, one non-RED signal or RED-as-fixture per SAFETY.md rules).
3. System emits observation record (Check-In completed).
4. System emits recommendation against released scoring/coordination rules currently valid for the pinned stack. TEST/CI remain on `SUAS_SUPPORT_SIGNAL_MODE=fixture`.
5. System emits confidence/uncertainty if the pinned stack has a representation; otherwise records `confidence: null` with reason `SURFACE_ABSENT`.
6. Operator accepts the recommendation.
7. System performs the corresponding authorized coordination action through fake/manual adapters.
8. Outcome and domain events persist.
9. Telemetry and audit events persist.
10. Run reaches `COMPLETED`.
11. Evaluator later attaches `EvaluationResult` without mutating the run.
12. Artifact is sealed.

### 4.3 Alternate paths

| Path | Operator / system behavior | Terminal class |
|---|---|---|
| Accept | as happy path | `COMPLETED` |
| Reject | recommendation declined; system records rejection; no unauthorized external effect | `COMPLETED` |
| Modify | operator supplies a permitted modification; system records before/after | `COMPLETED` |
| System abstains | model/system withholds recommendation; operator acknowledges | `COMPLETED` |
| Insufficient confidence | below protocol threshold if one exists; otherwise `NOT_COMPUTABLE` for this field | `COMPLETED` or `ABORTED` per freeze |
| Missing observation | scenario cannot start; run records why | `FAILED` or `ABORTED` |
| Delayed response | latency recorded; run still completable | `COMPLETED` |

### 4.4 Failure paths

Provider failure, timeout, telemetry failure, authentication failure, malformed response, inconsistent state, evidence persistence failure, partial run, operator abort.

A failed experiment is not automatically invalid evidence. Record the failure, classify the run `FAILED`, `ABORTED`, or `PARTIAL`, and seal what exists if integrity allows. If persistence itself failed, record a successor stub with `errors` naming the persistence failure.

### 4.5 Reconstruction requirement

A second authorized evaluator, given the sealed artifact plus frozen configuration and synthetic dataset hash, must be able to state whether the happy-path or named alternate/failure path occurred. Inability to reconstruct is an evaluation finding, not a reason to discard the run.

## 5. Measurement surfaces

Classify only quantities the current architecture can realistically produce or explicitly cannot.

Definitions use counts over a declared run cohort. Vanity metrics are omitted.

| ID | Metric | Definition | Class |
|---|---|---|---|
| FR-M-001 | End-to-end response latency | `t_outcome_recorded - t_scenario_start` in ms for a named path | OPTIONAL |
| FR-M-002 | Model inference latency | provider-reported or locally timed inference interval | FUTURE if no model is in the frozen config; OPTIONAL if present |
| FR-M-003 | Operator response latency | `t_operator_action - t_recommendation_emitted` | OPTIONAL |
| FR-M-004 | Intervention frequency | interventions / runs in cohort | REQUIRED for Run 001 cohort |
| FR-M-005 | Recommendation acceptance rate | accepts / recommendations offered | REQUIRED |
| FR-M-006 | Recommendation modification rate | modifies / recommendations offered | REQUIRED |
| FR-M-007 | Recommendation rejection rate | rejects / recommendations offered | REQUIRED |
| FR-M-008 | Abstention rate | system abstentions / recommendation attempts | REQUIRED |
| FR-M-009 | Error frequency | runs with `errors.length > 0` / runs started | REQUIRED |
| FR-M-010 | Recovery frequency | runs with recovery events / runs started | OPTIONAL |
| FR-M-011 | Successful completion rate | `COMPLETED` / runs started | REQUIRED |
| FR-M-012 | Disagreement frequency | reject+modify / recommendations offered | OPTIONAL (derived) |
| FR-M-013 | Calibration | reliability vs ground truth | NOT_COMPUTABLE until a ground-truth protocol exists |
| FR-M-014 | Repeatability | identical frozen config yields identical canonical state sequence | OPTIONAL |
| FR-M-015 | Resource consumption | recorded CPU/memory/request units when the platform exposes them | FUTURE / NOT_COMPUTABLE until provider known |
| FR-M-016 | Estimated compute cost | see cost record | OPTIONAL after first billed or credited interval |
| FR-M-017 | Evidence completeness | required fields present / required fields | REQUIRED |

ANALYTICS.md operational metrics remain product metrics. They are not funding-performance metrics and must not be retitled as clinical or causal outcomes.

## 6. Cloud credit experiment budget

Advisory only. Not a spending requirement. Provider unknown.

Planning envelope for the operator-asserted `$300`:

| Category | Planning ceiling |
|---|---|
| Controlled deployment | `$80` |
| Telemetry / observability | `$60` |
| Model / inference experiments | `$70` |
| Storage / evidence datasets | `$35` |
| Security / IAM testing | `$25` |
| Acceptance / contingency reserve | `$30` |
| **Total** | **`$300`** |

Actual allocation depends on provider credit rules, expiration, eligible services, existing free tiers, experiment requirements, and observed consumption. Prefer free tiers when they do not compromise experiment validity.

Cost evidence record:

```text
experiment → resource → usage → nominal cost → credit applied → cash cost → evidence produced
```

Fields: `experiment_id`, `resource`, `usage_qty`, `usage_unit`, `nominal_cost_usd`, `credit_applied_usd`, `cash_cost_usd`, `evidence_artifact_ids`, `recorded_at_utc`, `provider` (nullable / `NOT_COMPUTABLE`).

This record exists so later grant compute estimates can cite measured workloads. It does not authorize spending.

## 7. Funding evidence matrix

Never mark evidence `AVAILABLE` unless an artifact exists in this repository or a cited implementation repo at a named path/hash.

| Capability | Existing implementation | Evidence available | Evidence missing | Experiment needed | Funding-relevance class |
|---|---|---|---|---|---|
| Operator workflow | RESPONDER_WORKFLOWS.md + ADMIN.md specified; runtime conformance in SPEC-017 | spec text | sealed operator-loop run | Run 001 | HIGH |
| Human/AI decision support | Support Signal fixture path; no generative safety-critical AI | scoring contract `qv-001`/`sv-001` | operator accept/reject/modify record | Run 001 | HIGH |
| Autonomous-system observability | OPERATIONS.md duties; no production SLO | spec text | run telemetry artifact | Run 001 OPTIONAL metrics | MEDIUM |
| Uncertainty representation | incomplete-input behavior in SIGNAL_SCORING.md | scoring basis fields | calibrated confidence | FUTURE protocol | MEDIUM |
| Operator intervention | human coordination is first-class | spec doctrine | intervention_state on sealed runs | Run 001 | HIGH |
| Reproducible execution | tests + fixtures required | CI exists in implementation repos; not accepted as gate evidence | frozen-config reconstruction | Run 001 repeatability | HIGH |
| Security / access control | SECURITY.md / AUTH.md | D-035 staging packet accepted for VA path only | Run 001 auth-failure path | Run 001 failure paths | HIGH |
| Auditability | audit events specified | spec text | sealed audit excerpt for Run 001 | Run 001 | HIGH |
| Provenance | build provenance contract | ENVIRONMENT.md §8 | artifact digest + lineage | Run 001 seal | HIGH |
| Telemetry | operational health signals specified | spec text | measured latencies | OPTIONAL | MEDIUM |
| Failure recovery | RESILIENCE.md | spec text | recovery event on a failed run | Run 001 failure path | MEDIUM |
| Controlled experimentation | D-035 evidence authority pattern | D-035 qualifier released | D-037 run | Run 001 | HIGH |
| Model evaluation | no safety-critical generative model | none | ground truth protocol | FUTURE | LOW until a model is in scope |
| Data management | PRIVACY.md / synthetic-data skill | skill + env prohibitions | retention decision D-007 | none from D-037 | MEDIUM |
| Cloud deployment | D-001 open; `suas` is a Cloudflare Worker per README | README statement | production hosting decision | not authorized by this packet | MEDIUM |

`HIGH` / `MEDIUM` / `LOW` are relevance classes for later opportunity comparison. They are not product priorities and do not reorder SPEC-017.
