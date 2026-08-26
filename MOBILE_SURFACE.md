# MOBILE_SURFACE.md — Native mobile client contract (SUAS v0.3.0)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md)
**Authority:** client-surface contract for a native mobile application
**Decision:** D-033 ([RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md))
**Related:** [ARCHITECTURE.md](ARCHITECTURE.md) §4, [MVP_REFERENCE.md](MVP_REFERENCE.md), [API.md](API.md), [APIS.md](APIS.md), [AUTH.md](AUTH.md), [CONSENT.md](CONSENT.md), [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), [SAFETY.md](SAFETY.md), [SAFETY_COPY.md](SAFETY_COPY.md), [NOTIFICATIONS.md](NOTIFICATIONS.md), [ENVIRONMENT.md](ENVIRONMENT.md), [TESTING.md](TESTING.md)

## 1. Purpose

Define what a native mobile client of SUAS is, what it may consume, what it must render, and what it must never do.

Before this release the released client inventory in [ARCHITECTURE.md](ARCHITECTURE.md) §4 named a Veteran PWA, a Responder console, and an Admin console. A native mobile application was neither released nor forbidden; it was unspecified, and an unspecified surface is not implementable under [AGENTS.md](AGENTS.md) rules 3 and 12. This artifact closes that gap as a contract, not as a production authorization.

This artifact adds a **client surface**. It adds no domain concept, no state, no event, no API selector, and no capability. Every behavior a native mobile client performs is already specified elsewhere in this stack; this file states which of those obligations bind a client that is not a browser.

## 2. Definition and scope

A **native mobile client** is an installed application on a mobile operating system that consumes the SUAS product API as an ordinary authenticated client.

In scope:

1. A client of the **identified opt-in platform** only.
2. **Plane A consumption only** ([APIS.md](APIS.md) §1). The client calls the SUAS product API. It never calls a Plane B external capability, and it never holds a provider credential ([SECURITY.md](SECURITY.md) §4 rule 7).
3. The **Veteran** client role first. Responder and Admin roles on a native client are permitted by this contract but gated by §9.

Out of scope, and not changed by this release:

- The anonymous public front door, island identity, and any Rev 3 draft contract ([SURFACES.md](SURFACES.md), [ISLANDS.md](ISLANDS.md), [FENCE_POSTS.md](FENCE_POSTS.md), [RIDES.md](RIDES.md) remain draft and are not implementation authority; D-026–D-032 remain open).
- Application-store distribution, which is an operating question gated by SPEC-018, not a specification question.

The first implementation target is iOS. Nothing in this contract is platform-specific; a second platform requires no new release.

## 3. Client classification

| Client | Users | Primary role | Availability |
|---|---|---|---|
| Native mobile client | Veteran (Responder/Admin per §9) | Installed client of the identified opt-in platform | `ENABLED` for implementation, not production operation |

This matches the availability class already carried by the three clients released in v0.1.0. It authorizes implementation. It does not authorize production operation, real veteran data, distribution to real veterans, or a live pilot.

## 4. Consumption contract

1. The client uses `/api/v0`. The path prefix is the canonical version selector ([API.md](API.md) §2). The client **must not** introduce a second version selector: no client-type header, no negotiated media-type version, no `/api/mobile` prefix.
2. The client is an ordinary API consumer. The server derives tenant and actor authority from the session; the client cannot choose arbitrary tenant scope ([API.md](API.md) §1 rule 5).
3. State transitions use released command endpoints ([API.md](API.md) §1 rule 4). The client composes released commands; it does not invent a compound command, and a client-side composition is never presented as a single domain fact.
4. Unsafe commands carry `Idempotency-Key` ([API.md](API.md) §7). Because mobile networks lose responses routinely, the client must retry with the same key rather than issuing a new one, and must treat an authoritative replay as success.
5. Growing lists are consumed through the released cursor/limit contract ([API.md](API.md) §5). The client must not attempt to download complete growing history ([TESTING.md](TESTING.md) §8).
6. The client honors the released error contract ([API.md](API.md) §6), including `429` backpressure with backoff ([APIS.md](APIS.md) §6).
7. The client must not require a server behavior that is not released. Where a required read is not exposed by a released endpoint, the gap returns to specs ([AGENTS.md](AGENTS.md) rule 3). See §10.

