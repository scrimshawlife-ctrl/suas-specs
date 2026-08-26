# HANDOFF.md — Implementation handoff guide (SUAS v0.2.0)

**Audience:** new implementation owner / Fable / engineering agents
**Lifecycle:** `released` via [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md) (D-011 over v0.1.6 Wave A, v0.1.5 D-012, v0.1.4 conformance, v0.1.3 D-018)
**Canonical implementation repo:** `scrimshawlife-ctrl/SUAS`

## 1. Start here

Read in this order before changing implementation behavior:

1. `RELEASE_MANIFEST-0.2.0.md` (then `RELEASE_MANIFEST-0.1.6.md`, `RELEASE_MANIFEST-0.1.5.md`, `RELEASE_MANIFEST-0.1.4.md`, and `RELEASE_MANIFEST-0.1.3.md` for inherited scope)
2. `RELEASE_DECISIONS-0.2.0.md` for D-011, `RELEASE_DECISIONS-0.1.5.md` for D-012, `RELEASE_DECISIONS-0.1.3.md` for D-018, `RELEASE_DECISIONS-0.1.2.md` for D-017, plus `RELEASE_DECISIONS-0.1.0.md` for inherited decisions.
3. `STATUS.md`
4. `PRODUCT.md`
5. `GLOSSARY.md`
6. `AGENTS.md`
7. `ENVIRONMENT.md`
8. `ARCHITECTURE.md`
9. `DOMAIN_MODEL.md`
10. `DATA_MODEL.md`
11. `API.md` and `APIS.md`
12. `TESTING.md`
13. `MVP_REFERENCE.md`
14. domain files relevant to the current slice
15. `DEPLOYMENT.md`, `OPERATIONS.md`, `RESILIENCE.md`, `SECURITY.md`

If any implementation requirement conflicts, the release manifest and later released patch clarification control. Return unresolved semantic gaps to `SUAS-specs`.

## 2. Current lifecycle

- Released implementation contract: `0.2.0`
- Current implementation stage: `SPEC-017`
- Production/pilot readiness: `NOT_READY`
- Real veteran data: prohibited
- Production deployment: prohibited
- Real external provider effects: prohibited; Uber D-017 and Amadeus D-018 implementations are adapter-local until SPEC-018. Shelter reservation is payment-architecture-blocked absent a documented card-free enterprise contract.

The implementation may build and test the released architecture and workflows with synthetic data, fake adapters, sink communications, and manual adapter paths.

## 3. Required implementation sequence

Follow the slice order in `scrimshawlife-ctrl/SUAS/SPEC017_PLAN.md`.

Do not jump directly to UI or provider integration before the correctness kernel exists. At minimum, the foundation must establish:

- project/toolchain lockfiles and reproducible commands;
- typed environment/config validation;
- PostgreSQL migration harness;
- test harness;
- event + persistent idempotency kernel;
- tenant isolation foundation;
- durable job abstraction with fake/test implementation if provider remains undecided;
- build provenance/version surface.

## 4. Definition of done for every slice

Every implementation PR must include:

- released spec citations;
- change-map of files/modules to spec sections;
- tests for the affected contract;
- migration notes if schema changes;
- environment/config changes and `.env.example` updates if applicable;
- security/privacy impact;
- failure/idempotency behavior where applicable;
- user-visible/MVP-reference impact where applicable;
- explicit statement of features still unavailable by release manifest;
- rollback/forward-fix note for consequential state changes.

A slice is not complete because code compiles.

## 5. Repository hygiene expected from the first implementation PR

Create or maintain:

- `README.md` with exact local commands;
- `AGENTS.md` implementation authority rules;
- `SPEC017_PLAN.md` current progress;
- `.gitignore`;
- `.env.example` with safe placeholders only;
- dependency lockfile(s);
- formatter/linter/typecheck configuration;
- unit/integration test commands;
- CI workflow(s) once toolchain exists;
- migration directory and schema-version tracking once DB work begins;
- test-fixture/synthetic-data boundary;
- build/version metadata.

