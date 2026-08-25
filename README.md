# Shut Up and Serve (SUAS) — Specification v0.2.0

**Product:** Shut Up and Serve
**System:** SUAS
**Version:** `0.2.0`
**Lifecycle:** `released`
**Phase:** `IMPLEMENTATION_AUTHORIZED`
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`
**Release manifest:** [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md)

`SUAS-specs` is canonical. `scrimshawlife-ctrl/SUAS` implements released contracts and may not redefine them from code, prototype behavior, provider behavior, deployment state, or traction.

The weekend-build document **HACKATHON BUILD SPECIFICATION Rev 3 (2026-08-14)** is build direction, not a released SUAS product spec. Where it touches this repository, [FENCE_POSTS.md](FENCE_POSTS.md), [SURFACES.md](SURFACES.md), [ISLANDS.md](ISLANDS.md), and [RIDES.md](RIDES.md) define draft contracts that may be reviewed during the event. They are **not** implementation authority. If Rev 3 and this released stack conflict, record the conflict as `DECISION_PENDING` in [DECISIONS.md](DECISIONS.md). Santa Clara County v0.1 remains the same consent-governed identified coordination platform already defined on `main`.

## Start here for implementation / Fable handoff

1. [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md)
2. [HANDOFF.md](HANDOFF.md)
3. [ENVIRONMENT.md](ENVIRONMENT.md)
4. [STATUS.md](STATUS.md)
5. [PRODUCT.md](PRODUCT.md)
6. [GLOSSARY.md](GLOSSARY.md)
7. [AGENTS.md](AGENTS.md)
8. [ARCHITECTURE.md](ARCHITECTURE.md)
9. [DOMAIN_MODEL.md](DOMAIN_MODEL.md) + [DATA_MODEL.md](DATA_MODEL.md)
10. [API.md](API.md) + [APIS.md](APIS.md)
11. [TESTING.md](TESTING.md)
12. [MVP_REFERENCE.md](MVP_REFERENCE.md)
13. domain/operations files required by the active SPEC-017 slice

## Mission

Coordinate the shortest safe and consented path between a veteran's current need and an available human or material support resource.

`SIGNAL → NEED → CONSENT → COORDINATION → FULFILLMENT → FOLLOW-UP → SETTLEMENT`

MVP categories: `FOOD`, `TRANSPORTATION`, `SHELTER`, `PEER_SUPPORT`.

SUAS is not an EHR, diagnosis system, suicide-prediction product, automated emergency dispatcher, or MVP billing platform.

## Current lifecycle

- SPEC-001 through SPEC-015: `accepted`
- SPEC-016: released implementation authority
- SPEC-017: active implementation conformance
- SPEC-018: pilot/production go/no-go, still blocked
- Pilot readiness: `NOT_READY`
- Production readiness: `NOT_READY`
- All 12 readiness gates: `NOT_READY`

v0.2.0 closes D-011 by releasing `qv-001` + `sv-001` in [SIGNAL_SCORING.md](SIGNAL_SCORING.md). TEST/CI stay on `SUAS_SUPPORT_SIGNAL_MODE=fixture`. G-I-28 remains open. It does not authorize production operation. v0.1.6 (inherited) is a Wave A editorial hygiene patch over v0.1.5: it aligns D-015/D-016 domain wording with the already-decided v0.1 defaults, points SPEC-003 at the 0.1.4 effective-signal rule (including the two-override / chain case), and stamps leftover high-traffic `draft` headers as stale. It closes no D-0xx and invents no product behavior. v0.1.5 (inherited) is a D-012 safety/crisis copy decision patch: it approves the on-screen crisis copy and destinations (911 / 988) in [SAFETY_COPY.md](SAFETY_COPY.md) and the `REQUESTED ≠ ACCEPTED ≠ DISPATCHED ≠ ARRIVED ≠ RESOLVED` state-truthfulness contract; it approves copy only (no automated dispatch, no production-operating approval). v0.1.4 (inherited) is an implementation-conformance codification patch adopting accepted Bucket I gaps (P-1..P-23). v0.1.3 (inherited) is a D-018 shelter adapter decision patch: Amadeus may be implemented adapter-locally for commercial shelter search/inventory behind `TemporaryShelterPort`, `ManualShelterAdapter` remains mandatory, and production use remains blocked.

## Environment and configuration

[ENVIRONMENT.md](ENVIRONMENT.md) is mandatory. Logical environments are `LOCAL`, `TEST`, `STAGING`, `PRODUCTION`; LOCAL/TEST/STAGING prohibit real veteran data and real external support effects. Configuration may disable more functionality but cannot enable a release-manifest `UNAVAILABLE` or `FUTURE` surface.

Required implementation provenance includes app version/commit, spec version, manifest identifier, schema/migration version where applicable, build version/time, and environment class.

## Architecture doctrine

- scalable modular monolith;
- shared/persistent correctness state, not process-local truth;
- durable production-critical async work;
- persistent command idempotency distinct from event identity;
- replay-safe required Domain Event publication;
- deterministic one-winner contested operations;
- deterministic current projections while preserving history;
- provider-neutral ports and Manual/Fake adapters first;
- bounded/paginated growing APIs;
- evidence-based scale/resilience.

## MVP visual authority

The existing MVP at `https://suasqrf.org/app/` remains the visual/interaction reference. Preserve its action-first veteran/QRF/resource/responder/admin experience while applying the mandatory truthful/safe divergences in [MVP_REFERENCE.md](MVP_REFERENCE.md).

