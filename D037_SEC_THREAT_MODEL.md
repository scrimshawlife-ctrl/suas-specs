# D037_SEC_THREAT_MODEL.md — FR-T-SEC-001

**Decision:** D-037  
**Task:** `FR-T-SEC-001`  
**Parent:** FR-R-011  
**Date:** `2026-09-17`  
**Scope:** evidence artifacts, grant exports, and the optional GCP evidence project  
**Does not expand collection.**  

This is a written review. It is not a pentest, not a FedRAMP package, and not a HIPAA analysis (D-006 remains open).

## Assets

| Asset | Sensitivity |
|---|---|
| Sealed `EvidenceRun` / `EvidenceArtifact` JSON | privileged operator material; synthetic fixtures only for Run 001 |
| Freeze hash + dataset hash | reconstruction keys |
| `EvaluationResult` | derived; same privilege |
| `ExperimentCostRecord` | operational; no secrets |
| Grant-reporting export | derived from sealed artifacts only |
| GCP evidence project (if later authorized) | isolated; no production secrets |

## Threats and handling

| ID | Threat | Handling already required |
|---|---|---|
| T-01 | Real veteran data lands in an evidence artifact | ENVIRONMENT.md + Run 001 synthetic-only rule |
| T-02 | Secrets copied into artifacts or cost records | D037_FUNDING_READINESS.md §7; destination README |
| T-03 | DEMO or LOCAL run relabeled FIELD | purpose-class + env freeze after `RUNNING` |
| T-04 | Artifact mutated after seal | immutability + successor `lineage` |
| T-05 | Public GCS ACL or public GitHub file with PII | no public ACL; Run 001 fixtures only; privileged-operator default |
| T-06 | Production service account bound to evidence project | GCP placement forbids shared prod billing/secrets |
| T-07 | Vertex used as Support Signal | GCP placement forbids safety-critical inference |
| T-08 | Grant export written from unsealed or cherry-picked trials | export only from sealed artifacts; negative results retained |
| T-09 | Operator legal name stored without retention decision | prefer pseudonymous `operator_ref`; D-007 still open |
| T-10 | Provider-raw model payload retained | D-035 posture; raw payloads stay out of domain evidence storage |

## Explicit non-work

- no new telemetry fields
- no new veteran attributes
- no production log drain into GCP
- no identity-provider change
- no claim that the evidence project is authorized or hardened

## Result

| Claim | State |
|---|---|
| FR-T-SEC-001 written review | `DONE` 2026-09-17 |
| Extra collection introduced | `NO` |
| FR-T-SEC-002 IAM/seal scheme | still `OPEN` |
