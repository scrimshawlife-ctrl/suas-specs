# intent/ — SDLC intent records

**Kind:** process. Not a release artifact. Not implementation authority. Closes no D-0xx. Does not define complete.

Non-trivial specification or product-contract work starts here. Copy [`_TEMPLATE.md`](_TEMPLATE.md) to a dated file (`YYYY-MM-DD-short-slug.md`). Fill every section. Label claims with the epistemic set in [AGENTS.md](../AGENTS.md).

## Sequence

`intent.md` → `spec.md` (must include `## Workflows`) → plan → implement.

The next stage after a filled intent is `spec.md`: a new draft spec or a proposed patch to released contracts. That spec must include a `## Workflows` section. Plan and implement live in the implementation repositories named in [REPOS.md](../REPOS.md) and must cite released specs.

Clarifications that do not change behavior may skip this sequence.

## Holds

- The existing [HANDOFF.md](../HANDOFF.md) hold still applies: do not define complete.
- Do not add an SDLC `HANDOFF.md` in this repository. The released implementation handoff stays at repository root.
- An intent is not a spec, not a plan, and not a release. It does not authorize implementation, pilot, or production.
- Semantic gaps stay labeled. Do not invent product or domain rules here.
