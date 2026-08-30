# D033_NATIVE_CLIENT_PLAN.md — Native forks consume `/api/v0` (plan)

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Specify (what/why):** [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md)  
**Released client contract:** [MOBILE_SURFACE.md](MOBILE_SURFACE.md) (D-033)  
**Product API repo:** `scrimshawlife-ctrl/SUAS`  
**Does not implement:** iOS, Android, or Worker code  
**Does not define:** “complete”

This file states **how** the existing native forks become ordinary `/api/v0` clients of the identified opt-in platform. It adds no domain concept and opens no decision.

## 1. Naming and versioning conclusion

`OBSERVED` in this repository:

- [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md) (v0.3.0): SPEC-0xx numbers are **stage records**. A client-surface binding such as D-033 does **not** consume a stage number.
- `SPEC-001`–`SPEC-016` exist as files. `SPEC-017` is the active implementation-conformance stage (`scrimshawlife-ctrl/SUAS` holds `SPEC017_PLAN.md`). `SPEC-018` is launch readiness. `SPEC-019` is post-launch revision.
- D-033 is already `DECIDED`. [VERSIONING.md](VERSIONING.md) requires a MINOR/MAJOR bump for a contract addition or a breaking change. This packet is implementation-binding guidance for an already-released client surface, analogous to the additive [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md) packet (not a version bump).

Therefore this packet:

| Choice | Verdict |
|---|---|
| New SPEC-0xx stage (`SPEC-017` / `SPEC-020`) | Rejected. Would invent a stage and contradict [ROADMAP.md](ROADMAP.md). |
| New D-id | Rejected. D-033 already released the capability. |
| Stack bump | Rejected. Inherits current `0.6.0`. No new contract. Does not reopen D-004. |
| File names | `D033_NATIVE_CLIENT_INTEGRATION.md` (specify) + this plan, following the `D035_*` / `D-006_*` named-packet pattern. |

## 2. Observed current state

Do not treat this section as a product decision. It is the starting inventory.

### 2.1 Product API — `scrimshawlife-ctrl/SUAS`

`OBSERVED` at `scrimshawlife-ctrl/suas` main `49a01308`:

- Machine-readable contract: `docs/openapi/v0.json` (OpenAPI 3.0.3; `info.version` `0.2.0`). Paths document what the runtime registers today; draft [APIS.md](APIS.md) Plane A paths that are not yet implemented are intentionally absent.
- The Worker does **not** serve `/openapi.json` (`404`). Clients pin the repo file. There is no generated SDK in SUAS. Drift check only: `npm run openapi:check` (`scripts/check-openapi-drift.ts`).
- Auth for `/api/v0` and native clients is opaque session bearer only. Header: `Authorization: Bearer <credential>`. Native clients do not use cookies. v0.6.0 added a browser `/app` cookie; that path is HTML only ([AUTH.md](AUTH.md) §9.1). Client HMAC is server-side storage only; the client sends the raw opaque token.
- EMAIL delivery uses Resend exclusively under D-004. Native sign-in remains released challenge/verify + Bearer, not the HTML EMAIL OTP cookie path.
- Runtime status codes drift from OpenAPI. OpenAPI documents `200` for these three. Runtime: `POST /api/v0/auth/challenges` → `202`; verify → `201` `{session_credential, expires_at, mfa_elevated}`; logout → `204`.
- No CORS (`Access-Control-Allow-Origin` absent; `OPTIONS` → `404`). Native HTTP clients are fine. A `WKWebView` or browser cross-origin fetch would be blocked.
- Smallest Veteran loop from OpenAPI + route files: `GET /api/v0/health`; `POST /api/v0/auth/challenges`; `POST /api/v0/auth/challenges/commands/verify`; `POST /api/v0/auth/sessions/commands/logout`; `GET /api/v0/veterans/me`; `POST`/`GET` `/api/v0/check-ins`; `POST /api/v0/check-ins/{id}/responses`; `POST /api/v0/check-ins/{id}/commands/complete`.
- Check-In response body `{question_id, answer_option_id}` is in the route file and missing from the OpenAPI `requestBody`.
- Other registered Veteran-relevant JSON paths include `GET /api/v0/immediate-resources`, `GET /api/v0/resources`, `POST /api/v0/cases/{caseId}/service-requests`, `GET /api/v0/service-requests/{id}`, `POST /api/v0/service-requests/{id}/commands/{command}`, plus consent, notification, and trusted-contact paths listed in that OpenAPI file.
- `GET /api/v0/cases` is registered as a **responder** queue. `src/http/routes/cases.ts` registers no `POST /api/v0/cases`.
- [API.md](API.md) §8 still lists `POST /cases` as a representative command.
- `/api/v0/dev/*` is not in OpenAPI.