## 5. Prohibitions

These are restatements. Each is already binding; each is repeated because a native client makes the corresponding platform capability newly reachable.

| Prohibition | Source |
|---|---|
| Device push notifications. `PUSH` is a reserved `FUTURE` channel and `PUSH_PROVIDER` is `FUTURE`. Configuration may not enable a `FUTURE` surface. | [NOTIFICATIONS.md](NOTIFICATIONS.md) §2, [APIS.md](APIS.md) §3.3, [ENVIRONMENT.md](ENVIRONMENT.md) §4 |
| Social login, including platform identity providers. Veteran authentication is passwordless per [AUTH.md](AUTH.md) §2. | [AUTH.md](AUTH.md) §2, §10; [APIS.md](APIS.md) §3.4 |
| Long-lived unrevocable bearer credentials. | [AUTH.md](AUTH.md) §10 |
| Contact-list / device-address-book access. | [APIS.md](APIS.md) §3.4, [PRIVACY.md](PRIVACY.md) §3 |
| Continuous GPS, background location, or device telemetry beyond what session security requires. A one-time purpose-scoped location remains permitted only where a released workflow collects it. | [APIS.md](APIS.md) §3.4, [PRIVACY.md](PRIVACY.md) §3 |
| Provider credentials, tokens, or client secrets in the application bundle or on the device. | [SECURITY.md](SECURITY.md) §4 rule 7, §7 |
| Treating installation, first launch, or terms-of-service acceptance as a Consent Grant. | [CONSENT.md](CONSENT.md) §9 |
| Compliance claims (HIPAA, SOC 2, ISO) in the application, its metadata, or its store listing. | [SECURITY.md](SECURITY.md) §1, §6 |
| Automated dialing of an emergency destination, automated dispatch, diagnosis, or suicidality determination. | [SAFETY.md](SAFETY.md) §2, §3.1 |
| Writing sensitive free text, credentials, or veteran identifiers to device logs, crash reports, analytics, or screenshots. | [PRIVACY.md](PRIVACY.md) §3, [SECURITY.md](SECURITY.md) §2, [ENVIRONMENT.md](ENVIRONMENT.md) §6 |

## 6. Required client behavior

