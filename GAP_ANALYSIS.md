# What is still missing

**Pin:** `0.6.0`  
**Not a stack bump.**  
**Does not mean ready for veterans or an app store.**

This page is the living gap list in ordinary language. Decision IDs stay here so implementers can find the long form. The long form lives in [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md), [DECISIONS.md](DECISIONS.md), and the implementation catalogs `docs/SPEC_DESIGN_GAPS.md` / `docs/SPEC_GAP_PLAN.md` in `suas`.

## Already true on the current pin

- Specs through SPEC-016 are accepted or released. Work now is SPEC-017: build what the pin says, send leftovers back here.
- Web sign-in for already-enrolled people works with an email code and a cookie.
- Phones sign in with the same email code and a Bearer token. They do not use the cookie.
- Opening a Support Case on phones and JSON is `POST /api/v0/cases`. One open Case per Veteran.
- Chat pages say chat is unavailable. Responder number tiles say there is no released formula.
- Uber and Amadeus adapters exist as code only. They do not book or charge.
- Funding overlay (SAM plus cloud credits) is specified. It does not move a readiness gate.

## Product holes that stay closed until someone writes a rule

These are filled as “do not invent it.” They are not filled as features.

| What you might expect | What happens today | Why |
|---|---|---|
| On-duty switch for responders | Page says unavailable | No duty store (G-I-30). Hours policy is a separate owner decision (D-009). |
| In-app chat | Tab says unavailable | No thread store (G-I-31). |
| Dashboard totals | Tiles say no definition | No formula (G-I-32). Reporting policy is D-025. |
| Share this resource | Category cards only | No share command (G-I-33). |
| Partial fulfillment | Not a command | Owner has not said who may mark partial work (G-I-6). |
| Failed provider work auto-closes the request | It does not | Owner has not chosen the map (G-I-8). |

## Owner decisions that still need real values

Do not pick numbers or vendors in code.

| Decision | In plain English |
|---|---|
| D-003 | How official text messages get sent. |
| D-006 | Whether health information is in scope. |
| D-007 | How long events and keys are kept. |
| D-009 | When coverage is considered open. |
| D-010 | How money moves for a paid booking. |
| D-013 | Lawyer review of the privacy notice. |
| D-019 | Food vendor, or stay manual. |
| D-020 | Outside peer-support vendor, or stay manual. |
| D-021 / D-023 / D-024 | Load, speed, and restore targets. Until those exist, scale is not measurable. |
| D-025 | When a small group’s numbers may be shown. |
| D-034 | How a phone may store a session or Veteran fields. Today: memory only. |

JSON sign-in still asks the app to send `tenant_id`. The person must not pick an organization. The build pins the seed tenant. Making the field optional is Worker work, not a phone invention.

## Client leftovers

| Surface | Left |
|---|---|
| Web | Chat and number tiles stay honest-unavailable. |
| Android | Food and shelter cards still do nothing. Ride submit works only on the installed launcher after sign-in. Tests still use the dummy form. |
| iOS | Typed email code works on staging HTTPS. One-tap demo login is LOCAL only. Older draft PRs that duplicated this work are closed. |

## What this is not

Not a grant product. Not production. Not a live pilot. Not store distribution. Not a claim that Google Cloud should host the product. Evidence files may use a separate Google Cloud project later; that project is not the app.