`OBSERVED` synthetic shared-testing host: `https://suasqrf.com`. `GET /` redirects to `/app`. `GET /api/v0/health` is the liveness probe. `/api/v0/dev/*` returns `404` on that host.

### 2.2 iOS — `scrimshawlife-ctrl/suas-ios`

Private fork of `louisroehrs/suas-ios`. Swift.

`OBSERVED` in `suas/suas/APIClient.swift`:

- Already wraps `/api/v0` for challenges, verify (Bearer session), logout, `GET /veterans/me`, service-request create/read/command, and `GET /resources`.
- Sends `Authorization: Bearer <credential>` and `Idempotency-Key` on unsafe service-request commands.
- Hardcodes `http://localhost:3000` and tenant `00000000-0000-4000-8000-000000000001`.
- Opens a Support Case by `POST /app/qrf/deploy`. That path is HTML UI, not `/api/v0`. Do not treat it as the mobile case-open.
- Also calls `GET /api/v0/dev/last-challenge` (query `destination`) and `POST /api/v0/dev/service-requests/{id}/simulate`. Those paths are not in OpenAPI and `404` on `https://suasqrf.com`. `AppState.swift` `devLogin` issues a challenge, then reads the captured code from `/dev/last-challenge`, then verifies. Staging login must be the released challenge/verify flow, not `/dev/*`.

`OBSERVED` in `suas/suas/AppState.swift`: the bearer is written to `UserDefaults` (`suas.bearer`) and restored at launch as signed-in. That conflicts with the D-034 conservative rule (session only; do not persist Veteran domain data). Record the gap. Do not close D-034.

`OBSERVED`: `LocationManager.swift` exists. [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §5 forbids continuous GPS and background location.

### 2.3 Android — `scrimshawlife-ctrl/suas-android`

Public fork of `RuntimeSquad/Suas`. Kotlin Jetpack Compose.

`OBSERVED` in `app/src/main/java/com/example/suas/MainActivity.kt` plus theme: scaffold screens only. No API client. Copy on the scaffold asserts “dispatched now,” named ride brands, free hotel voucher, sponsor payment, and “Call 988 · Press 1” for immediate danger. That copy conflicts with [SAFETY_COPY.md](SAFETY_COPY.md) and [MVP_REFERENCE.md](MVP_REFERENCE.md) §6–§7.

## 3. Binding contracts

| Layer | Authority |
|---|---|
| Client rules | [MOBILE_SURFACE.md](MOBILE_SURFACE.md) |
| User-facing behavior | [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md) |
| Visual / interaction | [MVP_REFERENCE.md](MVP_REFERENCE.md) |
| Crisis copy | [SAFETY_COPY.md](SAFETY_COPY.md) |
| Shared HTTP contract | Repo file `docs/openapi/v0.json` in `scrimshawlife-ctrl/SUAS` (clients pin that file; the Worker does not serve `/openapi.json`), interpreted through [API.md](API.md) / [APIS.md](APIS.md) |
| Environment | [ENVIRONMENT.md](ENVIRONMENT.md); shared testing is `STAGING` |
| Auth / session | [AUTH.md](AUTH.md); opaque Bearer only (`Authorization: Bearer <credential>`); native clients do not use the v0.6.0 `/app` cookie; client sends the raw token; `Idempotency-Key` on unsafe commands ([API.md](API.md) §7) |

The OpenAPI file is the machine-readable inventory of **implemented** Plane A paths. [API.md](API.md) remains the product command doctrine. Where they disagree, do not invent a third path. Register the already-specified command on `/api/v0`, or return the gap here. Clients accept the `OBSERVED` auth status-code drift (`202` / `201` / `204`) rather than requiring OpenAPI’s documented `200`. Check-In answer writes use the route-file body `{question_id, answer_option_id}` until OpenAPI gains that `requestBody`; do not invent a different shape.

## 4. How — architecture

```text
iOS app (Swift, existing repo)
Android app (Kotlin, existing repo)
        |
        |  HTTPS + Authorization: Bearer <opaque credential> + Idempotency-Key
        |  (native HTTP; not a WKWebView / browser CORS fetch)
        v
SUAS product API  /api/v0   (scrimshawlife-ctrl/SUAS)
        |  contract: repo docs/openapi/v0.json (not /openapi.json)
        |
        v
identified opt-in platform  (existing modular monolith)
```

Rules:

1. **Native remains native.** iOS stays Swift in `scrimshawlife-ctrl/suas-ios`. Android stays Kotlin in `scrimshawlife-ctrl/suas-android`. No Flutter, React Native, or KMP harness. No new shared-app repository.
2. **One product API.** Clients call `/api/v0` only. No `/api/mobile`, no client-type version header, no negotiated media-type version ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §4).
3. **No generated-client mandate.** `OBSERVED`: SUAS has no generated SDK and no OpenAPI generator; drift check only. Each app keeps a hand-written client pinned to the repo OpenAPI file. A generator is permitted later as mechanism; it is not required by this packet.
4. **HTML `/app/*` is not a domain command.** The web UI may keep HTML POSTs for browsers. A native client composes released JSON commands. `POST /app/qrf/deploy` is HTML UI, not `/api/v0`. Do not treat it as the mobile case-open.
5. **Native HTTP, not in-app browser fetch.** `OBSERVED`: no CORS. Use the platform HTTP client. Do not load `/api/v0` through `WKWebView` or a browser cross-origin fetch.
6. **Opaque bearer only.** Send `Authorization: Bearer <credential>`. Do not send or read the v0.6.0 HTML `/app` cookie. Do not HMAC the token on the device; HMAC is server-side storage only.
7. **Plane A only.** The device never holds a provider credential and never calls a Plane B capability ([SECURITY.md](SECURITY.md) §4 rule 7).
8. **Worker/product API changes** are allowed only to expose an already-specified `/api/v0` command that native clients need and that OpenAPI does not yet register. They are not allowed to add mobile-only semantics. Auth status-code drift and the missing Check-In `requestBody` are recorded; this packet does not invent replacements.

