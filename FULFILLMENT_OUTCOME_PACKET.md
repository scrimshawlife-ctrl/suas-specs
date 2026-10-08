# FULFILLMENT_OUTCOME_PACKET.md: owner sheet for G-I-6, G-I-7, and G-I-8

**Status:** draft for the owner / not a settlement  
**Lifecycle:** not a stack bump / does not replace Wave C  
**Stack:** inherits `0.6.0`  
**Binding rule until this sheet is settled:** [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md) C1  
**Open questions:** `suas` `docs/SPEC_GAP_PLAN.md` C1  
**Disjunction this sheet does not resolve:** [FULFILLMENT.md](FULFILLMENT.md) §5 and §7  

This sheet lists the three fulfillment questions and the answers that are already in force. It does not choose a new answer. It does not authorize pilot, production, a provider, a readiness-gate change, or SPEC-018.

Wave C remains the rule. The word "typically" in [FULFILLMENT.md](FULFILLMENT.md) §5 is the open disjunction. It is not a decision.

## 1. Questions

| Id | What the owner must answer |
|---|---|
| G-I-6 | Who may declare `ServiceFulfillment.PARTIAL`, on what evidence, and whether a request may become `FULFILLED` from partial work. |
| G-I-7 | Who may dispute, from which fulfillment states, and which exits exist besides "never back to `CONFIRMED`." |
| G-I-8 | Whether fulfillment `FAILED` leaves the request actionable, or moves it to `UNFULFILLABLE`, and when that move happens. |

## 2. Answers in force today

| Id | Rule until a later settlement |
|---|---|
| G-I-6 | No Veteran or Responder command declares `PARTIAL`. A request does not become `FULFILLED` from partial work. `FULFILLED` still requires `COMPLETED` evidence. |
| G-I-7 | A dispute moves the fulfillment to `DISPUTED` and confirmation is refused after that. No new source states or actors are added by this sheet. |
| G-I-8 | `FAILED` does not, by itself, write request `UNFULFILLABLE`. The request stays actionable until an explicit released command moves it. |

Observed in `suas` on `b819d28`, not a new behavior:

- `PARTIAL` appears in the fulfillment state list. No HTTP route and no fulfillment caller sets that state.
- Provider acceptance writes fulfillment `ACCEPTED` only. It does not move the service request.
- `disputeFulfillment` and `confirmFulfillment` are library functions. Confirmation refuses `DISPUTED`, `CANCELLED`, and `FAILED`. There is no HTTP dispute or confirm route in that tree.
- `MARK_UNFULFILLABLE` is a named request transition with a required reason, from `TRIAGED`, `MATCHING`, `ASSIGNED`, or `DECLINED`. Nothing in the fulfillment path calls it.

## 3. What a later settlement may change

A filled section 5 may replace one or more rows. Code may then change only the named row. The other rows stay on section 2. Tests for a change must show the unnamed rows still refuse.

A settlement here still does not name a vendor, a retention duration, a reporting threshold, coverage hours, or a production target. Those stay on their own D-ids.

## 4. What this sheet does not do

- It does not close D-007, D-009, D-021, D-023, D-024, or D-025.
- It does not open chat, on-duty matching, dashboard numbers, or resource share.
- It does not move `AUTH`, `CONSENT`, `CHECK-IN`, `COORDINATION`, `EXTERNAL_FULFILLMENT`, `UI_CONFORMANCE`, `SAFETY`, `PRIVACY`, `SCALE`, `RESILIENCE`, `OPERATIONS`, or `REPORTING`.
- It does not open SPEC-018.

## 5. Owner response block

```text
Settlement: UNFILLED
Date:
Owner:
G-I-6: KEEP_CURRENT_DEFAULT
G-I-7: KEEP_CURRENT_DEFAULT
G-I-8: KEEP_CURRENT_DEFAULT
Replacement text: none
Evidence authority: none
```

`KEEP_CURRENT_DEFAULT` above is the blank form, not a recorded owner choice. To replace a row, change that line to `REPLACE` and write the answer under Replacement text. To keep the row, an owner records `KEEP_CURRENT_DEFAULT` with a date and a name. Until then Wave C stands.
