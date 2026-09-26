# SPEC018_OWNER_LAUNCH_PACKET.md — Owner go/no-go for SPEC-018

**Status:** settled `KEEP_BLOCKED`  
**Lifecycle:** owner settlement recorded / not a stack bump / does **not** open SPEC-018  
**Stack:** inherits `0.6.0`  
**Prior settlements:** [WAVE_C_OWNER_CONFIRMATION_PACKET.md](WAVE_C_OWNER_CONFIRMATION_PACKET.md) `ACCEPT_AS_SPECIFIED`; [OPERATOR_CALLS_2026-09-25.md](OPERATOR_CALLS_2026-09-25.md); [SPEC017_EVIDENCE_PACK.md](SPEC017_EVIDENCE_PACK.md) YES  
**Plain English:** [REMAINING.md](REMAINING.md) · [GAP_ANALYSIS.md](GAP_ANALYSIS.md) · [PILOT.md](PILOT.md) · [STATUS.md](STATUS.md)  

This packet lists what the owner must decide before SPEC-018 may collect launch evidence. It does **not** authorize pilot, production, store distribution, readiness-gate READY flips, HIPAA classification, credit spend, real external effects, or inventing chat / duty / dashboard formulas / PARTIAL commands.

Coding agents must **not** treat silence as permission to start SPEC-018 product work. Settlement `KEEP_BLOCKED` keeps that rule explicit.

## 1. Decision to make

Choose one for SPEC-018:

```text
A. KEEP_BLOCKED
SPEC-018 stays blocked. Agents continue SPEC-017 residual hygiene only.
Do not assemble launch evidence as if authorized. Do not invent product for KEEP_PENDING rows.

B. OPEN_LAUNCH_DECISIONS
Owner will close or explicitly waive the launch-required rows in §2 (fill §5).
Agents may then assemble a SPEC-018 evidence checklist against named decisions only.
Still no readiness READY flips and no real Veteran data until evidence + gate moves exist.

C. REJECT_AND_REWRITE
Owner rejects this packet’s framing. Named rows stay KEEP_PENDING / DECISION_PENDING.
Do not invent product. Wait for a replacement packet from the owner.
```

## 2. Launch-required owner rows (do not invent)

These are the rows that block a real pilot / production go/no-go. Fail-closed operator calls already bind the non-launch residuals ([OPERATOR_CALLS_2026-09-25.md](OPERATOR_CALLS_2026-09-25.md)).

### 2.A KEEP_PENDING — must be owner-closed or explicitly waived

| Id | Plain English | Why SPEC-018 cares |
|---|---|---|
| D-001 | Production compute / hosting cloud | PRODUCTION environment class |
| D-002 | Production auth provider | AUTH gate / PRODUCTION auth |
| D-006 | HIPAA / health-info classification (counsel) | PRIVACY / OPERATIONS claims; Neon BAA path ≠ classification |
| D-008 | Pilot partner organizations | [PILOT.md](PILOT.md) staffing / partners |
| D-010 | Funding / billing for paid booking | EXTERNAL_FULFILLMENT paid paths; D-037 overlay does not close this |
| D-013 | Counsel review of compliance register | Required before pilot per [PILOT.md](PILOT.md) §9 |

### 2.B Fail-closed already (do not reopen via this packet)

Already settled fail-closed or deferred — keep as-is unless the owner names a replacement D-id:

D-003 SMS unavailable · D-005 Neon preferred (no production Veteran data yet) · D-007 no invented reaper · D-009 no coverage store · D-014 geocoding unavailable · D-019/D-020 manual-only food/peer · D-021/023/024 NOT_COMPUTABLE · D-022 local fake queue only · D-025 reporting disabled · D-034 memory-only default · D-036 Option C · Lyft DEFER · Wave C G-I-30…38 · Rev 3 D-026…D-032 out of scope.

### 2.C Already decided adapters (still not production-operating)

D-004 Resend · D-017 Uber family · D-018 Amadeus search (reservation payment-blocked) · D-033 native clients · D-012 safety copy. Real effects still require SPEC-018 + `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS` validity.

## 3. Evidence still required after decisions (not invented here)

Per [PILOT.md](PILOT.md) §9 and [STATUS.md](STATUS.md), a later SPEC-018 evidence pack must still show, for the target build:

- launch-applicable readiness gates READY or owner-waived with named scope;
- PRODUCTION bootstrap complete for the chosen D-001/D-002/D-005 path;
- load / failure / restore evidence without invented SLO numbers unless D-021/023/024 close;
- no real Veteran data in STAGING; PRODUCTION only after go/no-go;
- store distribution remains a separate explicit owner act (not implied by pilot).

This packet does **not** create that evidence pack. Do not mark gates READY from this file.

## 4. What this packet does not settle

- Chat, on-duty matching, dashboard formulas, PARTIAL commands (Wave C).
- HIPAA_APPLICABILITY or “HIPAA compliant” claims (D-006 counsel only).
- Spending D-037 Google Cloud credits.
- Lyft, food vendors, SMS, geocoding, aggregate reporting.
- Application-store listing.
- Folding SUAS into Abraxas / Hermes / swarm registry.

## 5. Owner response block

```text
Settlement: KEEP_BLOCKED
Date: 2026-09-26
Owner: Daniel Meyer (scrimshawlife-ctrl) — recorded from operator “recommend and continue” on agent recommendation KEEP_BLOCKED
D-001: KEEP_PENDING
D-002: KEEP_PENDING
D-006: KEEP_PENDING (counsel)
D-008: KEEP_PENDING
D-010: KEEP_PENDING
D-013: KEEP_PENDING (counsel)
Waivers: none
Evidence authority: none
```

Rationale (agent recommendation accepted): launch-required rows still lack real owner/counsel values. Opening SPEC-018 or inventing those values would violate fail-closed doctrine. A later owner document may supersede with `OPEN_LAUNCH_DECISIONS` once §2.A is filled or waived.

## 6. After settlement

| If | Then |
|---|---|
| A `KEEP_BLOCKED` (this settlement) | No SPEC-018 evidence work. Hygiene + fail-closed operator calls only. |
| B `OPEN_LAUNCH_DECISIONS` | Owner fills §5. Agents may draft `SPEC018_EVIDENCE_PACK.md` checklist only against filled/waived rows. Still no gate READY without evidence. |
| C `REJECT_AND_REWRITE` | Treat this packet as non-binding. Wait for owner replacement. |

Pin stays `0.6.0`. All twelve readiness gates remain `NOT_READY` until evidence says otherwise.
