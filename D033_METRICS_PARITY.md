# D033_METRICS_PARITY.md — Dashboard numbers across clients

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Stack:** inherits `0.6.0`  
**Parents:** [MVP_REFERENCE.md](MVP_REFERENCE.md) §9, [ANALYTICS.md](ANALYTICS.md), [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6.8  
**Gap id:** G-I-32  
**Open decision:** D-025 reporting-privacy threshold

A dashboard label is not a metric. A metric exists only with numerator, denominator, cohort, window, source events, and tenant/role scope ([ANALYTICS.md](ANALYTICS.md) §2).

## 1. Same meaning on every surface

| Surface | What may appear |
|---|---|
| HTML responder dashboard `/app/responder` | Landmark labels such as `Responses` / `Avg Response`. Value is `NOT_COMPUTABLE` with reason `No released definition`. Not `0`. |
| iOS Responder/Admin (gated by [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §9) | Same labels if the surface exists. Same `NOT_COMPUTABLE`. No invented rating or monthly count. |
| Android | Same. Scaffold copy that shows stars, “dispatched now” counts, or lives-saved style totals is forbidden. |

Veteran home does not grow a clinical or outcome scoreboard. Support Signal labels stay coordination labels ([SIGNAL_SCORING.md](SIGNAL_SCORING.md)).

## 2. Forbidden presentations

From [ANALYTICS.md](ANALYTICS.md) §4, on every client:

- suicides prevented, lives saved, clinical efficacy
- suicide-prediction accuracy, diagnosis/recovery rates
- “QRF success rate” from assignment or notification alone
- a hard-coded small-cell suppression number presented as policy before D-025 closes

`0` is a computed value. These tiles do not have a released computation. Showing `0` lies.

## 3. Conservative behavior until G-I-32 / D-025 close

1. Keep the Summary landmark so the reference dashboard stays recognizable.
2. State `NOT_COMPUTABLE` in text.
3. Do not add a JSON metrics endpoint that returns placeholder zeros.
4. Do not enable `D025_REPORTING`.
5. Native clients do not scrape `/app/responder` HTML for numbers.

## 4. Non-claims

This file does not define the four reference metrics, close D-025, bump the stack, or set `REPORTING=READY`.
