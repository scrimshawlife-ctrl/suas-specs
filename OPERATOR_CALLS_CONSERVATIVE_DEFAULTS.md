# OPERATOR_CALLS_CONSERVATIVE_DEFAULTS.md

**Lifecycle:** `owner-accepted fail-closed` / implementation-binding / not a stack bump  
**Stack:** inherits `0.6.0`  
**Owner settlement:** [OPERATOR_CALLS_2026-09-25.md](OPERATOR_CALLS_2026-09-25.md)  
**Wave C (unchanged):** [WAVE_C_CONSERVATIVE_DEFAULTS.md](WAVE_C_CONSERVATIVE_DEFAULTS.md)  
**Does not close:** D-001, D-002, D-005, D-006, D-008, D-010, D-013  
**Does not authorize:** production, pilot, store, readiness READY, HIPAA claims, credit spend, Lyft effects  

Runtime must not invent product behavior for these ids. A later D-id or release may replace any row.

## Hosting / database

| Id | Default until a later decision |
|---|---|
| D-005 Production Postgres | **Neon preferred.** Synthetic STAGING already uses Neon + Hyperdrive. Prefer Neon for any later production DB. If counsel requires a BAA path: Neon Scale plan, accept org BAA, enable project HIPAA (irreversible per Neon docs). Still no production Veteran data until SPEC-018. |
| D-006 classification | Remains counsel-owned / `DECISION_PENDING`. Neon HIPAA features are vendor controls, not a SUAS classification. |

## Adapters and channels

| Id | Default until a later decision |
|---|---|
| D-019 Food vendor | Manual / fake / information-only only. No production food adapter. |
| D-020 External peer vendor | Manual / internal QRF only. No external peer-support API adapter. |
| D-003 SMS | Channel unavailable. Do not fake send success. |
| D-017 Lyft expansion | Deferred. Uber remains the only released API-backed transportation family. No Lyft credentials or effects. |
| D-014 Geocoding/maps | Unavailable / not required on this pin. |

## Client / device

| Id | Default |
|---|---|
| D-034 On-device data | Memory-only session credential. Clear stale disk keys. No local veteran domain persistence. |

## Measurement / reporting / scale

| Id | Default |
|---|---|
| D-025 Aggregate reporting | Disabled. No small-cell threshold. Tiles stay `NOT_COMPUTABLE`. |
| D-021 / D-023 / D-024 | Workload, SLO, and RTO/RPO stay `NOT_COMPUTABLE`. Harness refuses invented numbers. |

## Ops / durability / retention

| Id | Default |
|---|---|
| D-009 Coverage hours | No coverage/duty store (aligns Wave C G-I-30). |
| D-022 Durable queue | Production vendor pending. LOCAL/TEST declared non-durable fake only. |
| D-007 Retention | No reaper invents durations. |

## Auth network signal (D-036)

| Field | Value |
|---|---|
| Option | **C** — destination/account limits only |
| Network budget | none (`NOT_APPLICABLE`) |
| Claim network throttling implemented | **no** |

Released destination challenge limits remain in force.

## Rev 3 draft (D-026…D-032)

Out of scope for pin `0.6.0` implementation. Do not assume `island_id == tenant_id` or invent island staffing/reporting rules.