## 5. Environment and configuration

Each native build is a build under [ENVIRONMENT.md](ENVIRONMENT.md) §3 (Client builds) and [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §8.

Required on every build, stated explicitly, never inferred from hostname, debug/release, or store channel:

| Slot | Rule |
|---|---|
| Environment class | `LOCAL` \| `TEST` \| `STAGING`. `PRODUCTION` is invalid until SPEC-018. |
| Spec pin | Released stack version the build claims (`0.6.0` or the pin SUAS currently implements). Mismatch fails closed. |
| Manifest pin | Release manifest identifier. Mismatch fails closed. |
| API base URL | Configurable. Not hardcoded to `http://localhost:3000` on a shared-testing build. Non-loopback traffic is TLS. |
| Tenant scope | Pinned configuration until tenant-before-auth is decided. Not a Veteran-facing picker. |
| Build info | App commit/version, spec version, manifest id, build timestamp, environment class. No secrets. No Veteran PII. |

`STAGING` builds may target the `OBSERVED` synthetic host `https://suasqrf.com` or another owner-identified STAGING base URL. They must not target production data.

LOCAL-only endpoints (`/api/v0/dev/...`) may exist in a `LOCAL` workstation build. They must not be compiled into, advertised in, or reachable from a `STAGING` or shared-testing build.

This packet adds **no** new configuration variable. In particular it adds no push-channel mode.

## 6. iOS plan

Keep the existing Swift client. Change it so it is a configurable `/api/v0` client of the identified platform.

1. Replace hardcoded `Backend.baseURL` / tenant with the §5 configuration object. Fail closed on missing or unknown values.
2. Use HTTPS for any non-loopback host. `http://localhost:3000` is LOCAL-workstation only.
3. Stop using `POST /app/qrf/deploy` (and any `/app/*` HTML command) as case-open or any other domain command. That path is HTML UI, not `/api/v0`.
4. Open or reuse a Support Case through a released JSON command (see §9). Then create Service Requests with `POST /api/v0/cases/{caseId}/service-requests` and `Idempotency-Key`, as the file already does.
5. Retry unsafe commands with the **same** idempotency key. Treat an authoritative replay as success. Do not mint a new key because the network dropped.
6. Consume growing lists with `cursor` + `limit`. Do not download complete history.
7. Honor the released error contract, including `429` backoff ([API.md](API.md) §6; [APIS.md](APIS.md) §6). Accept runtime auth statuses `202` / `201` / `204` even though OpenAPI documents `200`.
8. Send the raw opaque `session_credential` as `Authorization: Bearer <credential>`. Do not HMAC it. Do not display or depend on `expires_at`.
9. Record the D-034 gap: `AppState.swift` persists the bearer in `UserDefaults`. Do not close D-034. Do not persist Veteran domain data. Do not treat `UserDefaults` as the at-rest contract.
10. Gate `LocationManager` so location is one-time and purpose-scoped only where a released workflow collects it. No continuous or background location.
11. Staging login is released challenge/verify only. `GET /api/v0/dev/last-challenge` and `POST /api/v0/dev/service-requests/{id}/simulate` are not in OpenAPI and `404` on `https://suasqrf.com`. Compile them out of `STAGING` builds; do not call them as sign-in.
12. Pin `docs/openapi/v0.json` from the SUAS repo. Do not fetch `/openapi.json` from the Worker.
13. Use `URLSession` (or equivalent native HTTP). Do not call `/api/v0` through `WKWebView`.
14. Render [SAFETY_COPY.md](SAFETY_COPY.md) verbatim; ship `988` / Veterans Crisis Line local constants for crisis fallback.
15. Expose the build-info surface.

## 7. Android plan

Keep the existing Kotlin Compose app. Give it the **same** Veteran client surface as iOS.

1. Add a hand-written `/api/v0` client pinned to the SUAS repo OpenAPI file. Smallest Veteran loop first: health, challenges, verify, logout, `GET /api/v0/veterans/me`, Check-In start/read/respond/complete. Check-In answers use `{question_id, answer_option_id}`. Then add `GET /api/v0/immediate-resources` and the other Veteran JSON paths iOS already calls.
2. Apply the same §5 configuration, TLS, fail-closed, tenant-pin, opaque Bearer, native-HTTP, and build-info rules. No `/app` cookie. No CORS assumption. No generated SDK.
3. Replace scaffold copy that invents providers, dispatch, payment, or unofficial crisis instructions with [MVP_REFERENCE.md](MVP_REFERENCE.md) hierarchy and [SAFETY_COPY.md](SAFETY_COPY.md) wording.
4. Wire `I NEED SUPPORT` / QRF / released categories to JSON commands and truthful states. Non-operational cards stay visibly non-operational.
5. Same session, idempotency, pagination, error, and consent-at-use-time rules as iOS. Do not persist Veteran domain data. Do not close D-034.
6. Do not add push, social login, contact-list access, or continuous location while filling in the scaffold.

## 8. Shared client rules (both apps)

| Topic | Rule |
|---|---|
| Version selector | `/api/v0` only |
| Auth | Passwordless challenge → opaque Bearer (`Authorization: Bearer <credential>`) → logout. Accept `202`/`201`/`204`. No `/app` cookie. No device HMAC. No `/dev/*` on STAGING. |
| Contract pin | Repo `docs/openapi/v0.json`; Worker `/openapi.json` is `404` |
| Transport | Native HTTP client. Not `WKWebView` / browser cross-origin fetch (no CORS). |
| Unsafe writes | `Idempotency-Key`; stable across retry |
| Lists | `cursor` + `limit` |
| Consent | Server at use time; never a cached grant |
| Crisis | Approved copy; local `988` / Veterans Crisis Line fallback |
| Logs | No credentials, Veteran identifiers, or sensitive free text in device logs, crash reports, analytics, or screenshots |
| Accessibility | WCAG 2.2 AA remains the target; platform a11y is mechanism, not a substitute ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §7) |

