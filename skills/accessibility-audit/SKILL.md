---
name: accessibility-audit
description: Audit accessibility evidence against the released SUAS contract.
version: 1.0.0
kind: specification
status: active
authority: canonical-spec
inputs: [ui_authority, surfaces, build_identity, automated_criteria, human_criteria]
outputs: [accessibility_evidence_contract]
fail_closed: true
self_test: skills/self-tests/accessibility-audit.yaml
---

# accessibility-audit

## Purpose
Define accessibility verification and evidence requirements for released SUAS client surfaces.

## Trigger
Use when a client/UI route changes, when staging evidence requires accessibility review, or when evaluating whether automated checks are sufficient.

## Inputs
- Released UI/MVP reference and safety-copy requirements.
- Route/surface inventory.
- Build/environment identity.
- Required automated and human-review criteria.

## Procedure
1. Read `AGENTS.md`, `MVP_REFERENCE.md`, accessibility/readiness requirements, and applicable safety-copy decisions.
2. Resolve the exact routes/surfaces and build identity under review.
3. Define automated checks for semantics, names/labels, contrast, structural errors, and other machine-testable criteria.
4. Define human checks for keyboard/focus, reading/order comprehension, zoom/reflow, reduced motion where applicable, error communication, and safety-copy presentation.
5. Record viewport/device, browser/client, tool/version, environment, and evidence artifact.
6. Separate automated result from human-review disposition.
7. Do not settle a human-review gate from automation alone.

## Invocation example
`Define the STAGING accessibility evidence contract for onboarding and crisis-copy surfaces, separating automated from human review.`

## Output schema
```yaml
audit_id: string
build_identity: string
environment: string
surfaces: [string]
viewport_or_device: string
automated:
  tool: string
  version: string
  result: PASS|FAIL|PARTIAL|NOT_COMPUTABLE
  evidence: string|null
human_review:
  reviewer: string|null
  completed: boolean
  result: PASS|FAIL|PARTIAL|NOT_COMPUTABLE
  evidence: string|null
findings: [string]
verdict: PASS|FAIL|PARTIAL|NOT_COMPUTABLE
```

## Prohibited actions
- Do not claim full accessibility conformance from automated tooling alone.
- Do not omit safety-copy presentation where it is part of the released surface.
- Do not test a stale build and apply the result to a newer one without explicit equivalence evidence.

## Self-test
Run `skills/self-tests/accessibility-audit.yaml`. The fixture must prevent an automated PASS from satisfying an outstanding human-review requirement.

## Completion criteria
Complete only when automated and human-review requirements are separately classified with reproducible provenance.