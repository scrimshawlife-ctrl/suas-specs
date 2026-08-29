---
name: contract-validation
version: 1.0.0
kind: specification
status: active
authority: canonical-spec
inputs: [release_manifest, contract_identities, invariants, golden_vectors, implementation_behavior]
outputs: [contract_verdict]
fail_closed: true
self_test: skills/self-tests/contract-validation.yaml
---

# contract-validation

## Purpose
Validate deterministic SUAS domain and scoring contracts against exact released identities and invariants.

## Trigger
Use when validating scoring/questionnaire behavior, version pins, provenance/basis fields, missing-input rules, safety escalation, disabled modes, or any deterministic domain contract.

## Inputs
- Released spec version and manifest.
- Exact contract identities (for example questionnaire/scoring/schema versions).
- Acceptance criteria and golden vectors.
- Implementation or proposed behavior under review.

## Procedure
1. Read `AGENTS.md`, active release manifest, and all referenced contract sections.
2. Pin exact version identities before comparison.
3. Enumerate required inputs, optional inputs, missing-input behavior, mappings, escalation rules, and expected outputs.
4. Compare implementation/proposal behavior against each invariant.
5. Run or specify golden vectors and boundary cases.
6. Verify emitted provenance/basis fields correspond exactly to accepted inputs and active identities.
7. Verify disabled/unavailable modes are actually non-callable where required.
8. Treat semantic ambiguity as a spec gap; do not invent a corrective rule.

## Invocation example
`Validate sv-001 against qv-001 and the released manifest; return every invariant as PASS, FAIL, or NOT_COMPUTABLE and identify the minimum fix.`

## Output schema
```yaml
contract_id: string
spec_version: string
manifest: string
implementation_identity: string|null
checks:
  - invariant: string
    result: PASS|FAIL|NOT_COMPUTABLE
    evidence: string|null
mismatches: [string]
spec_gaps: [string]
verdict: CONFORMANT|NON_CONFORMANT|NOT_COMPUTABLE
minimum_fix_or_decision: [string]
```

## Prohibited actions
- Do not validate against draft/unreleased semantics as if they were authoritative.
- Do not ignore version mismatches.
- Do not patch semantic ambiguity in runtime.

## Self-test
Run `skills/self-tests/contract-validation.yaml`. The fixture must fail a provenance/basis mismatch and must not invent behavior for an unresolved semantic gap.

## Completion criteria
Complete only when every relevant invariant is classified and the verdict is reproducible from cited contract identities and evidence.