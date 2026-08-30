# D033_NATIVE_CLIENT_INTEGRATION.md — Veteran native-client integration (specify)

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Decision:** D-033 (already `DECIDED`; [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md))  
**Contract:** [MOBILE_SURFACE.md](MOBILE_SURFACE.md)  
**How:** [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md)  
**Stack:** inherits current released stack `0.5.0`; this file does not bump it  
**Does not open or close:** D-034, D-006, D-002, device push, application-store distribution, production VA, or any readiness gate

This file states **what** a Veteran sees and does on the existing native iOS and Android apps when those apps talk to the identified opt-in platform. It does not add a domain concept, state, event, capability, API selector, or configuration variable. It does not define “complete.”

## 0. Epistemic labels

| Label | Meaning in this file |
|---|---|
| `OBSERVED` | Read from a released spec, a named repository file, or a named host |
| `INFERRED` | Follows from released rules plus the observed files; not independently measured |
| `SPECULATIVE` | Possible later work; not authority |
| `DECISION_PENDING` | Already open; this file does not close it |
| `FUTURE` | Already reserved; this file does not open it |

Do not treat prototype copy, a vendor API, or current app behavior as a product decision.

## 1. Purpose

A Veteran on iOS or Android uses the same identified opt-in platform a Veteran uses in the web client. The apps are installed clients. They are not a second product.

Why this file exists: D-033 already released the client contract. Two forks already exist. The Veteran-facing behavior on those forks is not yet bound to the released platform, so implementers can drift into HTML commands, localhost-only hosts, or untruthful scaffold copy. This specify file locks the user-facing behavior. [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) locks the how.

## 2. Who and where

