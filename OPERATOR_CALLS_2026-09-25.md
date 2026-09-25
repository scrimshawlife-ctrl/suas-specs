# OPERATOR_CALLS_2026-09-25.md — Owner calls on open residuals

**Status:** settled `2026-09-25`  
**Lifecycle:** owner calls recorded / not a stack bump  
**Stack:** inherits `0.6.0`  
**Canon defaults:** [OPERATOR_CALLS_CONSERVATIVE_DEFAULTS.md](OPERATOR_CALLS_CONSERVATIVE_DEFAULTS.md)  
**Plain English:** [GAP_ANALYSIS.md](GAP_ANALYSIS.md) · [REMAINING.md](REMAINING.md) · [DECISIONS.md](DECISIONS.md)  

Operator instruction: “review operator decisions and make calls.” This packet records those calls. It does **not** authorize pilot, production, store distribution, readiness-gate READY flips, HIPAA classification, credit spend, or inventing chat / duty / dashboard formulas / PARTIAL commands.

Wave C remains binding: [WAVE_C_OWNER_CONFIRMATION_PACKET.md](WAVE_C_OWNER_CONFIRMATION_PACKET.md) `ACCEPT_AS_SPECIFIED`.

## 1. How to read a call

| Call | Meaning |
|---|---|
| `ACCEPT_*` | Implementation-binding fail-closed / manual / unavailable rule until a later D-id or release replaces it |
| `DECIDED` | Global decision closed with the stated option (still not production-operating approval unless a release says so) |
| `DEFER` | Keep current released boundary; do not implement the expansion |
| `KEEP_PENDING` | Counsel, production hosting, or launch choice — agents must not invent |

## 2. Calls recorded

### 2.A Callable fail-closed / manual (binding)

