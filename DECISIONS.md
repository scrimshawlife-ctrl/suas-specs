# DECISIONS.md — SUAS decision register

**Stack:** `0.3.0` / `released`
**Release decision ledger:** [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md) for D-033 and D-034; inherited [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md) for D-011, [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012, [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018, [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017, and [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise.

Global decisions remain open until explicitly decided. A release-specific `DEFERRED_FOR_RELEASE` boundary does not globally close the decision; it only makes the affected capability unavailable/manual/future for that release.

## Decision register

| ID | Decision | Global status |
|---|---|---|
| D-001 | Production hosting/cloud | `DECISION_PENDING` |
| D-002 | Production auth provider/in-house implementation | `DECISION_PENDING` |
| D-003 | SMS provider | `DECISION_PENDING` |
| D-004 | Email provider | `DECISION_PENDING` |
| D-005 | Production database hosting | `DECISION_PENDING` |
| D-006 | Legal/HIPAA classification | `DECISION_PENDING`; `HIPAA_APPLICABILITY = DECISION_PENDING`. Counsel packet: [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md) (does not close this decision). |
| D-007 | Retention/deletion durations | `DECISION_PENDING` |
| D-008 | Operating pilot partner organizations | `DECISION_PENDING` |
| D-009 | Responder staffing/coverage hours | `DECISION_PENDING` |
| D-010 | Service funding/billing sources | `FUTURE` / `DECISION_PENDING` |
| D-011 | Production Support Signal scoring rules/thresholds | `DECIDED` 2026-08-23 PT for `qv-001` + `sv-001`; see [SIGNAL_SCORING.md](SIGNAL_SCORING.md) and [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md); implementation-authoritative, not production-operating approval |
| D-012 | Approved production safety/crisis copy | `DECIDED` (v0.1.5; copy + 911/988 destinations released in [SAFETY_COPY.md](SAFETY_COPY.md), [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md); copy approval only, not production-operating approval) |
| D-013 | Counsel review of compliance register | `DECISION_PENDING` |
| D-014 | Production geocoding/maps need | `DECISION_PENDING` |
| D-015 | Full Case Note veteran visibility | `DECIDED` for v0.1 default: full Case Notes are not veteran-visible |
| D-016 | Identity proofing beyond self-attest/passwordless contact | `DECIDED` for v0.1 default: no VA/DD-214/in-person proofing requirement |
| D-017 | Production transportation adapter(s) | `DECIDED` 2026-08-19 PT: Uber selected as first API-backed transportation adapter family; manual path remains required; production use still blocked until SPEC-018/readiness gates |
| D-018 | Production shelter/room adapter(s) | `DECIDED` 2026-08-19 PT: Amadeus selected as first commercial search/inventory adapter family; `ManualShelterAdapter` remains mandatory; reservation is `BLOCKED_BY_PAYMENT_ARCHITECTURE` absent a documented card-free enterprise contract; production use still blocked until SPEC-018/readiness gates |
| D-019 | Production food adapter(s) | `DECISION_PENDING` |
| D-020 | Production external peer-support adapter | `DECISION_PENDING`; internal/manual QRF remains valid |
| D-021 | Production workload/capacity envelope | `DECISION_PENDING` |
| D-022 | Production durable job/queue implementation | `DECISION_PENDING` |
| D-023 | Production performance SLOs/alerts | `DECISION_PENDING` |
| D-024 | Production RTO/RPO / backup-restore objectives | `DECISION_PENDING` |
| D-025 | Aggregate reporting privacy/small-cell policy | `DECISION_PENDING` |
| D-026 | Relationship of `island_id` to existing `tenant_id` / organization scope | `DECISION_PENDING`; draft Rev 3 contract only. Do not assume `island_id == tenant_id`. |
| D-027 | Dispatcher staffing, hours, and handoff model for island-specific routing | `DECISION_PENDING`; draft Rev 3 contract only |
| D-028 | Who curates and refreshes the island resource list | `DECISION_PENDING`; draft Rev 3 contract only |
| D-029 | Institutional reporting requirements vs collect-the-minimum data posture | `DECISION_PENDING`; draft Rev 3 contract only |
| D-030 | Dual enrollment and minors handling for Rev 3 surfaces | `DECISION_PENDING`; draft Rev 3 contract only |
| D-031 | Which legal entity contracts for island and ride operations | `DECISION_PENDING`; draft Rev 3 contract only |
| D-032 | Volunteer-driver insurance and screening requirements | `DECISION_PENDING`; draft Rev 3 contract only |
| D-033 | Native mobile client surface | `DECIDED` (v0.3.0; contract released in [MOBILE_SURFACE.md](MOBILE_SURFACE.md), [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md)); client surface only, `ENABLED` for implementation and not for production operation |
| D-034 | On-device protection of locally retained veteran data, including the stored session credential | `DECISION_PENDING`; opened by v0.3.0. [SECURITY.md](SECURITY.md) §2 covers database/backups only |
| D-035 | Optional VA-backed Veteran-status verification during onboarding | `DECISION_PENDING`; proposed contract in [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md). D-016 remains authoritative until explicit release settlement. |

D-006 remains `DECISION_PENDING`. [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md) is a counsel register packet of product facts. It is not a legal opinion and does not close D-006 or set `HIPAA_APPLICABILITY`.

D-035 is additive and currently `DECISION_PENDING`. The owner has requested VA-backed onboarding verification exploration, but no implementation default may supersede D-016 until a release settlement records the exact adapter/API family, minimum scopes, environment boundary, privacy/retention constraints, evidence references, and fallback rule.

D-011 is closed by [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md). D-033 is closed by [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md), which also opens D-034; D-033 releases a client surface only and authorizes no production operation. D-026–D-032 are additive draft questions from Rev 3 fence-post work. They do not replace D-017–D-025 in the released ledger. D-012 is closed by [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md), D-017 is closed by [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md), D-018 is closed by [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md), and D-019–D-025 remain open unless later released decisions close them.

## v0.1.0 release boundary

The first released cut is implementation-authoritative but not production-operating. Therefore unresolved production decisions are safely deferred only because the associated production surfaces are unavailable/manual-only/information-only/future in release manifests. D-017 and D-018 were later closed for adapter-local selection by v0.1.2 and v0.1.3 respectively, D-012 (safety/crisis copy) by v0.1.5, and D-011 (Support Signal scoring) by v0.2.0; those closures do not authorize production operation.

No implementation default may silently close an open decision.

## Standing decided architecture/product boundaries

- SUAS is coordination, not diagnosis/EHR/automated emergency dispatch.
- Canonical loop/concepts remain distinct.
- Scalable modular monolith is the default; microservices require measured need + released spec change.
- Correctness-critical application state is shared/persistent; production-critical async work is durable by contract.
- External fulfillment is capability-port based; provider SDKs/statuses are adapter-local; manual coordination is first-class.
- Provider state never replaces canonical Service Request/Fulfillment state.
- Referenced MVP visual/interaction identity is preserved with truthful production divergences, on every released client surface.
- Veteran auth is passwordless by contract; privileged roles require MFA; exact production provider remains open.
- No safety-critical generative decision and no automated 911/PSAP dispatch.
- Billing/Medi-Cal remains future; no billability claim.
- Controlled pilot remains approximately 25–50 veterans unless explicitly changed and is not a technical capacity ceiling.
- Operational metrics are not clinical/causal outcome evidence.

## Rules

1. Do not guess open decisions.
2. Provider/infrastructure choices are configuration/adapter decisions unless they introduce a genuinely new product capability.
3. Do not invent signal weights, crisis copy, legal status, capacity/SLO/RTO/RPO numbers, or reporting privacy thresholds.
4. When a global decision closes, record date, owner, spec version, decision, consequences, and supersedes relationship.
