# CHANGELOG.md

Dates are America/Los_Angeles (PT). Lifecycle changes are owner-controlled.

---

## 0.3.0 — pending owner merge — D-033 native mobile client surface

**Implementation-authoritative; not production-operating approval.**

- Closed D-033 through [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md) and released [MOBILE_SURFACE.md](MOBILE_SURFACE.md): the contract for a native mobile client of the identified opt-in platform, classified `ENABLED` for implementation and not for production operation.
- Opened D-034: on-device protection of locally retained veteran data, including the stored session credential. [SECURITY.md](SECURITY.md) §2 covers database and backups only. Until D-034 closes, a client persists no veteran domain data locally.
- Added a fourth client row to [ARCHITECTURE.md](ARCHITECTURE.md) §4 and recorded that adding a client adds no domain concept, state, event, capability, or API selector.
- Extended the fixture contracts by device class rather than by inventory: [MVP_REFERENCE.md](MVP_REFERENCE.md) §11 and [TESTING.md](TESTING.md) §7. `UI_CONFORMANCE` conditions are unchanged.
- Added a client-build subsection to [ENVIRONMENT.md](ENVIRONMENT.md) §3 (explicit environment class, spec/manifest pins, fail-closed startup, pinned tenant scope, no secrets in client bundles) and recorded that no push-mode variable may be introduced while `PUSH` is `FUTURE`.
- Preserved `/api/v0`, event schema `0.1.0`, `qv-001` + `sv-001`, notification channel availability, canonical state machines, and all 12 readiness gates as `NOT_READY`. Added no configuration variable and opened no `UNAVAILABLE` or `FUTURE` surface.
- Recorded that device push, application-store distribution, and any real-veteran use of a native client remain out of scope and SPEC-018-gated.
- Editorial, in the same change set per [CONTRIBUTING.md](CONTRIBUTING.md) §4: stamped stale inline `draft` headers on [ARCHITECTURE.md](ARCHITECTURE.md) and [MVP_REFERENCE.md](MVP_REFERENCE.md); corrected the stale `0.1.3` stack header, `0.1.3` implementation target, and `READY_TO_BEGIN` SPEC-017 status in [ROADMAP.md](ROADMAP.md); recorded that a released contract addition inside the current stage does not consume a SPEC-0xx stage number.

---

## 0.2.0 leftover-header stamp — 2026-08-24 PT

**Editorial stamp only. Not a version bump. Closes no D-0xx. Does not advance readiness gates.**

- Removed the pre-merge re-pin hold in [STATUS.md](STATUS.md). Owner-merged `0.2.0` / `4a722e69` is the implementation pin.
- Stamped [TESTING.md](TESTING.md) lifecycle to `0.2.0`. D-012 points at released [SAFETY_COPY.md](SAFETY_COPY.md); no new TEST mode.
- Stamped [ENVIRONMENT.md](ENVIRONMENT.md) header to `0.2.0`. Left `SUAS_SUPPORT_SIGNAL_MODE` as `disabled|fixture`.
- Pointed [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) authority at `0.2.0` / [SIGNAL_SCORING.md](SIGNAL_SCORING.md). Removed the inline `draft` / `0.1.0` leftover.
- Recorded unanswered G-I-28 QUESTIONS in [SIGNAL_SCORING.md](SIGNAL_SCORING.md). Not a close.
- Stamped start-here files to `0.2.0`: [HANDOFF.md](HANDOFF.md), [AGENTS.md](AGENTS.md), [README.md](README.md). This removes the conflict where STATUS told implementers to pin `0.2.0` while those guides still named `0.1.6` / `0.1.3`.
- Transcribed G-I-28 from [SAFETY.md](SAFETY.md) §3.2 as `APPLY_EFFECTIVE_SIGNAL` (RED opens/updates; non-RED is a no-op; CLOSED is not REOPEN). Not a D-0xx. Not a version bump. Not a readiness-gate advance.
- Recorded that [ADMIN.md](ADMIN.md) §3 remains the admin path for enabling and disabling **accepted catalog adapters** by tenant/coverage. Manual adapters stay first-class. Food/peer API adapters stay unaccepted until D-019/D-020. Credentials never appear on that surface. Implementation of that path is not a spec bump.