## 9. Product API obligation — case-open gap

`OBSERVED`: a Veteran native client today has no registered JSON case-open command. [API.md](API.md) §8 names `POST /cases`. OpenAPI and `src/http/routes/cases.ts` register GET queue / GET-by-id / responder commands only. iOS currently posts HTML `/app/qrf/deploy`. That path is HTML UI, not `/api/v0`. Do not treat it as the mobile case-open.

`INFERRED`: the HTML path is a browser command wired in SPEC-017 Slice 10, not the mobile contract.

Conservative close (no new semantics):

1. Native clients must not depend on `/app/*`.
2. `scrimshawlife-ctrl/SUAS` must register a Veteran-reachable case-open on `/api/v0` that already exists in doctrine — [API.md](API.md) §8 `POST /cases` — with `Idempotency-Key`, one-winner reuse of the Veteran’s non-closed Case ([CASES.md](CASES.md) §3.1), and an OpenAPI path. That is implementation of a released command, not a new endpoint family.
3. If owner review finds `POST /cases` is the wrong already-specified command, return the gap to `SUAS-specs`. Do not invent `/api/mobile`, a compound deploy, or a client-chosen tenant override.
4. Until that JSON command is registered, a native client may read `GET /veterans/me` (`open_case`) but must not pretend HTML deploy is the released mobile command.