## Production-unavailable surfaces

Until later decisions/evidence close, do not make operational:

- real production infrastructure or real veteran data;
- production Support Signal compute (`SUAS_SUPPORT_SIGNAL_MODE` stays `disabled|fixture`; G-I-28 remains open);
- production safety operation on real veteran data (the on-screen crisis copy/destinations are approved by D-012 in [SAFETY_COPY.md](SAFETY_COPY.md), but real operation remains SPEC-018-gated and SUAS performs no automated emergency dispatch);
- real food/external peer provider adapters; real transportation bookings; and real Amadeus inventory effects, holds, reservations, or cancellations until SPEC-018 readiness. Shelter reservation also remains `BLOCKED_BY_PAYMENT_ARCHITECTURE` absent a documented card-free enterprise contract;
- production workload/SLO/RTO/RPO claims;
- sensitive aggregate reporting;
- unsupported compliance claims.

See [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md), [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md), [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md), [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md), and [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md).

## Core index

**Authority/product:** [PRODUCT.md](PRODUCT.md), [GLOSSARY.md](GLOSSARY.md), [STATUS.md](STATUS.md), [VERSIONING.md](VERSIONING.md), [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), [AGENTS.md](AGENTS.md), [HANDOFF.md](HANDOFF.md), [ENVIRONMENT.md](ENVIRONMENT.md).

**Architecture/API:** [ARCHITECTURE.md](ARCHITECTURE.md), [DOMAIN_MODEL.md](DOMAIN_MODEL.md), [DATA_MODEL.md](DATA_MODEL.md), [EVENT_MODEL.md](EVENT_MODEL.md), [API.md](API.md), [APIS.md](APIS.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md).

**Domain:** [AUTH.md](AUTH.md), [CONSENT.md](CONSENT.md), [CHECKINS.md](CHECKINS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [SAFETY.md](SAFETY.md), [SAFETY_COPY.md](SAFETY_COPY.md), [TRUSTED_CIRCLE.md](TRUSTED_CIRCLE.md), [CASES.md](CASES.md), [DISPATCH.md](DISPATCH.md), [RESOURCES.md](RESOURCES.md), [REFERRALS.md](REFERRALS.md), [FULFILLMENT.md](FULFILLMENT.md), [FOLLOWUP.md](FOLLOWUP.md), [SETTLEMENT.md](SETTLEMENT.md), [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md), [NOTIFICATIONS.md](NOTIFICATIONS.md).

**Released Support Signal scoring:** [SIGNAL_SCORING.md](SIGNAL_SCORING.md) (`qv-001` + `sv-001`; D-011 decided by [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md)).

**Draft Rev 3 contracts (not implementation authority):** [FENCE_POSTS.md](FENCE_POSTS.md), [SURFACES.md](SURFACES.md), [ISLANDS.md](ISLANDS.md), [RIDES.md](RIDES.md).

**Operations/verification:** [MVP_REFERENCE.md](MVP_REFERENCE.md), [ADMIN.md](ADMIN.md), [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [COMPLIANCE.md](COMPLIANCE.md), [ONBOARDING.md](ONBOARDING.md), [PILOT.md](PILOT.md), [ANALYTICS.md](ANALYTICS.md), [TESTING.md](TESTING.md), [DEPLOYMENT.md](DEPLOYMENT.md), [OPERATIONS.md](OPERATIONS.md), [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md).

## Next work

Proceed with SPEC-017 in `scrimshawlife-ctrl/SUAS`, using [HANDOFF.md](HANDOFF.md) as the entrypoint. Semantic gaps return here; they are not resolved by implementation defaults. Draft Rev 3 files are not released contracts.
