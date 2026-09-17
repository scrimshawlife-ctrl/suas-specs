# D037_TASKS.md — Derived implementation tasks

**Decision:** D-037  
**Status:** `accepted specification` / no runtime authority  
**Owner settlement:** `ACCEPT_AS_SPECIFIED` 2026-09-17 on [PR #25](https://github.com/scrimshawlife-ctrl/suas-specs/pull/25)  
**Rule:** no task without a specification parent. No runtime work until owner option 2 in [D037_FUNDING_READINESS.md](D037_FUNDING_READINESS.md) §12 is recorded in a later qualifier.

Lane codes: `SPEC`, `INFRA`, `OBSERVABILITY`, `SECURITY`, `EXPERIMENT`, `EVALUATION`, `FUNDING`.

## SPEC

| ID | Task | Parent | Acceptance | State |
|---|---|---|---|---|
| FR-T-SPEC-001 | Keep this packet consistent after owner comments | FR-R-014 | drift audit updated | `DONE` 2026-09-17 |
| FR-T-SPEC-002 | After owner `ACCEPT_AS_SPECIFIED`, add D-037 to a future release decision ledger without claiming runtime authority | FR-R-001 | ledger row only | `OPEN` / `FUTURE` |
| FR-T-SPEC-003 | If EVENT_MODEL needs new audit names for run state changes, specify them here first | FR-R-013 | spec change before code | `BLOCKED` until limited-implementation authority |

## INFRA

| ID | Task | Parent | Acceptance | State |
|---|---|---|---|---|
| FR-T-INFRA-001 | Inventory whether existing `suas` STAGING can host Run 001 without a new vendor | FR-R-002, FR-R-003 | written inventory | `DONE` |
| FR-T-INFRA-002 | Declare evidence destination URI once a store exists | FR-R-004 | URI + access policy | `PARTIAL` — convention + interim repo path in [D037_EVIDENCE_DESTINATION.md](D037_EVIDENCE_DESTINATION.md); live `gs://` `NOT_COMPUTABLE` |
| FR-T-INFRA-003 | Specify which architecture parts belong on Google Cloud | FR-R-016–FR-R-018 | placement map; D-001 stays open | `DONE` |

## OBSERVABILITY

| ID | Task | Parent | Acceptance | State |
|---|---|---|---|---|
| FR-T-OBS-001 | Inventory EvidenceArtifact fields vs public contracts | FR-R-004, FR-R-005 | field table | `DONE` |
| FR-T-OBS-002 | Specify only the missing fields that Run 001 requires | FR-R-013 | spec patch, then later runtime | `OPEN` |

## SECURITY

| ID | Task | Parent | Acceptance | State |
|---|---|---|---|---|
| FR-T-SEC-001 | Threat-model evidence artifacts and grant exports | FR-R-011 | written review; no extra collection | `DONE` as [D037_SEC_THREAT_MODEL.md](D037_SEC_THREAT_MODEL.md) |
| FR-T-SEC-002 | IAM / integrity scheme for seal and successor lineage | FR-R-004 | digest + access control described | `OPEN` |

## EXPERIMENT

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-EXP-001 | Freeze Run 001 configuration after FR-2 preconditions exist | FR-R-003 | hash recorded |
| FR-T-EXP-002 | Execute Run 001 happy path plus at least one failure path | FR-R-003, FR-R-006 | sealed artifacts |
| FR-T-EXP-003 | Record cost evidence if credited resources were used | FR-R-012 | cost record or explicit `$0` / free-tier note |

## EVALUATION

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-EVAL-001 | Compute REQUIRED metrics for the Run 001 cohort | FR-R-007 | EvaluationResult |
| FR-T-EVAL-002 | Independent evaluation if an evaluator distinct from the operator is available | FR-4 | independence flag accurate |

## FUNDING

| ID | Task | Parent | Acceptance | State |
|---|---|---|---|---|
| FR-T-FUND-001 | Attach SAM / UEI artifacts when the owner provides them | FR-R-001 | rows promote to OBSERVED | `OPEN` |
| FR-T-FUND-002 | Attach credit-provider rules when the owner provides them | FR-R-002 | SKUs / expiration / balance no longer NOT_COMPUTABLE | `OPEN`; provider name `OPERATOR_ASSERTED` Google Cloud |
| FR-T-FUND-003 | Assess a named opportunity only from a source URL | FR-R-009 | WF-FR-003 record | `OPEN` |

## Runtime repositories

`suas`, `suas-ios`, and `suas-android` receive **no** tasks from this packet.

## Gate application

| Gate | Current |
|---|---|
| FR-1 | `PASS` 2026-09-17 |
| FR-2 | `NOT_READY` |
| FR-3 | `NOT_READY` |
| FR-4 | `NOT_READY` |
| FR-5 | `NOT_READY` |
