# RELEASE_DECISIONS-0.6.0.md — Resend email and browser authentication settlement

**Release:** `0.6.0`  
**Owner:** `@scrimshawlife-ctrl`  
**Owner decision:** `ACCEPT`  
**Decision date:** `2026-08-30`  
**Supersedes:** inherited D-004 release boundaries  
**Production readiness:** `NOT_READY`

## D-004 settlement

| ID | Global decision status | Released boundary |
|---|---|---|
| D-004 | `DECIDED` | Resend is the only EMAIL delivery provider. Every other email provider is out of scope unless a later owner decision supersedes this record. |

### Accepted contract

- Provider: `RESEND` behind the SUAS-owned `EmailPort`.
- Runtime mode: `SUAS_EMAIL_MODE=resend`.
- Required secret/config slots: `RESEND_API_KEY` and `SUAS_EMAIL_FROM`.
- EMAIL OTP and magic-link challenges use the same Resend adapter as operational EMAIL; no second provider client exists.
- Provider payloads, acknowledgements, failures, and webhook schemas remain adapter-local.
- Provider acceptance does not authenticate a user. Only atomic SUAS challenge verification creates a session.
- Unknown or unenrolled destinations receive the same public challenge response as enrolled destinations and do not trigger an email.
- Rate limits, single-use challenges, expiry, attempt limits, audit events, redaction, and idempotency remain mandatory.

### Environment boundary

- `LOCAL` and `TEST` continue to use `disabled|fake|sink`; they must not contact Resend.
- `STAGING` may use `resend` only for explicitly enrolled, owner-approved test accounts. This is authentication-delivery evidence only, not real Veteran operation or a support-provider effect.
- `PRODUCTION` may select `resend` only after SPEC-018 and all applicable launch gates pass.
- Selecting Resend does not authorize marketing email, arbitrary recipient discovery, or any notification lacking its required consent or system basis.

## Browser passwordless transport

The HTML `/app` surface may exchange a verified EMAIL OTP for the same server-revocable opaque session used by `/api/v0`. The browser receives the credential only in a `Secure`, `HttpOnly`, `SameSite=Strict` cookie scoped to `/app`; API and native clients continue to use `Authorization: Bearer`.

- A deployment-enabled browser sign-in surface is pinned to one configured tenant before authentication. The tenant is server configuration, not a user-supplied form field.
- Browser sign-in is for an already-enrolled destination. It does not create a User, PilotEnrollment, membership, role, consent, or Veteran record.
- Challenge issuance remains non-enumerating. The page uses the same confirmation copy whether or not the destination is enrolled.
- Cookie-authenticated state-changing `/app` requests must reject cross-origin submissions.
- Logout revokes the authoritative session and clears the browser cookie.
- Responder and administrator access still require active membership and MFA as specified elsewhere.

## Authority boundary

This release closes D-004 and repairs the browser transport contract. D-002 remains open for the eventual production auth implementation/provider decision. Pilot and production remain blocked. No real Veteran data, self-service enrollment, provider fulfillment effect, reporting authority, deletion/export execution, or production launch is authorized.
