# RELEASE_DECISIONS-0.7.0.md: DRAFT decision ledger for a future 0.7.0

> **DRAFT. Not released.** This file is not a release, has no `RELEASE_MANIFEST-0.7.0.md`, and has no tag. The stack stays `0.6.0` ([STATUS.md](STATUS.md)). It becomes a release decision ledger only when the owner releases `0.7.0`; until then it changes no lifecycle, gate, or decision status.

**Release:** `0.7.0` (DRAFT, not released)  
**Owner:** `@scrimshawlife-ctrl`  
**Owner decision on this release:** `NOT_RECORDED` (no 0.7.0 release decision exists yet)  
**Draft date:** `2026-10-07`  
**Supersedes:** nothing until released; [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md) and inherited ledgers stay in force  
**Production readiness:** `NOT_READY`

## D-037 record

This is task `FR-T-SPEC-002` in [D037_TASKS.md](D037_TASKS.md): after the owner's `ACCEPT_AS_SPECIFIED`, add D-037 to a future release decision ledger without claiming runtime authority. Ledger row only.

| ID | Global decision status | Boundary carried by this ledger |
|---|---|---|
| D-037 | `DECIDED` 2026-09-17: `ACCEPT_AS_SPECIFIED` by `scrimshawlife-ctrl` (Danny) on [PR #25](https://github.com/scrimshawlife-ctrl/suas-specs/pull/25) | Organizational funding readiness and evidence-reuse overlay (`SUAS-FUNDING-READINESS-001`), packet [D037_INDEX.md](D037_INDEX.md), is accepted specification text only. No runtime authority, no limited-implementation authority, no spending, eligibility, or grant-application authority. |

### What the record keeps as it is

- FR-1 is `PASS` as specification; FR-2 through FR-5 remain `NOT_READY` ([D037_TASKS.md](D037_TASKS.md) gate table).
- SAM positioning and the `$300` Google Cloud credit envelope remain `OPERATOR_ASSERTED`; UEI and eligibility remain `NOT_COMPUTABLE` ([D037_INDEX.md](D037_INDEX.md)).
- D-001, D-005, and D-010 stay open. D-037 does not close them ([DECISIONS.md](DECISIONS.md)).
- `suas`, `suas-ios`, and `suas-android` receive no tasks from the D-037 packet.

## Authority boundary

This draft records an existing owner decision for a future ledger. It authorizes nothing new: no runtime work, no Run 001, no credit spend, no grant application, no pilot or production operation. Releasing `0.7.0`, and whether this row belongs in it, is the owner's call.
