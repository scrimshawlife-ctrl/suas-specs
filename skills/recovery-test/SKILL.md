---
name: recovery-test
description: Check recovery evidence using approved synthetic fixtures.
version: 1.0.0
kind: specification
status: active
authority: canonical-spec
inputs: [recovery_contract, environment, backup_identity, restore_procedure, durability_expectations]
outputs: [recovery_evidence_contract]
fail_closed: true
self_test: skills/self-tests/recovery-test.yaml
---

# recovery-test

## Purpose
Define and assess backup/restore and durable-work recovery evidence without overstating production guarantees.

## Trigger
Use when a readiness gate requires recovery evidence, when validating backup/restore behavior, or when assessing whether migration rehearsal is sufficient.

## Inputs
- Governing recovery/readiness contract.
- Approved environment/target.
- Backup identity and restore procedure.
- Schema/build/config identities.
- Durable-job and idempotency expectations.

## Procedure
1. Read `AGENTS.md`, `ENVIRONMENT.md`, readiness/evidence contracts, and any recovery decisions.
2. Confirm the exercise target is approved and non-production unless explicit authority says otherwise.
3. Separate migration rehearsal from actual backup/restore evidence.
4. Record backup identity, source state, restore target, UTC start/end, and restoration duration.
5. Validate restored schema/version, required records, integrity constraints, and loss boundary.
6. Validate durable async work, replay safety, and idempotency after restoration.
7. Record failures, data loss, duplicate effects, or unresolved ambiguity.
8. Do not convert one exercise into an RTO/RPO/SLO claim unless canonical authority explicitly permits it.

## Invocation example
`Define the recovery evidence packet required for SPEC-018 and flag anything a migration rehearsal cannot satisfy.`

## Output schema
```yaml
exercise_id: string
environment: string
backup_id: string
restore_target: string
started_at_utc: string
ended_at_utc: string
duration_seconds: number
schema_identity: string
build_identity: string|null
integrity_result: PASS|FAIL|PARTIAL
loss_boundary: string|NOT_COMPUTABLE
durable_job_result: PASS|FAIL|NOT_APPLICABLE|NOT_COMPUTABLE
idempotency_result: PASS|FAIL|NOT_APPLICABLE|NOT_COMPUTABLE
findings: [string]
claims_authorized: [string]
claims_not_authorized: [string]
```

## Prohibited actions
- Do not call a migration rehearsal a restore exercise.
- Do not test against production without explicit authority.
- Do not infer RTO/RPO/SLO guarantees from incomplete evidence.

## Self-test
Run `skills/self-tests/recovery-test.yaml`. The fixture must classify migration-only evidence as insufficient for an actual restore requirement.

## Completion criteria
Complete only when restoration, integrity, loss boundary, and durable-work behavior are explicitly recorded or marked NOT_COMPUTABLE with missing evidence identified.