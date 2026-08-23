# RELEASE_DECISIONS-0.2.0.md — D-011 Support Signal scoring decision ledger

**Release:** `0.2.0`  
**Owner:** `@scrimshawlife-ctrl`  
**Owner action date:** `2026-08-23` PT  
**Supersedes for D-011 only:** [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) D-011 boundary  
**Inherited ledgers:** [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012; [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018; [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017; [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise  
**Target:** implementation-authoritative specification release; **not** production-operating approval  
**Production readiness:** `NOT_READY`

This ledger closes D-011 by approving [SIGNAL_SCORING.md](SIGNAL_SCORING.md): questionnaire `qv-001`, signal rules `sv-001`, incomplete-input behavior, and released golden vectors.

| ID | Release status | v0.2.0 boundary |
|---|---|---|
| D-011 | `DECIDED` | Publish the original closed-choice coordination questionnaire as `qv-001` and the deterministic dimension-maximum / ordered-escalation rules as `sv-001`. Six core questions are required; three follow-ups are optional. Missing required safety input refuses computation. Missing required non-safety input is imputed at weight 2 and recorded in basis. Only explicit safety answers can produce `RED`. |

## Consequences

1. Implementations may publish the exact `qv-001` content and implement `sv-001`; they must not alter either published identity in place.
2. The same canonical inputs and versions produce the same level and semantically equivalent basis.
3. Free text and generative-model interpretation are excluded from primary scoring.
4. Support Signals remain coordination labels, not diagnosis, clinical assessment, suicide prediction, or validated psychometrics.
5. Historical calculations remain immutable. A changed questionnaire or mapping requires a new runtime version and new rows.
6. The vectors in [SIGNAL_SCORING.md](SIGNAL_SCORING.md) B4 are released conformance fixtures for `qv-001` + `sv-001`.
7. D-011 does not authorize production operation, real veteran data, automated emergency dispatch, or readiness claims.
8. G-I-28 remains unresolved: this decision does not define the idempotent command that opens or updates a Support Case from a settled signal.

## Unchanged release-wide boundary

v0.2.0 remains implementation-authoritative but not production-operating. All readiness gates remain `NOT_READY`. SPEC-017 conformance and SPEC-018 readiness evidence remain required before any real pilot or production operation.
