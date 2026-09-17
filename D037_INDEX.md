# D037_INDEX.md — Funding readiness packet index

**Decision:** D-037  
**Stable identifier:** `SUAS-FUNDING-READINESS-001`  
**Status:** `proposed` / `DECISION_PENDING` / not release-authoritative  
**Stack:** does not bump `0.6.0`  
**Production authority:** none  
**Runtime authority:** none  
**Terminal condition of this packet:** `SUAS_FUNDING_READINESS_SPECIFIED`

This packet assimilates organizational funding readiness and an advisory `$300` credit envelope into existing SUAS evidence doctrine. It does not redesign the product, close D-010, consume SPEC-019, or authorize spending, experiments, or grant applications.

## Packet files

| File | Role |
|---|---|
| [intent/2026-09-17-funding-readiness.md](intent/2026-09-17-funding-readiness.md) | process intent; not a spec |
| [D037_FUNDING_READINESS.md](D037_FUNDING_READINESS.md) | canonical surface, principles, integrity boundary, environment overlay, security, acceptance, traceability, gates |
| [D037_EVIDENCE.md](D037_EVIDENCE.md) | evidence model, Evidence Run 001, measurements, credit budget, capability matrix |
| [D037_OPPORTUNITY_MODEL.md](D037_OPPORTUNITY_MODEL.md) | opportunity-assessment schema; sits outside the product requirement chain |
| [D037_WORKFLOWS.md](D037_WORKFLOWS.md) | workflows, state machines, contracts |
| [D037_TASKS.md](D037_TASKS.md) | derived tasks and readiness-gate application |
| [D037_DRIFT_AUDIT.md](D037_DRIFT_AUDIT.md) | cross-artifact consistency audit for this packet |

## Related released canon (unchanged authority)

- [AGENTS.md](AGENTS.md) epistemic labels and specs-first rule
- [ENVIRONMENT.md](ENVIRONMENT.md) environment classes
- [TESTING.md](TESTING.md) product readiness gates
- [SKILLS.md](SKILLS.md) / [skills/evidence-gate/SKILL.md](skills/evidence-gate/SKILL.md)
- [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md) limited evidence-generation pattern
- [ANALYTICS.md](ANALYTICS.md) operational metrics; not funding claims
- [DECISIONS.md](DECISIONS.md) D-010 remains service billing

## Explicit non-effects

- No change to `/api/v0`, event schema `0.1.0`, Veteran journeys, or client surfaces.
- No fifth `SUAS_ENV` value.
- No grant opportunity is named as eligible.
- No cloud provider is selected (D-001 remains open).
- No credit may be spent from this packet.
