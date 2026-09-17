# D037_OPPORTUNITY_MODEL.md — Funding opportunity assessment

**Decision:** D-037  
**Status:** `proposed` / not release-authoritative  
**Placement:** outside the product requirement chain  
**Runtime:** none

## 1. Purpose

Give SUAS a lightweight way to compare an external opportunity against current capabilities and sealed evidence. The assessment cannot write product requirements, close decisions, or enable surfaces.

Do not hard-code current grant opportunities into architecture.

## 2. Schema fields

Schema version: `funding-opportunity-assessment.v0`.

| Field | Cardinality | Rule |
|---|---|---|
| `assessment_id` | required | immutable |
| `opportunity_id` | required | stable local id |
| `agency` | optional | `NOT_COMPUTABLE` if unknown |
| `program` | optional | |
| `source_url` | required for any eligibility conclusion | |
| `publication_date` | optional | |
| `deadline` | optional | |
| `applicant_eligibility` | optional | quote or paraphrase with source |
| `technical_topic` | optional | |
| `research_alignment` | optional | reference released SUAS capabilities only |
| `required_evidence` | optional | list |
| `required_partners` | optional | |
| `cost_share_requirement` | optional | |
| `trl_expectation` | optional | |
| `data_management_requirements` | optional | |
| `security_requirements` | optional | |
| `reporting_requirements` | optional | |
| `current_suas_evidence_coverage` | required | references sealed artifacts or `NONE` |
| `evidence_gaps` | required | |
| `administrative_gaps` | required | include UEI/`NOT_COMPUTABLE` rows when relevant |
| `eligibility_status` | required | see §3 |
| `workflow_status` | required | state machine in [D037_WORKFLOWS.md](D037_WORKFLOWS.md) |
| `provenance` | required | who assessed, source hash or retrieval date |
| `last_verified_date` | required | |
| `schema_version` | required | `funding-opportunity-assessment.v0` |

## 3. Eligibility vocabulary

Exactly these values:

- `ELIGIBLE`
- `POTENTIALLY_ELIGIBLE`
- `INELIGIBLE`
- `NOT_COMPUTABLE`

No eligibility conclusion may be made without `source_url` (or an equivalent archived source reference) and an applicant-eligibility excerpt. Absent those, the status is `NOT_COMPUTABLE`.

`POTENTIALLY_ELIGIBLE` means the source text does not rule the applicant out and at least one administrative or evidence gap remains. It is not a green light.

## 4. Mutation ban

An assessment may list a product gap. The gap is information. Promoting that gap into a requirement requires the ordinary specify → accept → release path and an explicit owner decision. Opportunity text is never a hidden source of product doctrine.

## 5. Current register

Empty. No opportunity has been assessed in this repository.

| opportunity_id | eligibility_status | workflow_status | last_verified_date |
|---|---|---|---|
| — | `NOT_COMPUTABLE` | — | — |