---

## 0.2.0 — 2026-08-23 PT — D-011 Support Signal scoring

**Implementation-authoritative; not production-operating approval.**

- Closed D-011 through [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md).
- Released [SIGNAL_SCORING.md](SIGNAL_SCORING.md): original questionnaire `qv-001`, deterministic rules `sv-001`, conservative incomplete-input behavior, minimized basis, and golden vectors.
- Preserved `/api/v0`, event schema `0.1.0`, canonical state machines, and all readiness gates as `NOT_READY`.
- Left G-I-28 signal-driven Support Case action semantics unresolved at release; later transcribed from [SAFETY.md](SAFETY.md) §3.2 in the leftover-header stamp (not a version bump).

---

## Unreleased — draft Rev 3 fence-post contracts (not a version bump)

**Draft / not implementation authority.** Released `0.2.0` remains the implementation contract. These additions do not bump the stack and do not mark any artifact `accepted` or `released`.

- Added [FENCE_POSTS.md](FENCE_POSTS.md) — Rev 3 fence-post outcomes `G1`–`G14` as draft, testable contracts.
- Added [SURFACES.md](SURFACES.md) — anonymous public front door vs identified opt-in platform; crossing remains an affirmative act and declining costs nothing.
- Added [ISLANDS.md](ISLANDS.md) — island config schema, resolve-before-consume behavior, hardcoded 988 / Veterans Crisis Line fallback, and `island_id` isolation boundary.
- Added [RIDES.md](RIDES.md) — ride-adapter contract with human dispatch, minimized provider payloads, and cost guardrails that fail to a human.
- Opened D-026 through D-032 for island scope, dispatcher routing operations, resource-list curation, reporting/minimization, dual enrollment/minors, contracting entity, and volunteer-driver screening. D-017 is closed by v0.1.2 for Uber adapter-local implementation; D-018 is closed by v0.1.3 for Amadeus shelter search/inventory; D-019–D-025 remain the released production-adapter / scale / recovery ledger.
- Added an SB 903 / peer-support register row to [COMPLIANCE.md](COMPLIANCE.md) as a `NOT_COMPUTABLE` note only; no legal or compliance claim.
- Aligned `SUAS_SHELTER_ADAPTER_MODE` naming across runtime and spec text from prior draft placeholder terminology to `amadeus_lodging`; no product semantics changed.
- Added runtime hardening guidance for provider endpoints in line with this release’s security contract, including HTTPS-only non-loopback provider URLs, loopback-safe test endpoints, and rejection of URL-embedded credentials.
- Pushed release pin updates to keep provenance consistent with the final `0.1.3` draft-closure SHA lineage.

No implementation code is included.

---

## 0.1.6 — 2026-08-22 — `released`

**Wave A editorial hygiene patch. Closes no owner decision; no product roles, safety/privacy, API selector, or event-schema change; production readiness unchanged.**

- Added [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md), superseding v0.1.5 while inheriting every decision ledger (D-012/D-017/D-018/D-001–D-025) unchanged.
- Aligned D-015 / D-016 domain wording (`CASES.md`, `AUTH.md`, `PRODUCT.md`, `ONBOARDING.md`, `PILOT.md`, `PRIVACY.md`, `GLOSSARY.md`) with the v0.1 defaults already `DECIDED` in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md). Removed leftover `INFERRED` / "remains open" prose.
- Pointed SPEC-003 at the 0.1.4 effective-signal selection rule in `SUPPORT_SIGNALS.md` §7.1 / `DATA_MODEL.md` §4, and recorded the already-implemented two-override / chain case (a named target is excluded; remaining candidates ordered by `computed_at DESC`, `support_signal_id DESC`).
- Stamped leftover high-traffic inline `draft` headers as stale, with an Authority line pointing at this manifest ([VERSIONING.md](VERSIONING.md) §1).
- Did **not** invent a `ServiceOffer` / `ProviderOffer` join (G-I-4 remains open). Did not change D-011 / D-012 / D-015 / D-016 decision values.
- Production/pilot readiness, real veteran data, and real external provider effects remain `NOT_READY` / prohibited until SPEC-018.

