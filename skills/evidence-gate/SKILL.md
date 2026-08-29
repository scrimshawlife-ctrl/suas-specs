---
name: evidence-gate
version: 1.0.0
kind: specification
status: active
authority: canonical-spec
inputs: [gate_id, release_manifest, evidence_contract, evidence_artifacts, owner_authority]
outputs: [gate_assessment]
fail_closed: true
self_test: skills/self-tests/evidence-gate.yaml
---

# evidence-gate

## Purpose
Determine whether a SUAS decision, feature, pilot, reporting surface, or production gate has sufficient evidence and explicit authority to change state.

## Trigger
Use when a task asks whether something is ready, accepted, releasable, pilotable, production-ready, enabled, or blocked; when assembling owner evidence; or when evidence may have gone stale after code/spec/config changes.

## Canonical inputs
- Governing decision/gate identifier.
- Active released stack and release manifest.
- Required evidence contract and named decision authority.
- Evidence references/hashes, timestamps/cutoffs, build/schema/config identities, environment, scope, and constraints.

## Procedure
1. Read `AGENTS.md`, `HANDOFF.md`, active release manifest, and the governing decision/evidence contract.
2. Resolve the exact gate state vocabulary and required owner/authority.
3. Inventory each required evidence item and its provenance.
4. Validate freshness against current code, schema, config, fixtures, dependencies, and environment.
5. Classify each item as PRESENT_VALID, PRESENT_STALE, PRESENT_CONTRADICTORY, or MISSING.
6. Determine whether the gate is IMPLEMENTED, VERIFIED, ACCEPTED, RELEASED, NOT_READY, NOT_COMPUTABLE, or DECISION_PENDING.
7. Never infer acceptance from merged code, green CI, or artifact existence.
8. If owner settlement is required, produce the smallest complete decision packet and preserve all blocked/disabled states until settlement.

## Invocation example
`Assess D-007 using the current release manifest and evidence packet; return only the gate assessment and missing minimum actions.`

## Prohibited actions
- Do not create authority from implementation state.
- Do not silently treat stale evidence as current.
- Do not enable production/pilot/reporting behavior without released authority.

## Output schema
```yaml
gate_id: string
status: IMPLEMENTED|VERIFIED|ACCEPTED|RELEASED|NOT_READY|NOT_COMPUTABLE|DECISION_PENDING
owner:
  name: string|null
  role: string|null
required_evidence:
  - id: string
    state: PRESENT_VALID|PRESENT_STALE|PRESENT_CONTRADICTORY|MISSING
    reference: string|null
    hash: string|null
    observed_at_utc: string|null
scope: string
constraints: [string]
stale_due_to: [string]
missing: [string]
next_minimum_action: [string]
```

## Self-test
Run `skills/self-tests/evidence-gate.yaml`. The fixture must prove that green CI plus merged code cannot yield ACCEPTED or RELEASED when owner settlement is missing.

## Completion criteria
Complete only when every required evidence item is classified, authority is resolved, and the resulting gate state is explicit and reproducible.