This packet does not authorize any other Worker change.

## 10. Prohibited approaches

- New harness repo; Flutter / React Native / KMP rewrite.
- Generated-client requirement.
- Second API prefix or mobile-only version selector.
- Enabling push, social login, store distribution, or production by configuration.
- Staging login through `/api/v0/dev/last-challenge` or `/api/v0/dev/service-requests/{id}/simulate` (not in OpenAPI; `404` on `https://suasqrf.com`).
- Treating `POST /app/qrf/deploy` as the mobile case-open.
- Fetching `/openapi.json` from the Worker, or requiring a generated SDK.
- Calling `/api/v0` through `WKWebView` or a browser CORS fetch.
- HMAC-ing the session token on the device, or sending the v0.6.0 HTML `/app` cookie instead of the raw Bearer.
- Closing D-034 by moving `UserDefaults` to Keychain/Keystore “because that is what platforms do.” Record the iOS `UserDefaults` gap; leave D-034 open.
- HIPAA or live-ops claims. D-006 stays `DECISION_PENDING`.
- Treating `https://suasqrf.com` as production. It is `OBSERVED` synthetic STAGING.

## 11. Suggested implementation order

Order only. Not a definition of done. Not a completeness claim.

1. Specify accepted (this packet).
2. SUAS: register Veteran-reachable `POST /cases` (or return the gap) and refresh `docs/openapi/v0.json`.
3. Shared client configuration + fail-closed + build-info on both apps.
4. iOS: drop `/app/*`; point STAGING at a configurable HTTPS base URL; keep `/api/v0` calls; compile-out `/dev/*`; staging login is challenge/verify only.
5. Android: add the same `/api/v0` client (smallest Veteran loop first) and replace untruthful scaffold copy.
6. Both: crisis fallback, consent-at-use-time, idempotent retries, cursor lists. Record the iOS `UserDefaults` bearer gap; do not close D-034.
7. Synthetic STAGING evidence against [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md) §6 and [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §11.

## 12. Testability

Demonstrate with deterministic synthetic fixtures, not real Veterans:

1. Both apps call only `/api/v0` paths present in the pinned repo OpenAPI file (plus the §9 command once registered). They do not fetch `/openapi.json`.
2. No `/app/*` command from a native client. `POST /app/qrf/deploy` is not treated as case-open.
3. Unsafe commands replay with the same `Idempotency-Key`. Auth uses raw Bearer; challenges `202`, verify `201`, logout `204` are accepted.
4. `STAGING` sign-in is released challenge/verify. `/api/v0/dev/*` is not called and `404`s on `https://suasqrf.com`.
5. Crisis surface still presents `988` and the Veterans Crisis Line when `GET /api/v0/immediate-resources` fails.
6. Android no longer shows unofficial crisis wording or invented provider/dispatch/payment claims.
7. iOS is not localhost-only.
8. No push registration, social login, contact-list permission, continuous location, or provider secret in the bundle.

These extend [TESTING.md](TESTING.md) §7–§8. They do not advance a readiness gate.

## 13. Remains blocked

- Production, pilot launch, real Veteran data, application-store distribution (SPEC-018).
- D-034 on-device at-rest contract.
- D-006 / `HIPAA_APPLICABILITY`.
- Device push (`FUTURE`).
- Production VA credentials, production redirects, VA callbacks, VA reporting, VA launch. D-035 is optional status-only sandbox; D-016 remains the fallback.
- Real external provider effects; shelter reservation remains `BLOCKED_BY_PAYMENT_ARCHITECTURE` absent a documented card-free enterprise contract.
- Native Responder/Admin offered to real responders ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §9).
- Self-service enrollment and tenant discovery.