---

## 0.1.5 — 2026-08-22 — `released`

**D-012 safety/crisis copy decision patch. Copy approval only; no canonical state-machine/API/event change; no automated dispatch; production readiness unchanged.**

- Added [SAFETY_COPY.md](SAFETY_COPY.md), the released D-012 approved on-screen crisis copy (veteran-facing, banners/footer, operator-side), the approved/forbidden language rules, and the `REQUESTED ≠ ACCEPTED ≠ DISPATCHED ≠ ARRIVED ≠ RESOLVED` state-truthfulness principle.
- Added [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) and [RELEASE_MANIFEST-0.1.5.md](RELEASE_MANIFEST-0.1.5.md), superseding v0.1.4 while inheriting the D-017/D-018 and D-001–D-025 ledgers unchanged.
- Closed D-012 in `DECISIONS.md`; the only authorized crisis destinations are `911` and the `988` Suicide & Crisis Lifeline (call or text; Veterans via `988`).
- Updated `SAFETY.md` (approved destinations, §5.1 state truthfulness, non-goals, testability), `MVP_REFERENCE.md` §7.3 (crisis copy now `MUST_MATCH` the approved wording), and `ENVIRONMENT.md` (`SUAS_SAFETY_COPY_MODE=approved`).
- SUAS still performs no automated emergency dispatch, diagnosis, or suicidality determination; copy approval is not production-operating approval. Production/pilot readiness, real veteran data, and real external effects remain `NOT_READY` / prohibited until SPEC-018.

---

## 0.1.4 — 2026-08-22 — `released`

**Implementation-conformance codification patch. Closes no owner decision; no product roles, safety/privacy, API selector, or event-schema change; production readiness unchanged.**

- Added [RELEASE_MANIFEST-0.1.4.md](RELEASE_MANIFEST-0.1.4.md), superseding v0.1.3 while inheriting every decision ledger (D-017/D-018/D-001–D-025) unchanged.
- Adopted accepted Bucket I gaps P-1 through P-23 (from `scrimshawlife-ctrl/SUAS` `docs/SPEC_DESIGN_GAPS.md` / `docs/SPEC_GAP_PROPOSALS.md`) into DATA_MODEL, NOTIFICATIONS, RESOURCES, REFERRALS, AUTH, CASES, FOLLOWUP, DISPATCH, PROVIDER_INTEGRATIONS, FULFILLMENT, CONSENT, SUPPORT_SIGNALS, MVP_REFERENCE, VERSIONING, and ENVIRONMENT. Each change codifies implemented+tested behavior or is a pure editorial clarification; none invents product/domain behavior.
- Documented two additive, backward-compatible logical-model fields already carried by merged, tested implementation: `notifications.subject_type`/`subject_id` (P-12, makes MVP `RESPONDER_NOTIFIED` truthfully reachable) and `resources.contact_method_kind` (P-13, enables direct call/email/web actions). Both additive and nullable; absent them prior behavior is unchanged. Adopted at patch level as owner-accepted codifications with this explicit notice (VERSIONING.md §2).
- Bucket II (`D-0xx`) owner decisions and Bucket III contradictions remain owner-only and unaddressed.
- Production/pilot readiness, real veteran data, and real external provider effects remain `NOT_READY` / prohibited until SPEC-018.

---

## 0.1.3 — 2026-08-19 — `released`

