# Wave C conservative defaults

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Stack:** inherits `0.6.0`  
**Source catalog:** implementation `docs/SPEC_GAP_PLAN.md` Wave C, `docs/SPEC_DESIGN_GAPS.md`  
**Does not close:** D-009, D-019–D-025, D-034  
**Does not authorize:** production, pilot, `REPORTING=READY`, chat, on-duty matching

P-1…P-23 already ratify the Bucket I items that had a tested rule. Wave C was left open because those rows need a product choice. Until the owner writes that choice, the runtime must not invent one. This file records the fail-closed default so SPEC-017 can stop treating silence as a missing feature.

A later D-id may replace any row. Until then the default is the rule.

## C3 — Surfaces that exist as pages, not as domain

| Id | Default until a later decision |
|---|---|
| G-I-30 On duty | No availability store. No duty window. No matching on duty. `/app/responder` keeps the On Duty heading and states unavailability. No `POST` that writes duty. D-009 (hours) is separate and still open. |
| G-I-31 Chat | No thread. No message. No compose. `/app/chat` and any phone Chat tab state unavailable. See [D033_CHAT_PARITY.md](D033_CHAT_PARITY.md). |
| G-I-32 Dashboard numbers | `Responses`, `Rating`, `This Month`, `Avg Response` have no formula. Render `NOT_COMPUTABLE` / no released definition. Do not print `0`. See [D033_METRICS_PARITY.md](D033_METRICS_PARITY.md). D-025 stays open. |
| G-I-33 Quick Resource Share | Category cards only. No share command. No consent scope named “share this resource.” |

These four are **filled** as unavailable / not computable. They are not filled as product.

## C4 — Auth / tenancy

| Id | Default |
|---|---|
| G-I-34 Timing numbers | Challenge TTL, session idle/absolute timeout, MFA elevation TTL, and rate-limit bounds stay labelled inferred in code. This file does not publish seconds. Do not show a countdown from an `expires_at`. |
| G-I-35 Tenant at sign-in | The person does not pick a tenant. The server binds the enrolled contact to its tenant ([AUTH.md](AUTH.md) §9.1, v0.6.0). A client-supplied tenant override is rejected. |

G-I-35 is filled by the 0.6.0 auth rule. G-I-34 is filled only as “no published policy number.”

## C1 — Fulfillment outcomes

Until the owner writes the table:

| Id | Default |
|---|---|
| G-I-6 PARTIAL | No Veteran or Responder command declares `ServiceFulfillment.PARTIAL`. A Request does not become `FULFILLED` from partial work. `FULFILLED` still wants `COMPLETED` evidence ([DISPATCH.md](DISPATCH.md) §4). |
| G-I-7 DISPUTED | Keep the existing “never back to `CONFIRMED`” edge. Do not add new source states or actors in this file. |
| G-I-8 FAILED → request | Fulfillment `FAILED` does not, by itself, write Request `UNFULFILLABLE`. The Request stays actionable until an explicit released command moves it. |

## C2 — Events and settlement shape

| Id | Default |
|---|---|
| G-I-15 Extra Domain Events | Do not emit new Service Request Domain Events from this file. Audit-only transitions stay audit-only. |
| G-I-19 Settlement summary | Keep the structured `requested` / `occurred` / `fulfilled` / `unresolved` objects the resolve command already takes. Do not replace them with a free-text blob. Do not add fields here. |
| G-I-20 Category required details | Do not add per-category required body fields here. Empty allowed fields stay empty. |

## C5 — Notifications / consent templates

| Id | Default |
|---|---|
| G-I-37 Templates / webhook numbers | No new template vocabulary. No webhook signing scheme. No retry-second table. |
| G-I-38 Consent-template admin API | Not a released admin route. Bootstrap data is not a public publication surface. |

## Already closed — do not reopen

P-1…P-23, D-011, D-012, D-015, D-016, D-017, D-018, D-004, D-033. G-I-28 action is `APPLY_EFFECTIVE_SIGNAL` (RED only).

## Still owner-only

D-003, D-006, D-007, D-009, D-010, D-013, D-014, D-019–D-025, D-034. Those need values. This file does not supply them.