| Item | Binding |
|---|---|
| Role | Veteran first. Responder and Admin on a native client stay gated by [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §9. |
| Surface | Identified opt-in platform only. The anonymous public front door is out of scope ([SURFACES.md](SURFACES.md) remains draft and is not implementation authority). |
| Platforms | iOS and Android. [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §2: a second platform requires no new release. |
| Environment for shared testing | `STAGING` at most ([ENVIRONMENT.md](ENVIRONMENT.md) §2). No real Veteran data. No real external effects. |
| Production / store / real-Veteran use | Blocked. SPEC-018 remains the go/no-go. |

`OBSERVED` host for synthetic shared testing: `https://suasqrf.com`. `GET /` on that host redirects to `/app`. Health: `GET /api/v0/health`. This file does not name a production host.

## 3. What the Veteran does

The journeys below are the Veteran-visible meaning of already-released obligations. Layout may follow platform convention. Hierarchy, wording that D-012 owns, destinations, and state labels may not.

### 3.1 Sign in

The Veteran signs in with a passwordless challenge on a channel the build can actually deliver ([AUTH.md](AUTH.md) §2, §9; [ONBOARDING.md](ONBOARDING.md) §7.1).

The Veteran:

1. Enters the enrolled email or phone the tenant already has for them.
2. Receives a one-time challenge on that channel.
3. Submits the challenge result.
4. Continues only after the server issues a session.

The Veteran does not create an account from the app ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §10: self-service enrollment is `FUTURE`). The Veteran does not pick a tenant. The Veteran does not use a password, Apple/Google/social identity, or a long-lived unrevocable credential.

If the chosen channel cannot deliver, the app does not offer it and does not pretend the challenge succeeded.

If the server rejects the session later, the Veteran signs in again through the same challenge flow. The app does not display a session lifetime and does not treat a locally stored value as proof that the session is valid.

Optional VA-backed status verification (D-035, settled v0.5.0 as optional status-only sandbox) is not required on this surface. D-016 self-attestation remains available. Failure, cancellation, outage, or non-confirmation of any verification path must not block an explicit support request.

### 3.2 Home / take action

After sign-in the Veteran reaches an action-first home ([MVP_REFERENCE.md](MVP_REFERENCE.md) §5):

- `I NEED SUPPORT` remains the dominant Veteran action.
- Immediate / crisis help sits above the broader catalog.
- Released operational categories are `FOOD`, `TRANSPORTATION`, `SHELTER` (temporary), and `PEER_SUPPORT`.
- Cards that exist only for visual continuity (`Counseling`, `Activities`, `Job Training`, permanent housing) stay visibly non-operational. They are not hidden operational Service Requests.

Navigation stays simple: few primary destinations, recognizable labels. Platform-native controls are allowed. Added depth or density is not.

### 3.3 Ask for support

When the Veteran asks for peer support (QRF), the action means: create or submit an explicit `PEER_SUPPORT` need and attempt responder coordination according to actual coverage, availability, consent, and operations ([MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2).

When the Veteran asks for food, a ride, or temporary shelter, the action means: create or submit the matching released Service Request. The app does not invent a provider brand, a dispatch guarantee, a free-voucher promise, or a payment path.

The Veteran can cancel a request when the recorded state allows cancel. The app does not invent a compound “deploy everything” command and does not present a client-side sequence as a single domain fact.

If the platform cannot accept the request, the Veteran sees an unavailable or degraded state. The app does not simulate success.

### 3.4 See status

The Veteran sees only recorded facts ([SAFETY.md](SAFETY.md) §5.1; [SAFETY_COPY.md](SAFETY_COPY.md) §5; [MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2):

| What the Veteran may see | Only when |
|---|---|
| `REQUESTED` | A `PEER_SUPPORT` Service Request exists |
| `SEARCHING` | Matching is in progress, or assignment exists without a recorded responder notification |
| `RESPONDER_NOTIFIED` | A notification about **this** request, addressed to the active responder, reached a sent/delivered status |
| `RESPONDER_ACCEPTED` | The request or assignment records responder acceptance |
| `NO_RESPONDER_CURRENTLY_AVAILABLE` | Matching is exhausted with no available responder |
| `DEGRADED` | A truthful degraded or no-availability operational state |
| `CANCELLED` | The request reached `CANCELLED` |
| `Call` / `Message` | An authorized contact path exists |

Assignment alone is not `RESPONDER_NOTIFIED`. `REQUESTED`, `ACCEPTED`, `DISPATCHED`, `ARRIVED`, and `RESOLVED` stay distinct. A later label appears only when its recorded fact exists.

The Veteran sees their own Check-Ins, their own Service Request status, Settlement fields written for them, and Follow-Up prompts addressed to them (D-015). The Veteran does not see full Case Notes, other veterans, responder queue internals, or other Organizations.

### 3.5 Consent

The Veteran grants or revokes consent at the moment of use. The app reads consent state from the server then, never from a remembered grant ([CONSENT.md](CONSENT.md) §3 rule 1, §4).

Installing the app, opening it the first time, or accepting terms is not a Consent Grant ([CONSENT.md](CONSENT.md) §9). Notification preferences are not consent ([NOTIFICATIONS.md](NOTIFICATIONS.md) §4).

Consent capture offers only the closed permission/scope pairings in [CONSENT.md](CONSENT.md) §2.1.

### 3.6 Crisis help

Crisis copy and destinations are the D-012 set in [SAFETY_COPY.md](SAFETY_COPY.md): **911** for immediate danger or medical emergency; **988** Suicide & Crisis Lifeline (call or text); Veterans reach the Veterans Crisis Line through 988.

The crisis surface is always present. If the server-owned crisis read fails, the app still shows `988` and the Veterans Crisis Line from local constants ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6). A failed read never yields an empty crisis surface.

The Veteran starts a call or text only by an explicit action. The app never auto-dials, never appends tracking parameters, and never substitutes another hotline, URL, or “press 1” instruction as official copy.

SUAS coordinates practical support. It is not an emergency service. The crisis surface says so, using the approved wording.

### 3.7 Session ends

The Veteran can sign out. After sign-out, or after the server rejects the credential, the app returns to sign-in and does not keep Veteran domain data on the device (D-034 `DECISION_PENDING`; persist the session credential only).

## 4. What the Veteran must never see or be asked to do

| Forbidden Veteran experience | Source |
|---|---|
| Device push prompts or push-delivered alerts | [NOTIFICATIONS.md](NOTIFICATIONS.md) §2; `PUSH` is `FUTURE` |
| Sign-in with Apple, Google, or any social identity | [AUTH.md](AUTH.md) §2, §10 |
| Access to the device contact list | [PRIVACY.md](PRIVACY.md) §3 |
| Continuous location, background location, or unexplained telemetry | [PRIVACY.md](PRIVACY.md) §3 |
| A promise that a nearby responder is already notified | [MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2 |
| A provider brand, fare, voucher, or “dispatched now” claim the platform has not recorded | [MVP_REFERENCE.md](MVP_REFERENCE.md) §6; [ENVIRONMENT.md](ENVIRONMENT.md) §2 |
| HIPAA, SOC 2, ISO, or other compliance claims | [SECURITY.md](SECURITY.md) §1, §6; D-006 remains `DECISION_PENDING` |
| An empty crisis surface | [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6 |
| Invented crisis wording or destinations | [SAFETY_COPY.md](SAFETY_COPY.md) |
| Account creation / self-service enrollment | [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §10 |
| Tenant picker | [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §10 |
| Store listing, review prompts, or production-launch language | SPEC-018 |

Veteran-facing copy does not say “transition.” If the surface describes leaving a unit or service, use “leave the formation” only when that wording is the released copy. This file does not invent that phrase.

## 5. Same behavior on both platforms

iOS and Android present the same Veteran journeys, the same released categories, the same crisis destinations, and the same truthful states. Platform widgets may differ. Product meaning may not.

A surface with no released domain fact behind it renders as unavailable. It does not render as empty, simulated, or “coming soon” in a way that implies a released workflow.

Untrusted Veteran- or responder-authored text is encoded at render.

## 6. User-visible acceptance

A build is acceptable for this specify file when a synthetic Veteran on iOS and on Android can demonstrate all of the following:

1. Sign-in uses only a deliverable passwordless channel and a server-issued session.
2. Home is action-first: support request, crisis/immediate help, then truthful category cards.
3. Asking for support creates or updates a recorded Service Request; a lost response retried by the Veteran does not create a second request the Veteran can see as two needs.
4. Status labels match §3.4. `Call` / `Message` appear only with an authorized path.
5. Crisis copy matches [SAFETY_COPY.md](SAFETY_COPY.md). `988` and the Veterans Crisis Line remain visible when the server crisis read fails.
6. No forbidden experience from §4 is present.
7. After sign-out, Veteran domain data is gone from the device; only a session credential may have been stored, and it is no longer valid to use.
8. A `STAGING` build talks to the synthetic platform and never claims to be production.

These criteria extend [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §11 and [TESTING.md](TESTING.md) §7. They do not create a readiness gate and they do not define slice completion.

## 7. Non-goals

- Production operation, real Veteran data, live pilot, or application-store distribution.
- A new mobile product identity, a `/api/mobile` surface, or a second required-surface inventory.
- Device push, social login, contact-list access, continuous location, or on-device at-rest policy (D-034 stays `DECISION_PENDING`).
- Closing D-006 or stating a HIPAA class.
- Enabling production VA, VA callbacks, VA reporting, or VA launch. D-035 remains sandbox-bounded; D-016 remains the fallback.
- Responder or Admin native work beyond the existing §9 gate.
- Rewriting [MOBILE_SURFACE.md](MOBILE_SURFACE.md), [AGENTS.md](AGENTS.md), or [HANDOFF.md](HANDOFF.md).

## 8. Gaps returned, not resolved

| Gap | Status | Conservative behavior |
|---|---|---|
| On-device protection of stored session and any later local Veteran data | D-034 `DECISION_PENDING` | Persist session only; no Veteran domain data on device |
| Challenge and session TTL constants | `DECISION_PENDING` ([AUTH.md](AUTH.md) §3, §5) | Do not hardcode or display a lifetime |
| Tenant selection before authentication | `DECISION_PENDING` | Pin tenant on the build; no Veteran-facing picker |
| Veteran-reachable case-open on the implemented `/api/v0` JSON surface | `OBSERVED` gap; see [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) §9 | Do not use HTML `/app/*` as the long-term command; do not invent a new path |
| Self-service enrollment from the client | `FUTURE` | Do not present account creation |
| Device push | `FUTURE` | In-app notification read path only |