| Id | Call | Rule until later release |
|---|---|---|
| D-019 | `ACCEPT_MANUAL_ONLY` | No production food vendor. Food stays manual/fake / information-only. Do not invent a vendor. |
| D-020 | `ACCEPT_MANUAL_ONLY` | No external peer-support vendor. Internal/manual QRF remains valid. Native `PEER_SUPPORT` submit stays manual-coordination path. |
| D-034 | `ACCEPT_MEMORY_ONLY_DEFAULT` | Native clients hold session in memory only; clear stale disk keys; do not persist veteran domain fields. Full on-device crypto remains open for a later close. |
| D-025 | `ACCEPT_REPORTING_DISABLED` | Aggregate / small-cell reporting stays disabled. Dashboard tiles stay `NOT_COMPUTABLE`. No invented thresholds. |
| D-021 / D-023 / D-024 | `ACCEPT_NOT_COMPUTABLE` | No invented workload, SLO, or RTO/RPO numbers. Resilience harness refuses numeric targets. |
| D-003 | `ACCEPT_SMS_UNAVAILABLE` | SMS channel unavailable. Do not invent a provider or fake SMS success. |
| D-009 | `ACCEPT_NO_COVERAGE_STORE` | Confirms Wave C G-I-30: no duty/coverage store; On Duty states unavailable. |
| D-014 | `ACCEPT_GEOCODING_UNAVAILABLE` | No production geocoding/maps requirement on pin `0.6.0`. Do not invent a maps vendor. |
| D-022 | `ACCEPT_LOCAL_FAKE_QUEUE` | Durable production queue vendor still open. LOCAL/TEST may use declared non-durable fake; do not claim STAGING/PRODUCTION durable jobs. |
| D-007 | `ACCEPT_NO_REAPER` | Retention durations still open. Columns may exist; no purge/reaper invents a retention window. |
| D-026…D-032 | `DEFER_REV3_OUT_OF_SCOPE` | Rev 3 draft fence-post questions stay out of pin `0.6.0` implementation. |
| D-005 | `ACCEPT_NEON_PREFERRED` | Neon remains synthetic-STAGING Postgres (already in the CF Worker + Hyperdrive topology) and is the **preferred production Postgres candidate**. If counsel later requires a BAA path for PHI at rest, use Neon **Scale** + org BAA + project HIPAA enablement ([Neon HIPAA docs](https://neon.com/docs/security/hipaa)). Does **not** authorize production Veteran data or close SPEC-018. |

### 2.B Closed with an explicit option

| Id | Call | Detail |
|---|---|---|
| D-036 | `DECIDED` — Option **C** | Destination/account challenge limits only. **No fixed network-signal budget** yet. Do not claim network throttling is implemented. Destination budget OBSERVED (3 / 15 min) stays. Form: see §4. |
| D-017 Lyft expansion | `DEFER` | Keep Uber-only released adapter family + manual paths. No Lyft credentials, quotes, bookings, webhooks, or effects. Packet stays open for later evidence; not implementation authority. |

### 2.C Keep pending (do not invent)

| Id | Why agents must not close |
|---|---|---|
| D-001 | Production compute/hosting cloud — SPEC-018 launch choice (Worker topology for synthetic STAGING is separate) |
| D-002 | Production auth provider — SPEC-018 |
| D-006 | Legal/HIPAA **classification** — counsel only; no claim either way. Neon HIPAA-eligible DB controls are a **partial infrastructure mitigation** only (see [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md) §3.A). They do **not** set `HIPAA_APPLICABILITY` or make SUAS “HIPAA compliant.” |
| D-008 | Pilot partner organizations — SPEC-018 |
| D-010 | Funding/billing — FUTURE; D-037 overlay does not close this |
| D-013 | Counsel review of compliance register — counsel only |

## 3. What these calls do not do

- Do not advance any of the twelve readiness gates.
- Do not start SPEC-018 evidence collection as if authorized.
- Do not spend D-037 Google Cloud credits.
- Do not set `HIPAA_APPLICABILITY` or claim “HIPAA compliant.”
- Do not treat Neon Scale/BAA/HIPAA project toggle as closing D-006 or authorizing PHI in production.
- Do not enable Lyft, food vendors, SMS, geocoding, or aggregate reporting.
- Do not reopen Wave C, D-004, D-011, D-012, D-015–D-018, D-033, D-035, or D-037 overlay acceptance.

## 4. D-036 owner form (Option C)

```text
D-036_STATUS=DECIDED
NETWORK_OPTION=C
ISSUE_LIMIT=NOT_APPLICABLE
WINDOW_SECONDS=NOT_APPLICABLE
WORKER_ADDRESS_SOURCE=CF_CONNECTING_IP
NODE_ADDRESS_SOURCE=SOCKET_PEER
MISSING_ADDRESS_BEHAVIOR=SHARED_UNKNOWN_BUCKET
SUBJECT_STORAGE=NOT_APPLICABLE
EXPIRED_BUCKET_CLEANUP=NOT_APPLICABLE
AUTHORIZED_ENVIRONMENTS=SYNTHETIC_STAGING
OWNER=Daniel Meyer (scrimshawlife-ctrl) — operator “review operator decisions and make calls”
DECIDED_AT=2026-09-25
CONSEQUENCES=Destination/account limits remain authoritative. No network-subject budget. No claim that network throttling is implemented. A later decision may select A or B with evidence.
```

## 5. Operator attestation

```text
Date: 2026-09-25
Owner: Daniel Meyer (scrimshawlife-ctrl)
Instruction: review operator decisions and make calls
Wave C: unchanged ACCEPT_AS_SPECIFIED
SPEC-017 evidence: unchanged YES
SPEC-018: still blocked
```

## 6. After these calls

Coding agents treat [OPERATOR_CALLS_CONSERVATIVE_DEFAULTS.md](OPERATOR_CALLS_CONSERVATIVE_DEFAULTS.md) as implementation-binding fail-closed for the rows above. Gaps that remain `KEEP_PENDING` return to the owner; they are not filled with invented product.
