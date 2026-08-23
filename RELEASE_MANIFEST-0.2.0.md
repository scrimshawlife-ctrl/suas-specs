# RELEASE_MANIFEST-0.2.0.md — D-011 Support Signal scoring release

**Release version:** `0.2.0`  
**Release date:** `2026-08-23` PT  
**Owner:** `@scrimshawlife-ctrl`  
**Supersedes:** `0.1.6`  
**Base release:** [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md)  
**Decision ledgers:** [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md) for D-011; inherited [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012, [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018, [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017, and [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise  
**Lifecycle:** `released` when this PR is owner-merged  
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`  
**Production readiness:** `NOT_READY`

## Release scope

v0.2.0 is a backward-compatible contract addition that closes D-011. It releases:

- exact original questionnaire content as `qv-001`;
- deterministic Support Signal rules as `sv-001`;
- deterministic incomplete-input behavior;
- inspectable/minimized `basis` requirements;
- golden vectors for the published runtime-version pair.

It changes no canonical state machine, API selector, event schema, provider decision, readiness gate, compliance classification, or production-operating authorization.

## Released artifact set

All artifacts released by v0.1.6 remain released. v0.2.0 additionally releases:

- [SIGNAL_SCORING.md](SIGNAL_SCORING.md);
- [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md);
- this manifest;
- D-011 and stack-lineage updates in [DECISIONS.md](DECISIONS.md), [VERSIONING.md](VERSIONING.md), [STATUS.md](STATUS.md), [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), [CHECKINS.md](CHECKINS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), and [TESTING.md](TESTING.md).

Per [VERSIONING.md](VERSIONING.md) §1, this manifest governs the lifecycle of listed artifacts.

## Runtime pins

- Expected specification stack: `0.2.0`.
- QuestionnaireVersion: `qv-001`.
- Support Signal rules: `sv-001`.
- API selector: `/api/v0` unchanged.
- Event schema: `0.1.0` unchanged.
- Database schema remains implementation-owned and must use its explicit monotonic migration identity.

## Not closed by this release

- G-I-28 signal-driven Support Case action semantics.
- D-001–D-010, D-013–D-014, D-019–D-032 except decisions already closed by inherited ledgers.
- SPEC-018 pilot/production readiness.
- Production infrastructure, staffing, SLO, RTO/RPO, reporting privacy, compliance, and provider-operation gates.

## Readiness boundary

All 12 readiness gates remain `NOT_READY`. This release does not authorize production deployment, real veteran data, a live pilot, real provider effects, automated emergency dispatch, payment-card handling, or unsupported compliance/clinical claims.
