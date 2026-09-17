# D037_EVIDENCE_DESTINATION.md — FR-T-INFRA-002 destination convention

**Decision:** D-037  
**Task:** `FR-T-INFRA-002`  
**Date:** `2026-09-17`  
**Spend authority:** none  
**Runtime authority:** none  

Declares where sealed evidence lives. Does not create a bucket, project, or IAM binding.

## 1. Two destinations

| Class | URI / path | Status |
|---|---|---|
| Interim operator store | `evidence/runs/{experiment_id}/{run_id}/` in this repository | `SPECIFIED` now |
| Preferred credit-backed store | isolated Google Cloud Storage bucket in the evidence-plane project | pattern `SPECIFIED`; live bucket `NOT_COMPUTABLE` |

Run 001 may seal into the interim store without GCP. Copy into GCS later if a project is authorized.

A destination convention is not a live URI. FR-2 stays `NOT_READY` until a named run can actually write one of these paths.

## 2. Interim repository layout

```text
evidence/runs/
  SUAS-EVIDENCE-RUN-001/
    README.md
    {run_id}/
      EvidenceRun.json
      EvidenceArtifact.json
      EvaluationResult.json        # optional, derived
      ExperimentCostRecord.json    # optional; `$0` / free-tier allowed
      freeze.sha256
      dataset.sha256
```

Rules:

1. Files validate against `schemas/funding-readiness/*`.
2. No secrets, no real veteran data, no provider-raw payloads.
3. Sealed objects are not rewritten. Corrections add a successor directory with `lineage`.
4. `README.md` under the experiment id lists run ids and terminal states only.

## 3. GCS pattern (not a live bucket)

```text
gs://suas-evidence-{project_token}/runs/{experiment_id}/{run_id}/{artifact_id}.json
```

| Token | Value |
|---|---|
| `project_token` | `NOT_COMPUTABLE` until a project id is recorded |
| `experiment_id` | `SUAS-EVIDENCE-RUN-001` for the first protocol |
| `run_id` | immutable run identifier |
| `artifact_id` | immutable artifact identifier |

Access policy when a bucket exists:

- uniform bucket-level access
- principals = privileged operators only
- no public ACLs
- no production service accounts
- object versioning on
- `retention_class=UNRESOLVED` in the JSON, independent of bucket retention

The live `gs://` URI is written into this file in the same commit that records the project id. Until then the pattern is the specification and the URI is `NOT_COMPUTABLE`.

## 4. Result

| Claim | State |
|---|---|
| Destination *convention* specified | `DONE` |
| Interim repo path specified | `DONE` |
| Live GCS URI | `NOT_COMPUTABLE` |
| Bucket created | `NO` |
| FR-T-INFRA-002 | `PARTIAL` |
| FR-2 | `NOT_READY` |
