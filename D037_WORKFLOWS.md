# D037_WORKFLOWS.md — Workflows, state machines, contracts

**Decision:** D-037  
**Status:** `proposed` / not release-authoritative  
**Chain:** Journey → Workflow → State Transition → Contract → Acceptance Test → Implementation Task

## Workflows

The funding-readiness overlay adds three operator/admin workflows. None is a Veteran journey. None is callable from `/api/v0` until a later released contract says otherwise. Until then they are specification procedures executed by humans and spec agents.

---

## WF-FR-001 Controlled Evidence Run

**Stable ID:** `WF-FR-001`  
**Purpose:** Execute a reproducible SUAS run and produce a sealed evidence artifact.  
**Actors:** SUAS operator / researcher with privileged access to the declared environment.  
**Trigger:** Owner or authorized operator starts a planned run whose `experiment_id` is frozen.  
**Preconditions:** [D037_EVIDENCE.md](D037_EVIDENCE.md) §4.1.  
**Inputs:** `run_id`, `scenario_id`, frozen configuration hash, synthetic dataset hash, `SUAS_ENV`, purpose class `CONTROLLED_EXPERIMENT`.

### Happy path

1. Run state `PLANNED` → `CONFIGURED` when freeze hash is recorded.
2. `CONFIGURED` → `READY` when preconditions validate.
3. `READY` → `RUNNING` when the operator starts the scenario.
4. System records observation, output, confidence-or-absent, operator action, system action, outcome, telemetry.
5. `RUNNING` → `COMPLETED`.
6. Evaluator later moves `COMPLETED` → `EVALUATED` via WF-FR-002.
7. `EVALUATED` → `SEALED` when digest is written.

### Alternate paths

Accept / reject / modify / abstain / insufficient confidence / delayed response as in Evidence Run 001.

### Failure paths / recovery

Auth failure, provider failure, timeout, malformed response, inconsistent state, telemetry failure, persistence failure, operator abort.

- Persistence success after a domain failure → `FAILED` or `ABORTED`, still sealable.
- Persistence failure → `PARTIAL` stub plus successor if a later write succeeds.
- Operator abort → `ABORTED`.

### State transitions

```text
PLANNED → CONFIGURED → READY → RUNNING → COMPLETED | FAILED | ABORTED | PARTIAL
COMPLETED | FAILED | ABORTED | PARTIAL → EVALUATED → SEALED
```

No post-seal mutation. Corrections create a successor artifact with `lineage`.

### Terminal states

`SEALED`, or an unsealed `PARTIAL` that cannot be persisted. The latter remains evidence of persistence failure.

### Side effects

Synthetic domain records in TEST/STAGING. No real veteran data. No real external effects. Credit consumption if the environment uses credited resources; record via cost schema.

### Invariants

- purpose class cannot change after `RUNNING`;
- `SUAS_ENV` cannot change after `RUNNING`;
- operator action is recorded even when `NONE`;
- failed runs remain representable.

### Permissions

Privileged operator. Not Veteran. Not Organization Administrator by default.

### Observability / audit

Start, state change, operator action, seal, and abort emit audit events using existing privileged-admin audit vocabulary where possible. New event names, if required, wait for a released EVENT_MODEL change.

### Acceptance criteria

- happy path and at least one failure path are specified;
- reconstruction requirement in D037_EVIDENCE.md §4.5 is testable after a run exists;
- no production-unavailable surface is enabled to make the run look better.

### Dependencies

ENVIRONMENT.md, TESTING.md fixtures, evidence-gate skill, D037_EVIDENCE.md.

### Unresolved

Evidence store URI, observability vendor, whether current `suas` audit events can carry all fields without an API change (`NOT_COMPUTABLE` until runtime inventory).

---

## WF-FR-002 Evidence Evaluation

**Stable ID:** `WF-FR-002`  
**Purpose:** Evaluate a completed (or failed/aborted/partial) run against declared metrics without modifying source evidence.  
**Actors:** authorized evaluator distinct from the run operator when independence is claimed.  
**Trigger:** a run in `COMPLETED|FAILED|ABORTED|PARTIAL`.  
**Preconditions:** source artifact readable; metric definitions pinned; evaluator identity recorded.  
**Inputs:** `run_id`, `artifact_id`, metric ID set.

### Happy path

1. Evaluator reads sealed or pre-seal artifact.
2. Evaluator computes REQUIRED metrics that the artifact can support.
3. Evaluator records `EvaluationResult` as a derived artifact.
4. Run state → `EVALUATED` then `SEALED` if not already sealed.

### Alternate paths

Some OPTIONAL metrics omitted with explicit `NOT_COMPUTED`. Independent evaluator unavailable → evaluation marked `OPERATOR_SELF` and cannot claim independence.

### Failure paths