1. **Transport.** All network traffic uses TLS ([SECURITY.md](SECURITY.md) §2).
2. **Session.** The session credential is opaque and server-revocable ([AUTH.md](AUTH.md) §5). The client must not infer validity from a locally stored value, must not display or depend on a session lifetime, and must re-authenticate through the released challenge flow when the server rejects a credential. Exact challenge and session TTL constants remain `DECISION_PENDING` in [AUTH.md](AUTH.md) §3 and are not set here.
3. **Channel truth.** Where a delivery channel is unavailable, that channel is unavailable and the client does not offer it; a client must not present an authentication method it cannot deliver, and must not fake success ([AUTH.md](AUTH.md) §9, [ONBOARDING.md](ONBOARDING.md) §7.1).
4. **Consent at use time.** The client renders consent state from the server at the moment of use and never from a cached grant ([CONSENT.md](CONSENT.md) §3 rule 1, §4). Consent capture offers only the closed permission/scope pairings in [CONSENT.md](CONSENT.md) §2.1. Notification preferences are never presented as consent ([NOTIFICATIONS.md](NOTIFICATIONS.md) §4).
5. **Crisis path.** The client renders the D-012 approved copy and destinations verbatim ([SAFETY_COPY.md](SAFETY_COPY.md) §0, §1). Layout and markup may adapt to the platform; wording, destinations, actions, and status labels may not. Dialable destinations render as `911` and `988` with no appended parameters, and are invoked only by an explicit person-initiated action.
6. **Crisis fallback.** The crisis surface must not depend on a successful network read. The client ships the national `988` Suicide & Crisis Lifeline and Veterans Crisis Line destinations as local constants and presents them when the server-owned crisis slot is unavailable. A failed configuration read must not yield an empty crisis surface.
7. **State truthfulness.** The client surfaces a state only from its recorded fact ([SAFETY.md](SAFETY.md) §5.1, [SAFETY_COPY.md](SAFETY_COPY.md) §5). The QRF label mapping in [MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2 binds this client unchanged: `RESPONDER_NOTIFIED` requires a recorded delivery, an assignment alone is not sufficient, and `Call` / `Message` appear only when an authorized contact path exists.
8. **Degraded honesty.** A surface with no released domain fact behind it renders as unavailable rather than as empty, simulated, or coming soon in a way that implies a released workflow ([MVP_REFERENCE.md](MVP_REFERENCE.md) §6, §7).
9. **Minimum-necessary display.** The client displays only the veteran-visible projection defined by D-015 and [PRIVACY.md](PRIVACY.md) §5. It must not reconstruct responder-internal fields from any other read.
10. **Untrusted content.** Veteran- and responder-authored text is untrusted and is encoded at render ([SECURITY.md](SECURITY.md) §5).

## 7. Visual and interaction conformance

[MVP_REFERENCE.md](MVP_REFERENCE.md) governs this client without amendment. Its §13 non-goals already exclude freezing CSS or framework technology, so a native implementation is a permitted technology choice; the conformance classes in §2 and the required surface inventory in §5 apply as written.

Two clarifications for a native client:

1. **Navigation simplicity is the binding property.** [MVP_REFERENCE.md](MVP_REFERENCE.md) §5 requires `MUST_MATCH` simplicity of the persistent mobile navigation. A platform-native navigation control satisfies this when it preserves the number of primary destinations and their recognizability. Platform convention is not a divergence; added depth or density is.
2. **Accessibility target is unchanged.** [MVP_REFERENCE.md](MVP_REFERENCE.md) §10 requires WCAG 2.2 AA. Platform accessibility guidelines are an implementation mechanism, not a substitute target. The implementation records how each platform mechanism satisfies the corresponding WCAG criterion, and any residual difference is a documented divergence, not an assumed equivalence.

The visual-regression fixture contract in [MVP_REFERENCE.md](MVP_REFERENCE.md) §11 already records viewport/device class per fixture. A native client extends that contract with its own device class. It does not create a second inventory of required surfaces.

## 8. Environment, configuration, and provenance

A native mobile build is a build under [ENVIRONMENT.md](ENVIRONMENT.md) and inherits §2 and §5 unchanged.

1. The build carries an **explicit environment class**. It is never inferred from the configured API base URL, from a debug/release build configuration, or from a distribution channel ([ENVIRONMENT.md](ENVIRONMENT.md) §2).
2. The build carries the **expected specification stack version and release manifest identifier**, and refuses to run when they do not match its pinned values, mirroring the server rule in [ENVIRONMENT.md](ENVIRONMENT.md) §3.
3. Startup **fails closed** on an invalid or unknown configuration rather than degrading silently ([ENVIRONMENT.md](ENVIRONMENT.md) §5).
4. The build exposes a **build-info surface** carrying application commit and version, released spec version, release manifest identifier, build timestamp, and environment class, with no secrets and no veteran PII ([ENVIRONMENT.md](ENVIRONMENT.md) §8, [VERSIONING.md](VERSIONING.md) §4).
5. A non-production build must not be configured against production data or a production environment. Any build distributed for shared testing is `STAGING` at most and is bound by the `STAGING` row of [ENVIRONMENT.md](ENVIRONMENT.md) §2: no real veteran data, no real external effects.
6. This release adds **no new configuration variable**. In particular it does not add a push-channel mode; adding one requires closing the `FUTURE` push channel through a released decision.

The mobile application version is an **application version** under [VERSIONING.md](VERSIONING.md) §3. It declares which released spec it implements and is not conflated with the stack version, the API selector, or the event schema.

## 9. Responder and administrator roles on a native client

This contract permits a native client to serve Responder and Org Admin roles, subject to conditions that are not satisfied today:

1. Privileged session elevation requires MFA before privileged actions ([AUTH.md](AUTH.md) §4). The production factor type is not selected; D-002 remains `DECISION_PENDING`.
2. Responder queue consumption requires the released cursor/limit contract ([API.md](API.md) §5).
3. Desktop keyboard operation obligations in [MVP_REFERENCE.md](MVP_REFERENCE.md) §10 remain attached to the responder/admin console surfaces and are not discharged by a mobile client.

Until those conditions hold, a native Responder or Admin experience remains implementation-only under [ENVIRONMENT.md](ENVIRONMENT.md) §2 and is not offered to real responders.

## 10. Gaps returned to specs

Recorded here rather than resolved, per [AGENTS.md](AGENTS.md) rule 3 and the epistemic discipline in [AGENTS.md](AGENTS.md).

| Gap | Status | Note |
|---|---|---|
| On-device protection of any locally retained veteran data, including the session credential | D-034 `DECISION_PENDING` | [SECURITY.md](SECURITY.md) §2 specifies encryption at rest for database and backups. It does not specify a client-device at-rest contract. Until D-034 closes, a native client retains the minimum required to hold an authenticated session and does not persist veteran domain data locally. |
| Challenge and session TTL constants | `DECISION_PENDING` | Already open in [AUTH.md](AUTH.md) §3 and §5. Not set by this release. A client must not hardcode or display a lifetime. |
| Tenant selection before authentication | `DECISION_PENDING` | The released challenge contract authenticates within a tenant scope, and no released discovery mechanism assigns a client to a tenant before a session exists. Until this closes, a build carries its tenant scope as pinned configuration under §8 and does not offer tenant selection as a user-facing choice. |
| Self-service enrollment from a client surface | `FUTURE` | [ONBOARDING.md](ONBOARDING.md) governs enrollment. No released client-initiated account-creation contract exists; a native client must not present one. |
| Device push | `FUTURE` | Held at `FUTURE` by [NOTIFICATIONS.md](NOTIFICATIONS.md) §2. Not opened by this release. A native client uses the released in-app notification read path. |

None of these gaps blocks implementation of the veteran surface described in §2, because each has a released conservative behavior stated above.

## 11. Testability

A native mobile client is conformant when the following are demonstrable with deterministic synthetic fixtures:

1. The client consumes only `/api/v0` and introduces no second version selector.
2. Unsafe commands carry a stable `Idempotency-Key` across retries, and a replayed authoritative result is treated as success.
3. Growing lists are consumed through cursor/limit and no path downloads complete history.
4. No forbidden client from §5 is present: no push registration, no social login, no contact-list access, no continuous location, no provider credential in the bundle.
5. The crisis surface renders approved copy verbatim and still presents `988` and the Veterans Crisis Line when the server-owned crisis read fails.
6. No emergency destination is invoked without an explicit person-initiated action.
7. QRF states render only from recorded facts, and `Call` / `Message` appear only with an authorized contact path.
8. Consent capture offers only released permission/scope pairings, and no surface renders from a cached grant after revocation.
9. Startup fails closed on environment/spec/manifest mismatch, and build info reports commit, spec version, manifest, and environment class.
10. Sensitive values are absent from device logs, crash reports, and fixture screenshots.
11. Required surfaces and their conformance classes match [MVP_REFERENCE.md](MVP_REFERENCE.md) §5 under the client's device class, and accessibility evidence maps platform mechanisms to WCAG 2.2 AA criteria.

These extend the suites in [TESTING.md](TESTING.md) §7 and §8. They do not create a new readiness gate.

## 12. Non-goals

- Authorizing production operation, distribution to real veterans, or a live pilot.
- Opening the `FUTURE` push channel or any other unavailable surface.
- Redefining any canonical state machine, event, API selector, consent rule, safety rule, or readiness gate.
- Creating a second required-surface inventory or a mobile-specific product identity.
- Making platform accessibility guidelines a substitute for WCAG 2.2 AA.
- Specifying application-store presence, review, or metadata, which remain operating concerns gated by SPEC-018.
