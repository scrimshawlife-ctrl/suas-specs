# STATUS.md — SUAS specification status (v0.6.0)

**Specification lifecycle:** `released`
**Phase:** `IMPLEMENTATION_AUTHORIZED`
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`
**Release manifest:** [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md)
**Decision ledger:** [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md) for D-004; inherited ledgers govern other decisions.
**Pilot readiness:** `NOT_READY`
**Production readiness:** `NOT_READY`

## Governance frontier

SPEC-001 through SPEC-015 are accepted. SPEC-016 established the first released cut. v0.3.0 supersedes v0.2.0 and closes D-033 by releasing the native mobile client surface while preserving `/api/v0`, event schema `0.1.0`, canonical state machines, notification channel availability, and all readiness boundaries. v0.2.0 (inherited) closed D-011 by releasing `qv-001`, `sv-001`, incomplete-input behavior, basis requirements, and golden vectors. SPEC-017 implementation conformance is active. SPEC-018 remains the go/no-go stage for any real pilot or production operation.

## Current release additions

- [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md) grants `IMPLEMENTATION_EVIDENCE_AUTHORIZED` only for D-035 evidence generation in LOCAL fixture and VA SANDBOX. D-035 remains `DECISION_PENDING`; D-016 fallback and production block remain unchanged.

- [MOBILE_SURFACE.md](MOBILE_SURFACE.md) releases the native mobile client contract and closes D-033. The surface is `ENABLED` for implementation and not for production operation.
- D-034 (on-device protection of locally retained veteran data) is opened, not closed.
- Device push remains `FUTURE`; this release adds no push configuration and assigns no decision to that channel.
- [ARCHITECTURE.md](ARCHITECTURE.md) §4 gains a fourth client row; [MVP_REFERENCE.md](MVP_REFERENCE.md) §11 and [TESTING.md](TESTING.md) §7 extend by device class; [ENVIRONMENT.md](ENVIRONMENT.md) §3 gains a client-build subsection.
- Stale inline `draft` headers on [ARCHITECTURE.md](ARCHITECTURE.md) and [MVP_REFERENCE.md](MVP_REFERENCE.md), and the stale `0.1.3` stack header and SPEC-017 status in [ROADMAP.md](ROADMAP.md), are corrected; the manifest governs ([VERSIONING.md](VERSIONING.md) §1).

Inherited from v0.2.0:

- [SIGNAL_SCORING.md](SIGNAL_SCORING.md) releases `qv-001` + `sv-001` and closes D-011.
- Deterministic incomplete-input behavior and golden vectors are implementation-authoritative.
- Domain-file wording for D-015 / D-016 remains inherited from v0.1.6 and matches the v0.1 defaults already `DECIDED` in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md).
- SPEC-003 points at the 0.1.4 effective-signal selection rule in [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §7.1 / [DATA_MODEL.md](DATA_MODEL.md) §4, including the two-override / chain case.
- Leftover high-traffic inline `draft` headers are stamped stale; this manifest governs ([VERSIONING.md](VERSIONING.md) §1).

Inherited from v0.1.5: [SAFETY_COPY.md](SAFETY_COPY.md) and the D-012 copy/destination/truthfulness contract. Inherited from earlier patches: [ENVIRONMENT.md](ENVIRONMENT.md), [HANDOFF.md](HANDOFF.md), adapter-local D-017/D-018, and the 0.1.4 conformance codifications.

## Release meaning

v0.3.0 authorizes implementation of the released native mobile client surface in `scrimshawlife-ctrl/SUAS`, alongside the inherited D-011 scoring contract. It does not authorize production deployment, real veteran data, live pilot operation, application-store distribution, device push, payment-card handling, real external provider bookings/reservations, compliance claims, production SLO/RTO/RPO claims, or sensitive aggregate reporting.

## Readiness gates

All remain `NOT_READY`:

`AUTH`, `CONSENT`, `CHECK-IN`, `COORDINATION`, `EXTERNAL_FULFILLMENT`, `UI_CONFORMANCE`, `SAFETY`, `PRIVACY`, `SCALE`, `RESILIENCE`, `OPERATIONS`, `REPORTING`.

A gate changes only with reproducible evidence under [TESTING.md](TESTING.md).

## Decision boundary

D-012 is closed by [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md). D-017 is closed by [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md). D-018 is closed by [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md). D-015 and D-016 remain the v0.1 defaults decided in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md). D-011 is closed by [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md). D-033 is closed by [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md), which opens D-034. D-019–D-025 and D-026–D-032 remain open unless later releases supersede them.

## Next stage

Proceed with SPEC-017 implementation conformance against owner-merged release `0.4.0` ([RELEASE_MANIFEST-0.4.0.md](RELEASE_MANIFEST-0.4.0.md)). Implementers pin `scrimshawlife-ctrl/SUAS` to this released stack and re-pin `SUAS_SPEC_VERSION` / `SUAS_RELEASE_MANIFEST` accordingly; a stale pin fails closed. Use [HANDOFF.md](HANDOFF.md) and [ENVIRONMENT.md](ENVIRONMENT.md) as mandatory implementation inputs, and [MOBILE_SURFACE.md](MOBILE_SURFACE.md) before any client-surface work.

Native client implementation is authorized by this release and remains subject to SPEC-018 for any real operation or distribution. Nothing in this release advances a readiness gate or reduces the SPEC-018 residual set.

Draft implementation-binding specify/plan for integrating the existing iOS and Android forks with `/api/v0`: [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md), [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md). Those drafts do not consume a SPEC-0xx stage number, do not bump the stack, and do not reopen D-033 or close D-034.