Missing required field → completeness metric fails; evaluation still recorded. Evaluator attempts to edit source artifact → rejected by invariant.

### Terminal states

`EVALUATED` / `SEALED` with or without independent evaluator.

### Side effects

Derived evaluation artifact only.

### Invariants

Source artifact bytes unchanged. Negative results retained.

### Permissions

Evaluator role. Owner may evaluate FR-1 specification text; FR-3/FR-4 require a run.

### Acceptance criteria

EvaluationResult schema validates. Required metrics each have a value or an explicit `NOT_COMPUTABLE` reason.

### Dependencies

D037_EVIDENCE.md §5, evidence-gate skill.

### Unresolved

Named evaluator roster (`NOT_COMPUTABLE`).

---

## WF-FR-003 Funding Opportunity Assessment

**Stable ID:** `WF-FR-003`  
**Purpose:** Compare an external opportunity against current SUAS capabilities and evidence without mutating product requirements.  
**Actors:** authorized project / research administrator.  
**Trigger:** discovery of an opportunity or a scheduled re-verification.  
**Preconditions:** source URL or archived reference available for any status other than `NOT_COMPUTABLE`.  
**Inputs:** opportunity fields in [D037_OPPORTUNITY_MODEL.md](D037_OPPORTUNITY_MODEL.md).

### Happy path

`DISCOVERED` → `SCREENING` → `ELIGIBILITY_VERIFIED` → `EVIDENCE_GAP_ANALYSIS` → `READY|NOT_READY|INELIGIBLE|EXPIRED`.

### Alternate paths

Missing source → remain `NOT_COMPUTABLE`. Opportunity expires during screening → `EXPIRED`.

### Failure paths

Source disappears → status returns to `NOT_COMPUTABLE` with reason. Attempt to write a product requirement from the assessment → rejected; gap recorded only.

### Terminal states

`READY`, `NOT_READY`, `INELIGIBLE`, `EXPIRED`. `READY` means "assessment complete and evidence coverage is sufficient to *consider* an application." It does not mean GRANT_READY or GRANT_ELIGIBLE unless eligibility_status is `ELIGIBLE` *and* FR-5 is `PASS`. Today both are unmet.

### Side effects

Assessment record only. No runtime change.

### Invariants

Eligibility vocabulary from §3 of the opportunity model. Product chain remains unwritable from this workflow.

### Permissions

Project/research administrator. Not a Veteran path.

### Acceptance criteria

An assessment with no source cannot leave `NOT_COMPUTABLE`. An assessment cannot add a row to DECISIONS.md.

### Dependencies

D037_OPPORTUNITY_MODEL.md, D037_EVIDENCE.md matrix.

### Unresolved

Legal applicant entity (`NOT_COMPUTABLE`).

---

## State machines

### Evidence run

```text
PLANNED
  → CONFIGURED
  → READY
  → RUNNING
  → COMPLETED | FAILED | ABORTED | PARTIAL
  → EVALUATED
  → SEALED
```

### Opportunity assessment

```text
DISCOVERED
  → SCREENING
  → ELIGIBILITY_VERIFIED
  → EVIDENCE_GAP_ANALYSIS
  → READY | NOT_READY | INELIGIBLE | EXPIRED
```

`NOT_COMPUTABLE` is an eligibility value, not a workflow state. A discovered opportunity with no source stays in `SCREENING` with eligibility `NOT_COMPUTABLE`.

---

## Contracts

Machine-readable drafts live beside this packet as documentation schemas. They are not runtime validators until a released task says schema work includes a reference implementation.

| Contract | Schema version | Path |
|---|---|---|
| EvidenceRun | `evidence-run.v0` | [schemas/funding-readiness/evidence-run.v0.json](schemas/funding-readiness/evidence-run.v0.json) |
| EvidenceArtifact | `evidence-artifact.v0` | [schemas/funding-readiness/evidence-artifact.v0.json](schemas/funding-readiness/evidence-artifact.v0.json) |
| EvaluationResult | `evaluation-result.v0` | [schemas/funding-readiness/evaluation-result.v0.json](schemas/funding-readiness/evaluation-result.v0.json) |
| MetricDefinition | `metric-definition.v0` | [schemas/funding-readiness/metric-definition.v0.json](schemas/funding-readiness/metric-definition.v0.json) |
| ExperimentCostRecord | `experiment-cost-record.v0` | [schemas/funding-readiness/experiment-cost-record.v0.json](schemas/funding-readiness/experiment-cost-record.v0.json) |
| FundingOpportunityAssessment | `funding-opportunity-assessment.v0` | [schemas/funding-readiness/funding-opportunity-assessment.v0.json](schemas/funding-readiness/funding-opportunity-assessment.v0.json) |

Requirements common to all six: versioned, deterministic, provenance-aware, explicit optionality, no phantom defaults, immutable identifiers, lineage where a successor exists.
