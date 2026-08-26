# RELEASE_MANIFEST-0.3.0.md — D-033 native mobile client surface release

**Release version:** `0.3.0`  
**Release date:** pending owner merge  
**Owner:** `@scrimshawlife-ctrl`  
**Supersedes:** `0.2.0`  
**Base release:** [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md)  
**Decision ledgers:** [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md) for D-033 and D-034; inherited [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md) for D-011, [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012, [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018, [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017, and [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise  
**Lifecycle:** `released` when this PR is owner-merged  
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`  
**Production readiness:** `NOT_READY`

## Release scope

v0.3.0 is a backward-compatible contract addition that closes D-033 and opens D-034. It releases:

- the native mobile client surface contract as [MOBILE_SURFACE.md](MOBILE_SURFACE.md);
- the client classification `ENABLED` for implementation and not for production operation, matching the availability class of the three clients released by v0.1.0;
- the prohibitions, required behaviors, conformance clarifications, build-configuration obligations, and testability conditions in that artifact.

It changes no canonical state machine, API selector, event schema, consent rule, safety rule, provider decision, readiness gate, compliance classification, or production-operating authorization. It adds no configuration variable and opens no `UNAVAILABLE` or `FUTURE` surface.

## Released artifact set

All artifacts released by v0.2.0 remain released. v0.3.0 additionally releases:

- [MOBILE_SURFACE.md](MOBILE_SURFACE.md);
- [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md);
- this manifest;
- D-033/D-034 and stack-lineage updates in [DECISIONS.md](DECISIONS.md), [VERSIONING.md](VERSIONING.md), [STATUS.md](STATUS.md), [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), [AGENTS.md](AGENTS.md), [HANDOFF.md](HANDOFF.md), [ROADMAP.md](ROADMAP.md), [ARCHITECTURE.md](ARCHITECTURE.md), [MVP_REFERENCE.md](MVP_REFERENCE.md), [TESTING.md](TESTING.md), and [ENVIRONMENT.md](ENVIRONMENT.md).

Draft Rev 3 files remain draft and are not redefined by this release.

Per [VERSIONING.md](VERSIONING.md) §1, this manifest governs the lifecycle of listed artifacts.

## Runtime pins

- Expected specification stack: `0.3.0`.
- API selector: `/api/v0` unchanged.
- Event schema: `0.1.0` unchanged.
- QuestionnaireVersion `qv-001` and Support Signal rules `sv-001` unchanged.
- Notification channels unchanged: `EMAIL`, `SMS`, `IN_APP` available per release mode; `PUSH` remains `FUTURE`.
- Database schema remains implementation-owned and must use its explicit monotonic migration identity.
- Client application versions remain application-owned and declare the released spec they implement.

## Not closed by this release

- D-034 on-device data protection, opened by this release.
- Challenge and session TTL constants, tenant selection before authentication, and self-service enrollment from a client surface ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §10).
- Device push, which remains `FUTURE` with no decision assigned.
- G-I-28 signal-driven Support Case action semantics.
- D-001–D-010, D-013–D-014, D-019–D-032 except decisions already closed by inherited ledgers.
- SPEC-018 pilot/production readiness.
- Production infrastructure, staffing, SLO, RTO/RPO, reporting privacy, compliance, and provider-operation gates.

## Readiness boundary

All 12 readiness gates remain `NOT_READY`. `UI_CONFORMANCE` conditions are unchanged by this release; a native client extends the existing fixture contract with its own device class rather than adding a gate condition.

This release does not authorize production deployment, real veteran data, a live pilot, application-store distribution, real provider effects, device push, automated emergency dispatch, payment-card handling, or unsupported compliance/clinical claims.
