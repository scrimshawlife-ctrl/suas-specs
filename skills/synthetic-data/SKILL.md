# synthetic-data

## Purpose
Define reproducible, privacy-safe, deterministic datasets for SUAS development, testing, review, and evidence generation.

## Trigger
Use when creating fixtures, golden datasets, provider sandbox inputs, aggregate-only dry runs, deletion/export tests, or any evidence that depends on exact test data.

## Inputs
- Governing spec/test/evidence contract.
- Environment and data-use restrictions.
- Required entities, edge cases, mappings, projections, and expected outputs.
- Dataset version/identity requirements.

## Procedure
1. Read `AGENTS.md`, `ENVIRONMENT.md`, relevant domain specs, and the governing test/evidence contract.
2. Enumerate required positive, negative, boundary, NO_HIT/empty, malformed, replay, duplicate, and cross-tenant cases.
3. Define deterministic IDs and values with no real veteran or production data.
4. Define deterministic mapping/projection rules and expected outputs.
5. Record dataset identity/version, generator identity if used, exact cutoff where applicable, and cryptographic hash.
6. Ensure policy-sensitive attributes such as consent, retention, deletion, export, and reporting eligibility are represented where required.
7. Verify the fixture can be regenerated identically from checked-in definitions or a deterministic generator.
8. Explicitly state that synthetic evidence does not authorize production use.

## Output schema
```yaml
dataset_id: string
version: string
environment: LOCAL|TEST|STAGING|SANDBOX
source: checked_in_fixture|deterministic_generator
generator_id: string|null
dataset_hash: string
mapping_id: string|null
mapping_hash: string|null
cutoff_utc: string|null
cases:
  positive: [string]
  negative: [string]
  boundary: [string]
  no_hit_empty: [string]
  malformed: [string]
  replay_duplicate: [string]
  cross_tenant: [string]
expected_outputs_reference: string
production_authority: false
```

## Prohibited actions
- No real veteran or production data in prohibited environments.
- No nondeterministic fixture generation without an explicitly pinned seed and reproducible procedure.
- No production-readiness inference from synthetic-only evidence.

## Completion criteria
Complete only when the dataset is reproducible, hashed, covers all contract-required cases, and its expected outputs/projections are explicit.