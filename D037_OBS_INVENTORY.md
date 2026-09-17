# D037_OBS_INVENTORY.md — FR-T-OBS-001 field inventory

**Decision:** D-037  
**Task:** `FR-T-OBS-001`  
**Parent:** FR-R-004, FR-R-005  
**Date:** `2026-09-17`  
**Scope:** public contracts in `suas-specs` at `d037-accept-as-specified` (`0432c6f`) plus released `0.6.0` canon on `main` (`da49d315`)  
**Runtime repositories inspected:** none  
**Runtime authority:** none  

This inventory answers which `EvidenceArtifact` / `EvidenceRun` fields already have a public-contract source. It does not inspect `suas`, `suas-ios`, or `suas-android` logs. Runtime emission for every field is therefore `NOT_COMPUTABLE`.

## Method

Compared [schemas/funding-readiness/evidence-artifact.v0.json](schemas/funding-readiness/evidence-artifact.v0.json) and [D037_EVIDENCE.md](D037_EVIDENCE.md) §3 against:

- [EVENT_MODEL.md](EVENT_MODEL.md) envelope and catalogs
- [ENVIRONMENT.md](ENVIRONMENT.md) §2, §3, §8
- [ANALYTICS.md](ANALYTICS.md)
- [OPERATIONS.md](OPERATIONS.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [skills/evidence-gate/SKILL.md](skills/evidence-gate/SKILL.md)
- [D035_PROTOCOL.md](D035_PROTOCOL.md) §12 observability (pattern only; D-035 scope is VA verification)

Labels used here:

| Label | Meaning |
|---|---|
| `SPECIFIED` | a released or draft public contract already names an equivalent field or event |
| `PARTIAL` | a related concept exists; it is not the D-037 field and cannot be aliased |
| `ABSENT` | no public contract field or event type exists |
| `OBSERVED` | reserved for a cited runtime emit path; unused in this inventory |
| `NOT_COMPUTABLE` | runtime emit / store URI / vendor cannot be determined from specs |

`SPECIFIED` is not `OBSERVED`. Green CI and merged code still cannot promote a field to emitted.

## EvidenceArtifact fields

| Field | Cardinality in v0 schema | Public-contract source | Contract state | Runtime emit |
|---|---|---|---|---|
| `schema_version` | required | D-037 schema only | `ABSENT` outside this packet | `NOT_COMPUTABLE` |
| `artifact_id` | required | no existing evidence-artifact identity in EVENT_MODEL / evidence-gate | `ABSENT` | `NOT_COMPUTABLE` |
| `run_id` | required | no EvidenceRun identity in released catalogs | `ABSENT` | `NOT_COMPUTABLE` |
| `scenario_id` | required | TESTING.md fixtures exist as a class; no stable scenario id on events | `PARTIAL` | `NOT_COMPUTABLE` |
| `recorded_at_utc` | required | EVENT_MODEL `occurred_at` | `SPECIFIED` as event time, not artifact time | `NOT_COMPUTABLE` |
| `suas_env` | required | ENVIRONMENT.md `SUAS_ENV` | `SPECIFIED` as config; not an event payload field | `NOT_COMPUTABLE` |
| `purpose_class` | required | D-037 overlay only; ENVIRONMENT.md forbids new env values | `ABSENT` in released contracts | `NOT_COMPUTABLE` |
| `software_revision` | required | ENVIRONMENT.md §8 application commit SHA | `SPECIFIED` as build provenance | `NOT_COMPUTABLE` |
| `spec_version` | required | `SUAS_SPEC_VERSION` / ENVIRONMENT.md §3 and §8 | `SPECIFIED` as build provenance | `NOT_COMPUTABLE` |
| `release_manifest` | required | `SUAS_RELEASE_MANIFEST` / ENVIRONMENT.md §3 and §8 | `SPECIFIED` as build provenance | `NOT_COMPUTABLE` |
| `configuration_revision` | optional | no frozen-experiment config hash contract | `ABSENT` | `NOT_COMPUTABLE` |
| `model_provider_id` | optional | Run 001 permits fixture adapters with no model | `ABSENT` (and not required for Run 001 if unused) | `NOT_COMPUTABLE` |
| `model_version` | optional | same | `ABSENT` | `NOT_COMPUTABLE` |
| `input_provenance` | required | fixture/dataset identity is a TESTING.md practice; no required event field for dataset hash | `PARTIAL` | `NOT_COMPUTABLE` |
| `output_provenance` | required | no digest-of-output contract on domain events | `ABSENT` | `NOT_COMPUTABLE` |
| `operator_ref` | optional | EVENT_MODEL `actor_id` + `actor_type` | `PARTIAL` — actor is specified; durable pseudonymous evidence ref is not | `NOT_COMPUTABLE` |
| `system_state` | optional | domain aggregate status on payloads (`CASE_*`, Request state, etc.) | `PARTIAL` — canonical domain states exist; no run-level system_state | `NOT_COMPUTABLE` |
| `confidence` | optional | SIGNAL_SCORING.md scoring basis; D037_EVIDENCE.md allows `SURFACE_ABSENT` | `PARTIAL` / Run 001 may record `null` + `SURFACE_ABSENT` | `NOT_COMPUTABLE` |
| `operator_action` | required | RESPONDER_WORKFLOWS.md / CASES.md command outcomes; no `ACCEPT|REJECT|MODIFY|ABSTAIN_ACK|ABORT|NONE` enum on events | `PARTIAL` | `NOT_COMPUTABLE` |
| `intervention_state` | required | human coordination is first-class doctrine; enum `NONE|INTERVENED|ABSTAINED|UNAVAILABLE` is D-037 only | `ABSENT` as a field | `NOT_COMPUTABLE` |
| `latency_ms` | optional | ANALYTICS.md time-to-assignment / contact intervals; OPERATIONS.md latency as a reliability signal | `PARTIAL` — product intervals exist; run end-to-end `latency_ms` does not | `NOT_COMPUTABLE` |
| `errors` | optional | EVENT_MODEL does not define a structured run-error array; OPERATIONS.md names failure classes operationally | `PARTIAL` | `NOT_COMPUTABLE` |
| `recovery_events` | optional | EVENT_MODEL §4 includes recovery/replay/dead-letter as audit coverage | `PARTIAL` — coverage required; no typed recovery_events array | `NOT_COMPUTABLE` |
| `resulting_state` | optional | domain event payloads carry canonical states | `PARTIAL` | `NOT_COMPUTABLE` |
| `evaluation_method` | optional | evidence-gate skill output schema is a gate assessment, not EvaluationResult | `ABSENT` on domain events | `NOT_COMPUTABLE` |
| `evaluator_ref` | optional | none | `ABSENT` | `NOT_COMPUTABLE` |
| `artifact_digest` | required at seal | D-035 evidence hashes are a pattern; no general artifact digest contract | `PARTIAL` (pattern only) | `NOT_COMPUTABLE` |
| `lineage` | optional | EVENT_MODEL `causation_event_id` is event causality, not artifact successor lineage | `PARTIAL` | `NOT_COMPUTABLE` |
| `retention_class` | required | D-007 `DECISION_PENDING`; D-037 forces `UNRESOLVED` | `SPECIFIED` as unresolved doctrine, not a stored field | `NOT_COMPUTABLE` |

## EvidenceRun lifecycle vs EVENT_MODEL

WF-FR-001 states: start, state change, operator action, seal, and abort emit audit events using existing privileged-admin audit vocabulary where possible. New event names wait for a released EVENT_MODEL change (`FR-T-SPEC-003`, currently `BLOCKED`).

| Run / workflow fact | Existing event type | Contract state |
|---|---|---|
| Run opened / `PLANNED` | none | `ABSENT` |
| Configuration freeze recorded | none | `ABSENT` |
| Run `READY` / `RUNNING` | none | `ABSENT` |
| Check-In completed inside the scenario | `CHECKIN_COMPLETED` | `SPECIFIED` |
| Support Signal settled | `SUPPORT_SIGNAL_CHANGED` | `SPECIFIED` |
| Case created / assigned / contacted | `CASE_CREATED`, `CASE_ASSIGNED`, `RESPONDER_CONTACT_LOGGED` | `SPECIFIED` |
| Service request / fulfillment | `SERVICE_REQUEST_*`, `SERVICE_ACCEPTED`, `SERVICE_FULFILLED`, `SERVICE_FAILED` | `SPECIFIED` |
| Consent grant/revoke | `CONSENT_GRANTED`, `CONSENT_REVOKED` | `SPECIFIED` |
| Follow-up | `FOLLOWUP_*` | `SPECIFIED` |
| Operator accept/reject/modify/abstain/abort as D-037 enum | none | `ABSENT` |
| Run `COMPLETED` / `FAILED` / `ABORTED` / `PARTIAL` | none | `ABSENT` |
| Evaluation attached | none | `ABSENT` |
| Artifact sealed | none | `ABSENT` |
| Auth failure during the run | audit coverage required by EVENT_MODEL §4; no typed run-scoped event | `PARTIAL` |
| Persistence failure stub | none | `ABSENT` |

Domain events already cover the product loop Run 001 exercises. They do not cover the experiment envelope (run identity, purpose class, freeze hash, operator_action enum, intervention_state, seal, evaluation).

## What Run 001 can reconstruct today from specified domain facts

If a TEST/STAGING operator executes the released coordination loop on fixtures, an evaluator could later assemble:

- scenario-adjacent domain sequence from `CHECKIN_COMPLETED` → `SUPPORT_SIGNAL_CHANGED` → case/fulfillment events
- actor identity from event envelope `actor_type` / `actor_id`
- occurred_at timestamps
- build provenance if the admin/debug surface required by ENVIRONMENT.md §8 is present (runtime presence `NOT_COMPUTABLE`)
- `SUAS_ENV` from process configuration, not from the event envelope

That assembly is not a sealed `EvidenceArtifact`. Correlation across those events depends on `correlation_id`, which EVENT_MODEL marks optional.

## FR-T-OBS-002 candidate gaps (not applied)

Do not patch EVENT_MODEL in this change. `FR-T-SPEC-003` remains `BLOCKED` until limited-implementation authority.

Minimum fields Run 001 cannot honestly populate from existing catalogs without either (a) an off-band sealed artifact written by the operator or (b) a later additive EVENT_MODEL / evidence-store contract:

1. `run_id`, `artifact_id`, `scenario_id` as immutable identifiers
2. `purpose_class`
3. `configuration_revision` (frozen experiment hash)
4. `input_provenance` / `output_provenance` as required hashes
5. `operator_action` enum
6. `intervention_state` enum
7. `artifact_digest` at seal
8. run lifecycle audit names (`EVIDENCE_RUN_STARTED`, `EVIDENCE_RUN_STATE_CHANGED`, `EVIDENCE_RUN_SEALED`, or equivalent)

Optional Run 001 omissions that stay legal under D037_EVIDENCE.md:

- `model_provider_id` / `model_version` when the freeze uses fixture adapters only
- `confidence` as `null` + `SURFACE_ABSENT`
- `latency_ms`, `recovery_events` (OPTIONAL metrics)
- `evaluator_ref` until FR-4

`FR-T-OBS-002` remains `OPEN`. This file is its input, not its spec patch.

## Preconditions from D037_EVIDENCE.md §4.1 mapped to observability

| Precondition | Observability status |
|---|---|
| telemetry/audit write path enabled for the run | EVENT_MODEL requires append-only audit/domain stores; enablement in a named STAGING instance is `NOT_COMPUTABLE` |
| evidence destination available | `ABSENT` / `NOT_COMPUTABLE` — see [D037_INFRA_INVENTORY.md](D037_INFRA_INVENTORY.md) |
| known application commit, spec version, release manifest | specified as build provenance; emit path `NOT_COMPUTABLE` |
| synthetic dataset identity and hash | `PARTIAL` (fixture practice); no required event field |

## Result

| Claim | State |
|---|---|
| FR-T-OBS-001 written inventory | `DONE` 2026-09-17 |
| Any EvidenceArtifact field runtime-emitted | `NOT_COMPUTABLE` |
| Existing domain catalog sufficient to seal Run 001 without an evidence envelope | `NO` |
| Existing domain catalog sufficient to reconstruct the product loop inside Run 001 | `PARTIAL` |
| EVENT_MODEL change authorized | `NO` |
| FR-2 | remains `NOT_READY` |
