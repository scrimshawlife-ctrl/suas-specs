# D037_DRIFT_AUDIT.md — Cross-artifact consistency audit

**Decision:** D-037  
**Date:** `2026-09-17`  
**Scope:** this packet versus released `0.6.0` canon

## Method

Inspected repository canon listed in [D037_INDEX.md](D037_INDEX.md) before writing. Compared new IDs, environment semantics, decision boundaries, and evidence vocabulary against AGENTS.md, ENVIRONMENT.md, DECISIONS.md, TESTING.md, SKILLS.md, ROADMAP.md, ANALYTICS.md, and the D-035 evidence pattern.

## Findings repaired in-packet

| Risk | Handling |
|---|---|
| Funding language becoming product doctrine | Packet labeled overlay; opportunity assessments cannot write requirements |
| Duplicated evidence concepts | Extends evidence-gate / TESTING.md / D-035; does not rename product gates |
| Grant requirements leaking into runtime | No runtime tasks until owner limited authority |
| New `SUAS_ENV` values | Purpose class overlay instead of DEV/DEMO/FIELD env names |
| SPEC-019 consumed | Explicitly not consumed; D-037 is a decision packet |
| D-010 conflated with grants | Explicit separation |
| Metrics without data sources | Each metric classified; calibration and resource consumption stay NOT_COMPUTABLE / FUTURE |
| Fields runtime cannot produce | Optional / nullable; confidence may be `SURFACE_ABSENT` |
| Assumed cloud provider | NOT_COMPUTABLE; D-001 stays open |
| Assumed grant eligibility | Empty opportunity register |
| Implementation tasks without parents | Every FR-T-* cites an FR-R-* |
| Requirements without acceptance | FR-R-* map to §10 acceptance and workflows |

## Residual items requiring operator judgment

| Item | State |
|---|---|
| Promote SAM / `$300` from OPERATOR_ASSERTED to OBSERVED | needs owner artifacts |
| UEI, legal entity, credit provider, expiration | `NOT_COMPUTABLE` |
| Whether current `suas` can emit Run 001 fields | `NOT_COMPUTABLE` until FR-T-OBS-001 |
| Named evaluator roster | `NOT_COMPUTABLE` |
| Owner choice among ACCEPT_AS_SPECIFIED / limited authority / return / reject | `DECISION_PENDING` |
| Any production readiness gate | remains `NOT_READY` |

## Undefined terminology check

New terms introduced with packet-local definitions: `purpose class`, `OPERATOR_ASSERTED`, `SUAS-FUNDING-READINESS-001`, `SUAS-EVIDENCE-RUN-001`, `FR-1`–`FR-5`, `WF-FR-001`–`WF-FR-003`. They are not aliases of Veteran, Support Signal, Consent Grant, or product readiness gates.

## Inconsistent IDs

None detected against existing D-001–D-036 and SPEC-001–SPEC-019.

## Synthetic / field contamination

Packet forbids DEMO→RESEARCH and SYNTHETIC→FIELD relabeling. Run 001 is TEST/STAGING + CONTROLLED_EXPERIMENT only.

## Assumed capabilities not present

None claimed as AVAILABLE in the evidence matrix.

## Audit result

Packet is internally consistent as specification text. Terminal condition `SUAS_FUNDING_READINESS_SPECIFIED` is reachable after owner review of FR-1. FR-2–FR-5 remain `NOT_READY`.
