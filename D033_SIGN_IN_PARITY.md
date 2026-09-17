# D033_SIGN_IN_PARITY.md — Web / iOS / Android sign-in meaning

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Stack:** inherits `0.6.0`  
**Does not close:** D-002, D-003, D-034, D-036  
**Does not authorize:** production, store distribution, self-service enrollment  
**Parents:** [AUTH.md](AUTH.md) §9.1, [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md), [MOBILE_SURFACE.md](MOBILE_SURFACE.md), [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md)

Sign-in is one product act. Transport differs by client. Meaning does not.

## 1. Same act

An already-enrolled Veteran (or responder, where that role is offered) proves control of an enrolled channel. The server issues a single-use challenge, then a server-revocable opaque session. That session is the only proof of sign-in.

This act does **not** create a User, PilotEnrollment, membership, role, Consent Grant, or Veteran record. Enrollment stays [ONBOARDING.md](ONBOARDING.md). Recovery stays [AUTH.md](AUTH.md) §7.

## 2. Transport by surface

| Surface | Repository | How the session is held | How the challenge is submitted |
|---|---|---|---|
| HTML `/app` | `suas` | `Secure; HttpOnly; SameSite=Strict` cookie, `Path=/app` only | HTML form POST `/app/auth/challenges` then `/app/auth/verify` |
| iOS native | `suas-ios` | `Authorization: Bearer <opaque credential>` | JSON `POST /api/v0/auth/challenges` then `POST /api/v0/auth/challenges/commands/verify` |
| Android native | `suas-android` | `Authorization: Bearer <opaque credential>` | Same JSON commands as iOS |

Rules that follow from that table:

1. Native clients do not read or send the `/app` cookie.
2. The HTML surface does not use `Authorization: Bearer` for `/app` writes.
3. `/api/v0` never accepts the browser cookie as a second API auth scheme.
4. No surface uses `/app/*` HTML commands as a native domain command.
5. Status codes on the JSON path may be `202` / `201` / `204` even when OpenAPI still says `200`. Clients accept the runtime codes.

## 3. Rules that are identical on every surface

| Rule | Binding |
|---|---|
| Channel | EMAIL OTP through Resend (D-004) where EMAIL is available. Phone OTP is not offered while D-003 is open. |
| Enrolled destination only | Sign-in does not create an account. |
| Non-enumeration | Challenge issuance returns the same public confirmation for enrolled and unenrolled destinations. Unenrolled destinations receive no message. |
| Tenant | Server / build configuration. No Veteran-facing tenant picker. |
| No social login | No Apple, Google, or other platform identity. |
| No password | Veteran authentication stays passwordless. |
| No `/dev/*` on STAGING | Captured-code shortcuts are LOCAL-only and are not sign-in on `https://suasqrf.com`. |
| Logout | Revokes the server session. HTML also clears the cookie. Native drops the Bearer. |
| Later reject | Client returns to this same challenge flow. It does not display a session lifetime. |
| Crisis | D-012 copy. Native ships local `988` / Veterans Crisis Line constants. |

iOS and Android present the same Veteran journeys after sign-in ([D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md) §3–§5). Platform widgets may differ. Product meaning may not.

## 4. What each surface must not grow into

| Temptation | Rule |
|---|---|
| WebView wrapping `/app/join` as the iOS or Android app | Forbidden. Native HTTP to `/api/v0` only. No CORS, no cookie session on device. |
| Shared sign-in SDK that hides the transport split | Forbidden as a product requirement. Mechanism later is optional; this file does not require one. |
| Different confirmation copy on Android vs iOS vs `/app/join` | Forbidden. Non-enumeration copy is the same idea on every surface. |
| Account-creation CTA on any client | `FUTURE` ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §10). |
| Device push after sign-in | `FUTURE`. |

## 5. Observed implementation notes (not new authority)

- `suas` already serves `GET /app/join`, `POST /app/auth/challenges`, `POST /app/auth/verify`, `POST /app/auth/logout` when `SUAS_BROWSER_AUTH_MODE=email_otp`.
- iOS already wraps JSON challenge / verify / logout and must drop `/dev/last-challenge` on STAGING ([D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) §2.2).
- Android scaffold still lacks an API client ([D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) §2.3). Parity means it gains the same JSON sign-in as iOS, not a copy of `/app/join`.

## 6. Non-claims

This file does not bump the stack, close D-002 or D-034, register `POST /cases`, or mark `UI_CONFORMANCE` ready.
