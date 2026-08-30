# RELEASE_MANIFEST-0.6.0.md — Resend email and browser authentication

**Release version:** `0.6.0`  
**Release date:** `2026-08-30`  
**Owner:** `@scrimshawlife-ctrl`  
**Supersedes:** `0.5.0`  
**Decision ledger:** [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md) plus inherited ledgers  
**Lifecycle:** `RELEASED_FOR_IMPLEMENTATION`  
**Production readiness:** `NOT_READY`

## Release scope

v0.6.0 closes D-004 by selecting Resend as the sole EMAIL provider and releases an HTML `/app` passwordless session transport for already-enrolled accounts. It removes the contradiction in which the UI appeared to accept an email while the Worker used a sink and the join page had no submit path.

## Released artifacts

- [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md)
- [ENVIRONMENT.md](ENVIRONMENT.md) notification and browser-auth configuration
- [AUTH.md](AUTH.md) browser transport and fixed-tenant resolution
- [ONBOARDING.md](ONBOARDING.md) email-provider settlement
- [DECISIONS.md](DECISIONS.md) D-004 status
- this manifest and the release-lineage updates in [VERSIONING.md](VERSIONING.md), [STATUS.md](STATUS.md), [AGENTS.md](AGENTS.md), [HANDOFF.md](HANDOFF.md), [README.md](README.md), and [CHANGELOG.md](CHANGELOG.md)

## Runtime pins

- Expected specification stack: `0.6.0`.
- API selector: `/api/v0` unchanged.
- Event schema: `0.1.0` unchanged.
- Database schema remains implementation-owned and monotonic.

## Explicit prohibitions

No alternate email adapter or fallback; no browser self-registration; no client-supplied tenant authority; no real Veteran operation; no production launch; no marketing email; no production provider effects beyond a later SPEC-018 settlement.

## Readiness boundary

`PILOT_LAUNCH=blocked` and `PRODUCTION_LAUNCH=blocked`. D-002, D-007, D-013, D-025, and every existing launch/evidence gate remain independently controlling.
