# SUAS agent skill execution framework

This framework applies to every project-local skill under `skills/*/SKILL.md`.

## Required SKILL.md frontmatter

```yaml
---
name: <kebab-case>
version: 1.0.0
kind: specification|runtime
status: active
authority: canonical-spec|released-runtime-conformance
inputs: [<logical input names>]
outputs: [<logical output names>]
fail_closed: true
self_test: skills/self-tests/<name>.yaml
---
```

## Execution contract

1. Resolve canonical authority before acting.
2. Validate required inputs. Missing authority-critical input returns `NOT_COMPUTABLE`; do not guess.
3. Execute only the procedure declared by the skill and any explicitly composed skills.
4. Preserve `OBSERVED` versus `INFERRED` provenance.
5. Emit the skill-specific output plus the common result envelope below.
6. Run the declared self-test fixture when the skill itself changes or when its output contract changes.
7. A passing self-test proves the skill contract is internally executable; it does not settle a product/readiness gate.

## Common result envelope

```yaml
skill:
  name: string
  version: string
execution_id: string
executed_at_utc: string
authority:
  repository: string
  release_or_manifest: string|null
inputs_resolved: boolean
result: PASS|FAIL|PARTIAL|NOT_COMPUTABLE|DECISION_PENDING
observed: [string]
inferred: [string]
evidence: [string]
missing: [string]
warnings: [string]
```

## Composition

Composition is explicit. A skill may call another skill only when the router or governing procedure names that dependency. Downstream skills must not silently strengthen an upstream verdict.

Recommended order where applicable:

`synthetic-data -> contract-validation -> adversarial-testing/accessibility-audit/recovery-test -> evidence-gate`

## Self-test rule

Each `skills/self-tests/<name>.yaml` fixture contains:

- `skill`
- `scenario`
- `given`
- `expect`
- `must_not`

A self-test passes only if every `expect` condition is satisfied and every `must_not` condition remains false.