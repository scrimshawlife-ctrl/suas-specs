# SKILLS.md — SUAS specification agent skills

This file defines the reusable agent skills recommended for work in `SUAS-specs`.

`SUAS-specs` is the canonical specification and governance repository. Skills used here MUST preserve the authority, environment, safety, evidence, and release boundaries defined by `AGENTS.md`, `HANDOFF.md`, `ENVIRONMENT.md`, and the active release manifest.

## Required core skills

| Skill | Purpose in SUAS-specs | Requirement |
|---|---|---|
| `spec-driven-development` | Convert product intent into governed requirements, plans, tasks, decisions, and release contracts. | REQUIRED |
| `github` | Inspect history, issues, PRs, review threads, releases, manifests, and cross-repo evidence. | REQUIRED |
| `code-review` | Review specification changes for contradictions, missing contracts, unintended authority changes, and cross-artifact drift. | REQUIRED |
| `security-audit` | Threat-model auth, authorization, tenant boundaries, provider boundaries, secrets, abuse cases, and fail-closed behavior. | REQUIRED |
| `privacy-compliance` | Review consent, minimization, retention, deletion, export, reporting, sensitive-data, and production-use constraints. | REQUIRED |
| `test-engineering` | Define deterministic acceptance criteria, golden vectors, negative cases, conformance tests, and evidence requirements. | REQUIRED |
| `api-integration` | Specify provider-neutral capability ports, external API contracts, provenance, failure modes, sandbox boundaries, and adapter requirements. | REQUIRED |
| `documentation` | Maintain decision records, release manifests, handoffs, runbooks, evidence contracts, and canonical terminology. | REQUIRED |

## SUAS-specialized skills

These skills encode recurring SUAS reasoning patterns and SHOULD be implemented as reusable agent skills rather than reconstructed ad hoc.

### `evidence-gate`

Purpose: determine whether a decision, feature, pilot, or production gate is merely implemented, verified, accepted, or actually released.

Required behavior:

- Distinguish `IMPLEMENTED`, `VERIFIED`, `ACCEPTED`, `RELEASED`, `NOT_READY`, `NOT_COMPUTABLE`, and `DECISION_PENDING` states.
- Never infer gate settlement from green CI, merged code, or the existence of an artifact.
- Resolve the named owner, decision authority, required evidence, evidence hashes/references, UTC cutoff where applicable, scope, and constraints.
- Preserve disabled or blocked runtime states until explicit authority permits activation.
- Detect missing, stale, contradictory, or cross-environment evidence.
- Produce the smallest evidence packet needed for deterministic owner review.

### `synthetic-data`

Purpose: specify and validate canonical deterministic synthetic datasets for development, testing, privacy review, and gate evidence.

Required behavior:

- Use no real veteran or production data in LOCAL/TEST/STAGING where prohibited by `ENVIRONMENT.md`.
- Record dataset identity/version and cryptographic hash when evidence depends on exact inputs.
- Record deterministic mapping identity/hash, projection rules, cutoff, expected outputs, and aggregate contract when applicable.
- Include negative, boundary, NO_HIT/empty, malformed, replay, and cross-tenant cases where the contract requires them.
- Make fixtures reproducible from checked-in definitions or deterministic generators.
- Never silently broaden synthetic evidence into production authorization.

### `recovery-test`

Purpose: define and assess backup/restore and durable-work recovery evidence.

Required behavior:

- Separate migration rehearsal from actual backup/restore evidence.
- Record backup identity, restore target, UTC start/end, restoration timing, schema validation, loss boundary, durable-job behavior, and operator result.
- Verify replay/idempotency behavior after restoration.
- Identify assumptions that remain unavailable, untested, or environment-specific.
- Do not manufacture RTO/RPO/SLO claims from a single exercise unless canonical authority explicitly permits them.

### `contract-validation`

Purpose: validate deterministic SUAS domain and scoring contracts against released identities and invariants.

Required behavior:

- Pin exact questionnaire/scoring/spec identities where applicable.
- Verify required/optional inputs and conservative missing-input behavior.
- Validate golden vectors and explicit safety escalation rules.
- Detect mismatches between emitted provenance/basis and accepted inputs.
- Verify disabled or unavailable modes are actually non-callable where the contract requires that behavior.
- Treat semantic ambiguity as a spec gap, not an implementation opportunity.

### `adversarial-testing`

Purpose: design negative-path evidence for boundaries that must fail closed.

Required behavior:

- Include unauthenticated, unauthorized, wrong-role, wrong-tenant, stale-token, replay, malformed-input, unavailable-provider, disabled-feature, and ambiguous-outcome cases as applicable.
- Test cross-tenant negatives at API, database, jobs, caches, adapters, reports, and admin boundaries where those surfaces exist.
- Verify failures do not create observable external effects.
- Preserve provenance so failures can be independently reproduced.

### `accessibility-audit`

Purpose: define and evaluate accessibility conformance for released SUAS client surfaces.

Required behavior:

- Combine automated checks with required human review; automated tools alone do not settle human-review gates.
- Cover keyboard/focus behavior, labels/names, semantic structure, contrast, zoom/reflow, reduced motion where applicable, error communication, and safety-copy presentation.
- Record environment, build identity, route/surface, evidence artifact, findings, and reviewer disposition.

## Supporting specification skills

The following are RECOMMENDED when the slice requires them:

- `frontend-design` — define usable, truthful, accessible UI behavior without inventing domain semantics.
- `database-migration-audit` — specify schema invariants, compatibility, rollback, data lifecycle, and evidence expectations.
- `deployment-runbook` — specify staging/production gates, provenance, rollback, and operator procedures.
- `observability` — define structured logs, audit events, traces, metrics, redaction, and diagnostic boundaries.
- `threat-modeling` — perform structured abuse-case and trust-boundary analysis.
- `research` — gather authoritative vendor, API, legal, regulatory, accessibility, and technical sources; provenance is mandatory.
- `technical-writing` — produce safety copy, operator instructions, decision records, and evidence templates using canonical terminology.

## Skill execution rules

1. Read `AGENTS.md` and `HANDOFF.md` before using any skill to change canonical material.
2. Resolve the active released stack and release manifest before claiming implementation authority.
3. Use canonical terminology exactly.
4. Separate `OBSERVED` facts from `INFERRED` conclusions. Weak or missing evidence returns `NOT_COMPUTABLE` or the canonical pending state.
5. A skill may reduce ambiguity; it may not create authority.
6. External provider behavior is evidence about a provider, not automatically a SUAS product decision.
7. Any semantic gap discovered by a skill MUST return to specification/decision work before runtime implementation.
8. Evidence-producing skills MUST record enough provenance for independent reproduction.

## Recommended team bundle

For agents working primarily in this repository, install or provide equivalents for:

`spec-driven-development`, `github`, `code-review`, `security-audit`, `privacy-compliance`, `test-engineering`, `api-integration`, `documentation`, `evidence-gate`, `synthetic-data`, `recovery-test`, `contract-validation`, `adversarial-testing`, and `accessibility-audit`.

The specialized skills are SUAS workflow contracts. If the agent platform does not provide them natively, implement them as project-local skills with deterministic inputs, outputs, provenance, and fail-closed handling for missing evidence.
