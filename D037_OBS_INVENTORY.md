# D037_OBS_INVENTORY.md — FR-T-OBS-001 field inventory

**Decision:** D-037  
**Task:** `FR-T-OBS-001`  
**Parent:** FR-R-004, FR-R-005  
**Date:** `2026-09-17`  
**Scope:** public contracts in `suas-specs` after PR #26 on `main` (`a390a36`)  
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
| `operator_ref` | optional | EVENT_MODEL `actor_id` + `actor_type` | `PARTIAL` | `NOT_COMPUTABLE` |
| `system_state` | optional | domain aggregate status on payloads | `PARTIAL` | `NOT_COMPUTABLE` |
| `confidence` | optional | SIGNAL_SCORING.md scoring basis; D037_EVIDENCE.md allows `SURFACE_ABSENT` | `PARTIAL` | `NOT_COMPUTABLE` |
| `operator_action` | required | responder/case commands exist; D-037 enum does not | `PARTIAL` | `NOT_COMPUTABLE` |
| `intervention_state` | required | human coordination is first-class; enum is D-037 only | `ABSENT` as a field | `NOT_COMPUTABLE` |
| `latency_ms` | optional | ANALYTICS.md / OPERATIONS.md intervals | `PARTIAL` | `NOT_COMPUTABLE` |
| `errors` | optional | no structured run-error array | `PARTIAL` | `NOT_COMPUTABLE` |
| `recovery_events` | optional | EVENT_MODEL §4 recovery/replay coverage | `PARTIAL` | `NOT_COMPUTABLE` |
| `resulting_state` | optional | domain event payloads carry canonical states | `PARTIAL` | `NOT_COMPUTABLE` |
| `evaluation_method` | optional | evidence-gate is a gate assessment, not EvaluationResult | `ABSENT` on domain events | `NOT_COMPUTABLE` |
| `evaluator_ref` | optional | none | `ABSENT` | `NOT_COMPUTABLE` |
| `artifact_digest` | required at seal | D-035 hash pattern only | `PARTIAL` | `NOT_COMPUTABLE` |
| `lineage` | optional | `causation_event_id` is event causality, not artifact lineage | `PARTIAL` | `NOT_COMPUTABLE` |
| `retention_class` | required | D-007 pending; D-037 uses `UNRESOLVED` | `SPECIFIED` as unresolved doctrine | `NOT_COMPUTABLE` |

## EvidenceRun lifecycle vs EVENT_MODEL

Domain events cover the product loop. They do not cover the experiment envelope.

Specified product-loop events: `CHECKIN_COMPLETED`, `SUPPORT_SIGNAL_CHANGED`, `CASE_CREATED`, `CASE_ASSIGNED`, `RESPONDER_CONTACT_LOGGED`, `SERVICE_REQUEST_*`, `SERVICE_ACCEPTED`, `SERVICE_FULFILLED`, `SERVICE_FAILED`, `CONSENT_GRANTED`, `CONSENT_REVOKED`, `FOLLOWUP_*`.

Absent experiment-envelope facts: run opened, freeze recorded, run READY/RUNNING, operator_action enum, run COMPLETED/FAILED/ABORTED/PARTIAL, evaluation attached, artifact sealed, persistence-failure stub.

## FR-T-OBS-002 candidate gaps (not applied)

1. `run_id`, `artifact_id`, `scenario_id`
2. `purpose_class`
3. `configuration_revision`
4. `input_provenance` / `output_provenance` hashes
5. `operator_action` enum
6. `intervention_state` enum
7. `artifact_digest` at seal
8. run lifecycle audit names

`FR-T-SPEC-003` remains `BLOCKED`. EVENT_MODEL is unchanged.

## Result

| Claim | State |
|---|---|
| FR-T-OBS-001 written inventory | `DONE` 2026-09-17 |
| Any EvidenceArtifact field runtime-emitted | `NOT_COMPUTABLE` |
| Domain catalog sufficient to seal Run 001 without an evidence envelope | `NO` |
| Domain catalog sufficient to reconstruct the product loop | `PARTIAL` |
| FR-2 | remains `NOT_READY` |
