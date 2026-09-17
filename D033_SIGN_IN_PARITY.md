# Sign-in on web, iOS, and Android

**Stack:** `0.6.0`  
**Does not change:** D-002, D-003, D-034  
**Parents:** [AUTH.md](AUTH.md) §9.1, [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md)

Signing in means: an already-enrolled person proves they control their email, the server issues a one-time code, then the server issues a session. That session is the only proof they are signed in.

This is not account creation. It does not write a User, Pilot enrollment, membership, consent, or Veteran record.

## How each client holds the session

| Client | Holds the session as | Sends the code through |
|---|---|---|
| Web `/app` | Cookie on `/app` only (`Secure`, `HttpOnly`, `SameSite=Strict`) | Form posts to `/app/auth/challenges` and `/app/auth/verify` |
| iOS | `Authorization: Bearer …` | JSON `POST /api/v0/auth/challenges` then verify |
| Android | Same Bearer header | Same JSON as iOS |

Phones do not use the web cookie. The web app does not use the Bearer header on `/app` writes. `/api/v0` does not accept the cookie.

Do not wrap `/app/join` in a WebView and call that the phone app.

## Same rules everywhere

- Email code through Resend when email is available. Do not offer SMS while D-003 is open.
- Unknown and known addresses get the same on-screen confirmation. Unknown addresses get no email.
- The person does not pick a tenant.
- No Apple, Google, password, or long-lived token.
- Staging sign-in is the real code the person received. `/api/v0/dev/…` is not sign-in on `https://suasqrf.com`.
- Sign-out revokes the server session. Web also clears the cookie. Phones drop the Bearer token.
- If the server later rejects the session, the person signs in again the same way. The app does not show a countdown.

Web, iOS, and Android then show the same Veteran actions. Buttons may look native. The meaning may not change.

Android still needs the JSON client iOS already started. Copying the web form is not that client.