Do not create provider credential files or real-data fixtures.

## 6. Versioning contract

Three version identities must not be conflated:

1. **Specification stack version** — currently `0.2.0`.
2. **Application version** — chosen/maintained in `SUAS`; must identify which released spec it conforms to.
3. **Runtime artifact/schema versions** — API `/api/v0`, event schema, DB migration/schema version, QuestionnaireVersion, signal version, templates, etc.

Git SHA is provenance, not a replacement for any of these versions.

Implementation should expose a machine-readable build-info object containing app version/commit, spec version, manifest id, schema/migration version, and environment class.

## 7. Environment contract

`ENVIRONMENT.md` is mandatory. Key rule: configuration may further disable features but cannot enable a surface that the release manifest marks `UNAVAILABLE` or `FUTURE`.

LOCAL/TEST/STAGING must fail closed against real external effects and production data.

## 8. UI handoff

The existing MVP is a behavioral/visual reference, not source-code authority.

Preserve:

- `TAKE ACTION` hierarchy;
- `I NEED SUPPORT` / `I WANT TO SERVE`;
- QRF request/search/contact/cancel flow;
- Immediate Resources;
- Food/Transportation/temporary Shelter/Peer Support category presentation;
- responder on-duty dashboard, Quick Resource Share, Alerts/Chat/Home;
- distinct admin surface;
- mobile-first low cognitive load.

Required divergences remain those in `MVP_REFERENCE.md`: truthful availability, no unsupported proximity guarantee, no hidden future workflows, no unapproved safety copy, and production auth requirements.

## 9. Safety and privacy hard stops

Do not implement or imply:

- automated 911/PSAP dispatch;
- diagnosis or suicide prediction;
- generative primary Support Signal or other safety-critical generative decisions;
- HIPAA or other compliance claims without released evidence;
- crisis copy or destinations other than the D-012 approved set in `SAFETY_COPY.md` (911 / 988); interface language implying a stronger intervention than recorded facts prove;
- production Support Signal compute; D-011 released `qv-001` + `sv-001` as implementation-authoritative scoring, and TEST/CI stay on `SUAS_SUPPORT_SIGNAL_MODE=fixture`. APPLY_EFFECTIVE_SIGNAL transcribes SAFETY.md §3.2 (RED opens/updates a case; non-RED is a no-op; CLOSED is not REOPEN);
- sensitive aggregate reporting while its privacy policy is unavailable;
- whole-case/provider payload disclosure when minimum projection is sufficient.

## 10. Provider handoff

Implement capability ports and Manual/Fake adapters first. Uber is selected for D-017 transportation. Amadeus is selected for D-018 temporary-shelter search/inventory, with mandatory `ManualShelterAdapter`, deterministic explainable ranking, field-level disclosure, and no raw-card handling. Search may be implemented adapter-locally, but reservation is `BLOCKED_BY_PAYMENT_ARCHITECTURE` unless a documented card-free enterprise contract exists. Real effects remain unavailable until SPEC-018.

Never put provider SDK types/statuses in domain packages.

## 11. Questions / ambiguity protocol

When Fable encounters an ambiguity:

1. classify it as implementation mechanism vs product/domain semantics;
2. if mechanism, choose the simplest solution that proves the released invariant and document the tradeoff;
3. if semantic, do not guess—open/update a spec issue or proposed patch in `SUAS-specs`;
4. do not use prototype behavior or third-party API behavior as implicit canon.

## 12. Handoff success criterion

Fable can begin implementation without asking what product is being built, what is canonical, what environments exist, what can contact real systems, how versions are identified, which workflows are enabled, or what evidence constitutes conformance.

The next active stage is SPEC-017; SPEC-018 remains the only path to pilot/production go-live.
