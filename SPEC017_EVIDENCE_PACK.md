# SPEC017_EVIDENCE_PACK.md — Conformance evidence inventory (not STATUS completion)

**Pin:** `0.6.0` / `RELEASE_MANIFEST-0.6.0.md`  
**Date:** `2026-09-25`  
**Owner STATUS claim:** `PENDING` (do not edit [STATUS.md](STATUS.md) SPEC-017 completion language until owner marks `YES`)  
**Wave C:** settled `ACCEPT_AS_SPECIFIED` — [WAVE_C_OWNER_CONFIRMATION_PACKET.md](WAVE_C_OWNER_CONFIRMATION_PACKET.md)  
**Does not authorize:** pilot, production, store distribution, readiness-gate READY flips  

This pack lists OBSERVED pointers so the owner can accept or reject a SPEC-017 STATUS claim. It is not itself that claim.

## 1. Spec pin

| Claim | Pointer | Label |
|---|---|---|
| Specs stack `0.6.0` | [STATUS.md](STATUS.md), [README.md](README.md), [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md) | OBSERVED |
| Runtime pin `0.6.0` | `suas` `src/release/pins.ts` (`SPEC_VERSION`, `RELEASE_MANIFEST`, `SPECS_COMMIT`) | OBSERVED |
| Wave C fail-closed accepted | [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md) + owner packet settlement A | OBSERVED |

## 2. Worker / web conformance slices

| Slice | Record | Label |
|---|---|---|
| 1–12 recorded | `suas` [SPEC017_PLAN.md](https://github.com/scrimshawlife-ctrl/suas/blob/main/SPEC017_PLAN.md) + `docs/slices/SLICE_*.md` | OBSERVED (records exist; not a readiness flip) |
| Chat unavailable | Web `/app/chat`; [D033_CHAT_PARITY.md](D033_CHAT_PARITY.md) | OBSERVED |
| Metrics not computable | Web `/app/responder`; [D033_METRICS_PARITY.md](D033_METRICS_PARITY.md) | OBSERVED |
| On-duty unavailable | G-I-30 / Wave C C3 | OBSERVED |
| Case open JSON | `POST /api/v0/cases`; [D033_CASE_OPEN.md](D033_CASE_OPEN.md) | OBSERVED |
| Tenant from enrolled email | `suas` sign-in tenant resolve (`5d7d58b` lineage) | OBSERVED |

## 3. Native clients

| Claim | Pointer | Label |
|---|---|---|
| Android `/api/v0` MVP categories | `suas-android` RootActivity + `SupportKind` including `PEER_SUPPORT` | OBSERVED |
| iOS `/api/v0` MVP categories | `suas-ios` `ServiceCategory` including `PEER_SUPPORT`; staging HTTPS | OBSERVED |
| D-034 memory-only session | Android `SessionStore`; iOS clears stale disk keys | OBSERVED |
| Test harness not product | Android `MainActivity` banner TEST HARNESS ONLY | OBSERVED |

## 4. Explicitly still NOT READY

All twelve readiness gates remain `NOT_READY` per [STATUS.md](STATUS.md). SPEC-018 remains the only pilot/production go/no-go. UI_CONFORMANCE is not advanced by truthful-unavailable pages alone.

## 5. Owner accept block

```text
Evidence accepted for SPEC-017 STATUS claim: YES | NO
Date:
Owner:
Notes:
```

If `YES`, a follow-on docs PR may update [STATUS.md](STATUS.md) / [REMAINING.md](REMAINING.md) SPEC-017 wording without advancing readiness gates or SPEC-018.
