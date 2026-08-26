# RELEASE_DECISIONS-0.3.0.md — D-033 native mobile client surface decision ledger

**Release:** `0.3.0`  
**Owner:** `@scrimshawlife-ctrl`  
**Owner action date:** pending owner merge  
**Supersedes for D-033 only:** none; D-033 is a new decision opened and closed by this release  
**Inherited ledgers:** [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md) for D-011; [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012; [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018; [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017; [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise  
**Target:** implementation-authoritative specification release; **not** production-operating approval  
**Production readiness:** `NOT_READY`

This ledger closes D-033 by releasing [MOBILE_SURFACE.md](MOBILE_SURFACE.md): the contract for a native mobile client of the identified opt-in platform. It adds a client surface only. It adds no domain concept, state, event, capability, or API selector, and it opens no currently unavailable surface.

| ID | Release status | v0.3.0 boundary |
|---|---|---|
| D-033 | `DECIDED` | A native mobile application is a released client of the identified opt-in platform, classified `ENABLED` for implementation and not for production operation. It consumes Plane A `/api/v0` as an ordinary authenticated client, holds no provider credential, and inherits [MVP_REFERENCE.md](MVP_REFERENCE.md) conformance, [SAFETY_COPY.md](SAFETY_COPY.md) approved copy, [CONSENT.md](CONSENT.md) use-time evaluation, [PRIVACY.md](PRIVACY.md) collection boundaries, and [ENVIRONMENT.md](ENVIRONMENT.md) environment-class, pin, fail-closed, and provenance rules. Device push, social login, contact-list access, continuous location, and long-lived unrevocable credentials remain prohibited. |
| D-034 | `DECISION_PENDING` | On-device protection of any locally retained veteran data, including the stored session credential. [SECURITY.md](SECURITY.md) §2 specifies encryption at rest for database and backups only. Until D-034 closes, a native client retains the minimum required to hold an authenticated session and does not persist veteran domain data locally. |

## Consequences

1. Implementations may build a native mobile client against the released `/api/v0` contract. The client is an API consumer; it is not a second architecture and does not change the modular-monolith doctrine in [ARCHITECTURE.md](ARCHITECTURE.md).
2. [ARCHITECTURE.md](ARCHITECTURE.md) §4 gains a fourth client row. Every client in that table, including this one, conforms to [MVP_REFERENCE.md](MVP_REFERENCE.md).
3. The required-surface inventory, conformance classes, and QRF truthfulness table in [MVP_REFERENCE.md](MVP_REFERENCE.md) bind the native client unchanged. The client extends the §11 fixture contract with its own device class rather than creating a second inventory.
4. WCAG 2.2 AA remains the accessibility target ([MVP_REFERENCE.md](MVP_REFERENCE.md) §10). Platform accessibility guidelines are an implementation mechanism, and any residual difference is a documented divergence rather than an assumed equivalence.
5. The D-012 approved crisis copy is rendered verbatim on a native client; layout may adapt, wording and destinations may not. The client presents `988` and the Veterans Crisis Line from local constants when the server-owned crisis read is unavailable, so a failed read never yields an empty crisis surface.
6. The `PUSH` channel remains `FUTURE` ([NOTIFICATIONS.md](NOTIFICATIONS.md) §2) and `PUSH_PROVIDER` remains `FUTURE` ([APIS.md](APIS.md) §3.3). This release neither opens them nor assigns a decision to them, and adds no push configuration variable. A native client uses the released in-app notification read path.
7. Veteran authentication remains passwordless ([AUTH.md](AUTH.md) §2). Platform identity providers are social login and remain excluded. Session credentials remain opaque and server-revocable; long-lived unrevocable bearer credentials remain a non-goal ([AUTH.md](AUTH.md) §10).
8. Installation, first launch, and terms-of-service acceptance are not Consent Grants ([CONSENT.md](CONSENT.md) §9). The clause excluding implied consent from downloading the PWA applies to an installed native client on the same basis.
9. Collection boundaries are unchanged ([PRIVACY.md](PRIVACY.md) §3). A native client adds no continuous location, no device address book, and no device telemetry beyond what session security requires.
10. A native build is a build under [ENVIRONMENT.md](ENVIRONMENT.md): explicit environment class, spec and manifest pins, fail-closed startup, and a build-info surface. Any build distributed for shared testing is `STAGING` at most and carries no real veteran data and no real external effects.
11. D-033 does not authorize production operation, application-store distribution, a live pilot, real veteran data, or any readiness claim. It changes no readiness gate.
12. D-034 is opened, not closed. No implementation default may close it ([DECISIONS.md](DECISIONS.md) rule 1).

## Unchanged release-wide boundary

v0.3.0 remains implementation-authoritative but not production-operating. All 12 readiness gates remain `NOT_READY`. SPEC-017 implementation conformance and SPEC-018 readiness evidence remain required before any real pilot or production operation, on any client surface.
