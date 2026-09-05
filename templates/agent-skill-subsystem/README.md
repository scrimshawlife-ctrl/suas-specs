# Reusable Agent Skill Subsystem Template

This template generalizes the SUAS project-local agent skill architecture for reuse across other repositories.

## Goal

Provide deterministic, reviewable, self-validating agent skills that can be discovered by agents, composed safely, and enforced in CI.

## Canonical layout

```text
SKILLS.md
skills/
  README.md
  FRAMEWORK.md
  schemas/
    result-envelope.schema.json
  templates/
    result-envelope.yaml
  self-tests/
    <skill-name>.yaml
  <skill-name>/
    SKILL.md
scripts/
  validate-skills.py
.github/
  workflows/
    skills-validate.yml
```

## SKILL.md contract

Each skill MUST include YAML frontmatter with:

```yaml
---
name: <skill-name>
description: "Use when <trigger>. <What this skill does; non-empty, at most 1024 characters>."
version: 1.0.0
kind: specification|runtime
status: active
authority: <repo-specific-authority-label>
inputs: [<declared-inputs>]
outputs: [<declared-outputs>]
fail_closed: true
self_test: skills/self-tests/<skill-name>.yaml
---
```

Each skill MUST contain these sections:

1. `## Purpose`
2. `## Trigger`
3. `## Inputs` or `## Canonical inputs`
4. `## Procedure`
5. `## Prohibited actions` where relevant
6. `## Output schema`
7. `## Completion criteria`
8. `## Invocation example`
9. `## Self-test`

## Execution rules

- Read repository authority files before execution (`AGENTS.md`, `CONTEXT.md`, release manifest, or equivalent).
- Separate `OBSERVED` facts from `INFERRED` conclusions.
- Missing or insufficient evidence MUST produce `NOT_COMPUTABLE` or the repository's canonical pending state.
- A downstream skill MUST NOT strengthen an upstream verdict.
- Skills MAY reduce ambiguity; they MUST NOT create authority.
- Evidence-producing skills MUST emit enough provenance for independent reproduction.
- Runtime skills MUST bind evidence to current commit/build/schema/environment identity.
- Stale evidence MUST be invalidated after material code, schema, configuration, fixture, dependency, or environment changes.

## Shared result envelope

All skill outputs SHOULD embed or map to the shared result envelope:

```yaml
skill: string
skill_version: string
kind: specification|runtime
status: PASS|FAIL|PARTIAL|NOT_COMPUTABLE|DECISION_PENDING
observed: [string]
inferred: [string]
provenance:
  repository: string
  commit: string|null
  build: string|null
  schema: string|null
  environment: string|null
evidence: [string]
missing: [string]
next_minimum_action: [string]
```

The exact schema may be extended per repository but SHOULD remain backward-compatible.

## Self-test contract

Each skill MUST have one or more fixture-based self-tests that target the failure mode the skill exists to prevent.

Example:

```yaml
skill: evidence-gate
scenario: merged code and green CI without required owner settlement
given:
  code_merged: true
  ci_green: true
  owner_disposition: null
expect:
  status: DECISION_PENDING
must_not:
  - status_is_ACCEPTED
  - status_is_RELEASED
```

Self-tests SHOULD validate behavior, not only document examples.

## Router contract

`skills/README.md` MUST map common task intents to the applicable skill package(s). Example:

```text
readiness / release / pilot / enablement -> evidence-gate
fixture / golden dataset / synthetic run -> synthetic-data
backup / restore / recovery evidence -> recovery-test
deterministic contract / golden vector -> contract-validation
negative path / tenant isolation / fail-closed -> adversarial-testing
UI accessibility / staging a11y evidence -> accessibility-audit
```

Composition SHOULD be explicit. Example:

```text
synthetic-data -> contract-validation -> adversarial-testing -> evidence-gate
```

The final skill in a chain MUST NOT upgrade an earlier unresolved state.

## CI enforcement

Add a dependency-light validator (Python standard library is sufficient) that fails when:

- a required skill package is missing;
- YAML frontmatter is absent or malformed;
- required metadata differs from repository policy;
- `fail_closed` is not true;
- a declared self-test is missing;
- a self-test references the wrong skill or has no explicit expected outcome;
- required procedural sections are missing;
- the router omits a registered skill;
- shared schema/template/framework artifacts are missing;
- runtime skills do not bind outputs to runtime provenance.

Run the validator on pull requests touching `skills/**`, `SKILLS.md`, the validator, or the workflow itself. Running it on pushes to the default branch is recommended.

## Adoption procedure

1. Copy this layout into the target repository.
2. Define the repository-specific authority label(s).
3. Identify 3–8 recurring agent workflows that deserve first-class skills.
4. Write each skill as a deterministic behavioral contract.
5. Add one self-test for the primary failure mode of each skill.
6. Add the router and shared result envelope.
7. Add CI validation.
8. Run the validator before treating the subsystem as active.
9. Add new skills only when they encode recurring, materially useful behavior.

## Reference implementation

The canonical reference implementation for this template is the SUAS pair:

- `scrimshawlife-ctrl/suas-specs` — specification/governance skills
- `scrimshawlife-ctrl/suas` — runtime/conformance skills

When adapting this template, preserve the architecture but replace SUAS-specific semantics with the target repository's canonical language, authority model, evidence states, and runtime provenance requirements.
