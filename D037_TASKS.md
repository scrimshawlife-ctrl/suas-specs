# D037_TASKS.md — Derived implementation tasks

**Decision:** D-037  
**Status:** `proposed`  
**Rule:** no task without a specification parent. No runtime work until owner option 2 in [D037_FUNDING_READINESS.md](D037_FUNDING_READINESS.md) §12.

Lane codes: `SPEC`, `INFRA`, `OBSERVABILITY`, `SECURITY`, `EXPERIMENT`, `EVALUATION`, `FUNDING`.

## SPEC

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-SPEC-001 | Keep this packet consistent after owner comments | FR-R-014 | drift audit updated |
| FR-T-SPEC-002 | After owner `ACCEPT_AS_SPECIFIED`, add D-037 to a future release decision ledger without claiming runtime authority | FR-R-001 | ledger row only |
| FR-T-SPEC-003 | If EVENT_MODEL needs new audit names for run state changes, specify them here first | FR-R-013 | spec change before code |

## INFRA

Blocked on owner limited-implementation authority and on D-001 remaining open.

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-INFRA-001 | Inventory whether existing `suas` STAGING can host Run 001 without a new vendor | FR-R-002, FR-R-003 | written inventory; no silent vendor pick |
| FR-T-INFRA-002 | Declare evidence destination URI once a store exists | FR-R-004 | URI + access policy |

## OBSERVABILITY

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-OBS-001 | Inventory which EvidenceArtifact fields current logs/audit events already emit | FR-R-004, FR-R-005 | field-by-field table labeled OBSERVED/NOT_COMPUTABLE |
| FR-T-OBS-002 | Specify only the missing fields that Run 001 requires | FR-R-013 | spec patch, then later runtime |

## SECURITY

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-SEC-001 | Threat-model evidence artifacts and grant exports | FR-R-011 | written review; no extra collection |
| FR-T-SEC-002 | IAM / integrity scheme for seal and successor lineage | FR-R-004 | digest + access control described |

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

Documentation only.

| ID | Task | Parent | Acceptance |
|---|---|---|---|
| FR-T-FUND-001 | Attach SAM / UEI artifacts when the owner provides them | FR-R-001 | rows promote from OPERATOR_ASSERTED / NOT_COMPUTABLE to OBSERVED |
| FR-T-FUND-002 | Attach credit-provider rules when the owner provides them | FR-R-002 | provider no longer NOT_COMPUTABLE |
| FR-T-FUND-003 | Assess a named opportunity only from a source URL | FR-R-009 | WF-FR-003 record |

## Runtime repositories

`suas`, `suas-ios`, and `suas-android` receive **no** tasks from this packet. A later released limited-authority qualifier may create them. Coding agents must not open product PRs to "support grants."

## Gate application

| Gate | Tasks that can move it | Current |
|---|---|---|
| FR-1 | this packet + owner review | specification text present; owner state `NOT_COMPUTABLE` |
| FR-2 | FR-T-INFRA-001, FR-T-OBS-001, FR-T-EXP-001 | `NOT_READY` |
| FR-3 | FR-T-EXP-002 | `NOT_READY` |
| FR-4 | FR-T-EVAL-001, FR-T-EVAL-002 | `NOT_READY` |
| FR-5 | FR-3 + FR-4 + FR-T-FUND-001 at OBSERVED | `NOT_READY` |
