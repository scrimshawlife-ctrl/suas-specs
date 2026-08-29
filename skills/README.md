# SUAS specification skill router

Read repository-root `SKILLS.md` for the full skill catalog and execution rules. Load the specialized skill below when its trigger matches the task.

| Skill | Load |
|---|---|
| Evidence/readiness/owner settlement | [`evidence-gate/SKILL.md`](evidence-gate/SKILL.md) |
| Deterministic fixtures/evidence datasets | [`synthetic-data/SKILL.md`](synthetic-data/SKILL.md) |
| Backup/restore evidence | [`recovery-test/SKILL.md`](recovery-test/SKILL.md) |
| Deterministic domain/scoring conformance | [`contract-validation/SKILL.md`](contract-validation/SKILL.md) |
| Fail-closed/negative boundary coverage | [`adversarial-testing/SKILL.md`](adversarial-testing/SKILL.md) |
| Client accessibility evidence | [`accessibility-audit/SKILL.md`](accessibility-audit/SKILL.md) |

## Routing rule

1. Read `AGENTS.md` and `HANDOFF.md` first.
2. Resolve active released stack and release manifest.
3. Load every specialized skill whose trigger materially applies; skills may compose.
4. Specification skills define authority/evidence semantics. They do not create runtime authority.
5. Missing canonical input returns `NOT_COMPUTABLE` or the governing pending state; do not invent it.