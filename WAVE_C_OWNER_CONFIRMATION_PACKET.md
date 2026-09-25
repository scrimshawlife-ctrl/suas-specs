# WAVE_C_OWNER_CONFIRMATION_PACKET.md — Owner settlement for fail-closed Wave C

**Status:** settled `ACCEPT_AS_SPECIFIED`  
**Lifecycle:** owner settlement recorded / not a stack bump  
**Stack:** inherits `0.6.0`  
**Canon defaults:** [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md)  
**Plain English:** [GAP_ANALYSIS.md](GAP_ANALYSIS.md) · [REMAINING.md](REMAINING.md)  

This packet does **not** close SPEC-017 by itself. It does **not** authorize pilot, production, `REPORTING=READY`, chat, on-duty matching, or store distribution.

## 1. Decision to make

Choose one settlement for the Wave C fail-closed defaults already written in [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md):

```text
A. ACCEPT_AS_SPECIFIED
Keep every Wave C row as the rule until a later D-id replaces it.

B. ACCEPT_WITH_CORRECTIONS
Keep Wave C as the rule, but list row-level corrections below before coding agents treat silence as product.

C. REJECT_AND_REWRITE
Do not treat Wave C as binding. Owner will replace named rows. Until then those rows stay NOT_COMPUTABLE and must not be invented in code.
```

## 2. What Wave C already fills (fail-closed)

| Cluster | Ids | Default meaning |
|---|---|---|
| C3 pages ≠ domain | G-I-30…33 | On-duty, chat, dashboard numbers, Quick Share stay unavailable / `NOT_COMPUTABLE` |
| C4 auth / tenancy | G-I-34…35 | No published auth timing seconds; person does not pick a tenant |
| C1 fulfillment | G-I-6…8 | No PARTIAL command; DISPUTED edge unchanged; FAILED fulfillment does not auto-close Request |
| C2 events / settlement | G-I-15, 19, 20 | No new Domain Events; settlement shape unchanged; no new required category bodies |
| C5 notifications | G-I-37…38 | No new templates / webhook scheme / consent-template admin API |

## 3. What this packet does not settle

Still owner-only and **out of scope** here: D-003, D-006, D-007, D-009, D-010, D-013, D-014, D-019–D-025, D-034.

Already closed — do not reopen via this packet: P-1…P-23, D-011, D-012, D-015, D-016, D-017, D-018, D-004, D-033.

## 4. Runtime evidence already matching Wave C (OBSERVED)

These are inventory facts for owner review. They are not SPEC-017 completion.

| Claim | Evidence pointer |
|---|---|
| Chat unavailable | Web `/app/chat`; phone parity docs `D033_CHAT_PARITY.md` |
| Dashboard numbers not computable | Web `/app/responder` tiles; `D033_METRICS_PARITY.md` |
| On-duty unavailable | Web responder On Duty states unavailability; no duty store |
| Tenant not person-chosen | `suas` JSON sign-in resolves enrolled email; `tenant_id` optional |
| Native clients on `/api/v0` | `suas-ios` + `suas-android` submit MVP categories after Case open |

## 5. Owner response block

```text
Settlement: A
Date: 2026-09-25
Owner: Daniel Meyer (scrimshawlife-ctrl) — recorded from operator “ok continue” on agent recommendation ACCEPT_AS_SPECIFIED
Corrections: none
Evidence accepted for SPEC-017 STATUS claim: YES
```

Evidence `YES` (2026-09-25): after `0.6.0` completion audit landed on `suas` (`c5016fc`). See [SPEC017_EVIDENCE_PACK.md](SPEC017_EVIDENCE_PACK.md). All twelve readiness gates remain `NOT_READY`. SPEC-018 remains blocked. Coding agents must **not** flip readiness gates or start SPEC-018.

## 6. After settlement

| If | Then |
|---|---|
| A (this settlement) | Keep [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md) as implementation-binding. Lifecycle header updated to owner-accepted fail-closed. |
| B | Patch Wave C rows named in corrections, then treat the patched file as binding. |
| C | Named rows revert to open gaps in [GAP_ANALYSIS.md](GAP_ANALYSIS.md). No invented product behavior. |

SPEC-018 remains blocked until its own go/no-go evidence exists.