**D-018 shelter adapter decision patch. Product/domain/API semantics and production readiness unchanged.**

- Added [RELEASE_MANIFEST-0.1.3.md](RELEASE_MANIFEST-0.1.3.md), superseding v0.1.2 while preserving v0.1.0 through v0.1.2 release history.
- Added [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md), closing D-018 by selecting Amadeus as the first commercial search/inventory adapter family behind `TemporaryShelterPort`.
- Kept `ManualShelterAdapter` mandatory and added deterministic explainable ranking, a field-level shelter disclosure projection, provider health/fallback, idempotency, and ambiguous-outcome contracts.
- Prohibited raw payment-card handling and made reservation `BLOCKED_BY_PAYMENT_ARCHITECTURE` unless a documented card-free enterprise contract permits reservation without SUAS card handling.
- Production/pilot readiness, real veteran data, and real external provider effects remain `NOT_READY` / prohibited until SPEC-018.

---

## 0.1.2 — 2026-08-19 — `released`

**D-017 transportation adapter decision patch. Product/domain/API semantics and production readiness unchanged.**

- Added [RELEASE_MANIFEST-0.1.2.md](RELEASE_MANIFEST-0.1.2.md), superseding v0.1.1 while preserving v0.1.0 and v0.1.1 release history.
- Added [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md), closing D-017 by selecting Uber as the first API-backed transportation adapter family for adapter-local implementation behind `TransportationPort`.
- Updated DECISIONS, README, STATUS, VERSIONING, AGENTS, HANDOFF, ENVIRONMENT, APIS, PROVIDER_INTEGRATIONS, and RIDES to preserve provider neutrality, manual/fake adapter requirements, consent/minimum-necessary disclosure, idempotency, and fail-closed environment rules.
- Production/pilot readiness, real veteran data, and real external provider effects remain `NOT_READY` / prohibited until SPEC-018.

---

## 0.1.1 — 2026-08-18 — `released`

**Handoff/environment hardening patch. No product/domain/API semantic change.**

- Added [ENVIRONMENT.md](ENVIRONMENT.md) with canonical `LOCAL|TEST|STAGING|PRODUCTION` classes, configuration precedence, startup fail-closed rules, secret classes, safe fake/manual adapter modes, build provenance, and schema/migration compatibility requirements.
- Added [HANDOFF.md](HANDOFF.md) as the canonical implementation/Fable start-here path, including read order, repository hygiene, slice definition-of-done, ambiguity protocol, environment/versioning expectations, and safety/provider hard stops.
- Added [RELEASE_MANIFEST-0.1.1.md](RELEASE_MANIFEST-0.1.1.md), superseding v0.1.0 for implementation handoff while preserving the v0.1.0 D-001–D-025 decision ledger.
- Updated README, STATUS, VERSIONING, DEPLOYMENT, and AGENTS to point to the handoff/environment contract and distinguish spec/app/API/event/schema/runtime versions.
- Production/pilot readiness and all 12 readiness gates remain `NOT_READY`.

---

## 0.1.0 — 2026-08-18 — `released`

**First implementation-authoritative SUAS specification release.**

Owner `@scrimshawlife-ctrl` completed SPEC-001 through SPEC-015 acceptance and released SPEC-016. The release established the consent-governed product/domain/API architecture, MVP visual authority, provider-neutral capability ports, scalable modular monolith, replay/idempotency/concurrency rules, testing/readiness gates, operations/resilience contracts, and safe production deferrals recorded in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md).

Implementation authority became `RELEASED_FOR_IMPLEMENTATION`; pilot and production remained `NOT_READY`.

---

## 0.1.0 — 2026-08-14 through 2026-08-18 — pre-release history

The bootstrap/preflight established the canonical loop, staged governance, provider-neutral architecture, MVP reference, scale/resilience contracts, and cross-artifact reconciliation. See [SPEC_AUDIT.md](SPEC_AUDIT.md).
