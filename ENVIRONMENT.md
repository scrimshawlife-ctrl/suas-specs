# ENVIRONMENT.md — Environment and configuration contract (SUAS v0.6.0)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md)
**Authority:** implementation configuration contract
**Related:** [DEPLOYMENT.md](DEPLOYMENT.md), [SECURITY.md](SECURITY.md), [ARCHITECTURE.md](ARCHITECTURE.md), [RESILIENCE.md](RESILIENCE.md), [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md), [MOBILE_SURFACE.md](MOBILE_SURFACE.md), [SIGNAL_SCORING.md](SIGNAL_SCORING.md)

## 1. Purpose

Define the runtime environment names, configuration ownership, required startup validation, secret handling, external-effect safety, and feature availability rules a new implementer must follow.

Configuration may select an implementation mechanism. It may not redefine released product/domain semantics.

## 2. Canonical environments

Exactly these logical environment classes are used:

| Value | Purpose | Real veteran data | Real external side effects |
|---|---|---|---|
| `LOCAL` | developer workstation | forbidden | forbidden |
| `TEST` | automated tests / CI | forbidden | forbidden |
| `STAGING` | integrated synthetic validation, visual/load/failure drills | forbidden | forbidden unless a specifically allow-listed sandbox cannot affect real people/resources |
| `PRODUCTION` | eventual real operation | permitted only after SPEC-018 | permitted only after SPEC-018 and relevant decisions close |

Environment class is explicit. It is never inferred from hostname, branch name, NODE_ENV, cloud account, or database name alone.

## 3. Canonical configuration variables

The implementation must expose an equivalent validated configuration object. These environment variable names are the default contract unless a released implementation note maps them explicitly to another mechanism.

### Required in every environment

- `SUAS_ENV` = `LOCAL|TEST|STAGING|PRODUCTION`
- `SUAS_SPEC_VERSION` = released stack version expected by the build
- `SUAS_RELEASE_MANIFEST` = release manifest identifier/path expected by the build
- `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS` = `false|true`

Rules:

1. `SUAS_SPEC_VERSION` must match the implementation's pinned released spec version.
2. `SUAS_RELEASE_MANIFEST` must identify the manifest the build claims to implement.
3. `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=true` is invalid outside `PRODUCTION`.
4. Until SPEC-018 makes production operation ready, `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=true` is invalid even in `PRODUCTION`.
5. Startup must fail closed on invalid/unknown values.

### Data / persistence

Logical configuration names:

- `DATABASE_URL` — PostgreSQL connection string when persistence is enabled
- `DATABASE_POOL_MAX` — bounded connection-pool setting; exact production value remains release/operations evidence
- `SUAS_MIGRATIONS_MODE` = `off|validate|apply` as an implementation control; production automatic migration policy must be explicit in deployment runbooks

No application startup may silently point LOCAL/TEST/STAGING at a production database.

### Auth / sessions

Logical secret/config slots:

- `SUAS_SESSION_SECRET` or equivalent server-side session-signing/encryption secret where the chosen implementation requires one
- provider-specific auth configuration only after the corresponding release decision closes

For the HTML browser surface:

- `SUAS_BROWSER_AUTH_MODE` = `disabled|email_otp`
- `SUAS_BROWSER_TENANT_ID` — required UUID when browser auth is `email_otp`; it pins the deployment to one tenant before authentication

The browser tenant is server-owned configuration and is never accepted from a public form. Browser auth creates no User or enrollment; it authenticates an already-enrolled destination only.

Secrets must come from environment/platform secret storage, never committed files or client-visible bundles.

### Notifications

- `SUAS_EMAIL_MODE` = `disabled|fake|sink|resend`
- `SUAS_SMS_MODE` = `disabled|fake|sink`

`resend` is the only named EMAIL provider mode (D-004, v0.6.0). It requires `RESEND_API_KEY` and `SUAS_EMAIL_FROM`. LOCAL and TEST reject `resend`. STAGING permits it only for already-enrolled, owner-approved test accounts and authentication-delivery evidence. PRODUCTION rejects it until SPEC-018 and applicable launch gates pass. Provider selection does not supply consent or a system basis for an operational notification.

No alternate EMAIL provider mode, fallback, or standby is valid.

No push-channel mode exists. `PUSH` is `FUTURE` ([NOTIFICATIONS.md](NOTIFICATIONS.md) §2) and §4 forbids configuration from enabling it, so a push mode variable must not be introduced before a released decision closes that channel.

### Client builds

A released client surface that ships as an installed application is a build under this contract ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §8). Such a build must carry an equivalent validated configuration object providing:

- environment class, stated explicitly and never inferred from the configured API base URL, a debug/release build configuration, or a distribution channel;
- the expected released stack version and release manifest identifier, refusing to run on mismatch;
- the API base URL and the tenant scope the build is pinned to, until tenant selection before authentication is decided.

Startup fails closed under §5. A client build exposes build provenance under §8. A build distributed for shared testing is `STAGING` at most under §2 and carries no real veteran data and no real external effects. Client bundles are client-visible and therefore never carry secrets or provider credentials (§6, [SECURITY.md](SECURITY.md) §4).

### Fulfillment adapters

For each MVP capability:

- `SUAS_TRANSPORTATION_ADAPTER_MODE` = `manual|fake|uber_api|disabled`
- `SUAS_SHELTER_ADAPTER_MODE` = `manual|fake|amadeus_lodging|disabled`
- `SUAS_SHELTER_RESERVATION_MODE` = `blocked_by_payment_architecture|card_free_enterprise`
- `SUAS_FOOD_ADAPTER_MODE` = `manual|fake|disabled`
- `SUAS_PEER_SUPPORT_ADAPTER_MODE` = `manual|fake|disabled`

`uber_api` is authorized only as the D-017 transportation adapter mode. `amadeus_lodging` is authorized only as the D-018 temporary-shelter search/inventory adapter mode. Both remain invalid for real external effects until `SUAS_ENV=PRODUCTION`, SPEC-018 readiness passes, required secrets and callback/webhook validation are configured, and `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=true` is valid.

`SUAS_SHELTER_RESERVATION_MODE` defaults to `blocked_by_payment_architecture`. `card_free_enterprise` is valid only when a released, owner-approved deployment record identifies a documented enterprise contract under which the selected reservation can complete without SUAS collecting, transmitting, proxying, tokenizing, or storing raw payment-card data. Configuration alone cannot assert that contract exists. Otherwise reservation initiation fails closed as `BLOCKED_BY_PAYMENT_ARCHITECTURE` and returns to `ManualShelterAdapter` or another explicitly allowed human path.

Future real food or external peer-support modes still require D-019 or D-020 closure and a released manifest update.

### Support Signal / safety / reporting

Until their owning decisions close:

- `SUAS_SUPPORT_SIGNAL_MODE` = `disabled|fixture`
- `SUAS_SAFETY_COPY_MODE` = `placeholder_test_only|approved|disabled`
- `SUAS_SENSITIVE_AGGREGATE_REPORTING` = `disabled`

`fixture` and `placeholder_test_only` are never production authority. `approved` (0.1.5) renders the released D-012 copy in [SAFETY_COPY.md](SAFETY_COPY.md) and is valid in any environment; it approves wording only and does not by itself authorize production operation, which remains gated by SPEC-018 and the environment rules above.

## 4. Configuration precedence

Precedence is:

1. released specification and release manifest;
2. environment-class safety invariants in this file;
3. deployment configuration / secret store;
4. tenant/org operational configuration where explicitly allowed;
5. code defaults.

A lower layer may further restrict a feature. It may not enable a feature the release manifest marks `UNAVAILABLE` or `FUTURE`.

## 5. Startup validation

Before serving traffic or running workers, configuration validation must fail closed when any of these are true:

- unknown `SUAS_ENV`;
- spec version or release manifest mismatch;
- real external effects enabled outside an authorized production release;
- LOCAL/TEST/STAGING points at known production data resources;
- a real provider adapter is configured without a released provider decision, or `uber_api`/`amadeus_lodging` is configured for real effects before SPEC-018/readiness authorization;
- `card_free_enterprise` shelter reservation is configured without the documented contract and release/deployment record required above;
- required secrets are absent for an enabled capability;
- `SUAS_SUPPORT_SIGNAL_MODE` attempts production scoring without a released signal version;
- official safety copy is requested without an approved released artifact;
- sensitive aggregate reporting is enabled while D-025 remains unresolved for that surface.

Configuration validation runs in tests and at runtime startup.

## 6. Secret classes

Treat at least these as secrets:

- database credentials;
- session/signing/encryption secrets;
- auth provider credentials;
- email/SMS provider credentials;
- external service/provider tokens;
- webhook signing secrets;
- encryption/KMS credentials;
- any recovery or break-glass credential.

Never write secret values to logs, fixtures, screenshots, analytics, error responses, repository files, or release manifests.

## 7. Repository files

Implementation may include:

- `.env.example` containing names and safe placeholders only;
- typed/config-schema source code;
- test fixture environment files containing no secrets;
- local developer overrides excluded by `.gitignore`.

Implementation must not commit `.env`, production credentials, real addresses/phone numbers, or copied production data.

## 8. Build provenance

Every build intended for shared testing must expose at least:

- application commit SHA;
- released SUAS spec version;
- release manifest identifier;
- build timestamp/version;
- environment class.

These values may be shown in an admin/debug build-info surface without secrets or veteran PII.

## 9. Migration and compatibility rules

- Migrations cite the released data/domain contract they implement.
- Destructive migrations require an explicit migration/rollback or forward-fix plan.
- A code build must reject a database schema state it cannot safely operate against.
- Schema compatibility cannot be inferred only from application version; use an explicit migration/schema version mechanism. That mechanism (0.1.4): the schema version is a monotonic integer equal to the highest applied numbered migration, recorded in a runner-owned bookkeeping table; the build declares the schema version it requires and refuses to operate against a state below it ([VERSIONING.md](VERSIONING.md) §3).
- Rollback must not re-run external provider effects or lose idempotency/event/Settlement/FulfillmentAttempt history.

## 10. Handoff acceptance

A new implementer is correctly configured when they can prove:

1. LOCAL starts with no real external effects;
2. TEST runs with deterministic synthetic fixtures;
3. STAGING can exercise fake/manual adapters and failure drills without contacting real veterans/providers;
4. build info identifies the released spec/manifest and app commit;
5. invalid feature/environment combinations fail closed;
6. no secret or production data is committed.

Production remains blocked until SPEC-018.
