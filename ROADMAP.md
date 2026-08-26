# ROADMAP.md — Specification-driven path to production

**Stack:** `0.3.0` / `released`
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`  
**Release manifest:** [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md)

The owner completed the specification acceptance chain on 2026-08-18 PT.

## Completed specification stages

| Stage | Status | Scope |
|---|---|---|
| SPEC-001 | `accepted` | product/authority/governing principles |
| SPEC-002 | `accepted` | consent/privacy/safety/security |
| SPEC-003 | `accepted` | Check-In/Support Signal/events |
| SPEC-004 | `accepted` | Cases/Service Requests/responder workflow |
| SPEC-005 | `accepted` | Resources/Referral/Fulfillment/Follow-Up/Settlement |
| SPEC-006 | `accepted` | domain/data/event/architecture reconciliation |
| SPEC-007 | `accepted` | architecture/API/auth/notifications/admin |
| SPEC-008 | `accepted` | referenced MVP visual/interaction conformance |
| SPEC-009 | `accepted` | provider-neutral fulfillment |
| SPEC-010 | `accepted` | scaling contract |
| SPEC-011 | `accepted` | resilience/degradation |
| SPEC-012 | `accepted` | testing/readiness evidence contract |
| SPEC-013 | `accepted` | deployment/operations/incident/recovery |
| SPEC-014 | `accepted` | controlled pilot/analytics |
| SPEC-015 | `accepted` | v0.1.0 decision ledger/safe deferrals |
| SPEC-016 | `released` | first implementation-authoritative cut |

## Current stage — SPEC-017

**Status:** `ACTIVE`

Objective: implement `scrimshawlife-ctrl/SUAS` against the current released manifest and continuously compare the implementation with the released contracts. The pinned release is `0.3.0`; see [STATUS.md](STATUS.md).

Rules:

1. Implementation PRs cite released artifact/section/version and the current release manifest.
2. Gaps return to `SUAS-specs`; code does not redefine canon.
3. Production-unavailable surfaces in the release manifest remain unavailable in implementation except for explicit fake/sink/manual/test scaffolding.
4. Conformance evidence covers domain states, auth, consent, provider neutrality, MVP visuals, idempotency, durability, scale/resilience semantics, and tests.
5. SPEC-017 completion does not authorize production operation.

## SPEC-018 — Pilot / production readiness

**Status:** blocked by SPEC-017 implementation/conformance plus operating evidence and required production decision closure.

Before any real pilot or production use:

- applicable readiness gates must be `READY` from reproducible evidence;
- production hosting/auth/delivery/DB/job decisions must close;
- legal/retention/partner/staffing/counsel/safety-copy/signal-rule decisions required for the launch must close;
- enabled real provider adapters must be selected and pass conformance;
- production workload/SLO/RTO/RPO targets must close and pass evidence;
- affected aggregate reporting requires D-025 policy;
- load, failure, restore, incident, and operations evidence must be attached.

## SPEC-019 — Post-launch revision

**Status:** future.

Measured pilot/launch feedback and scale data become a new version through the same specify → accept → release → conform → readiness process.

## Ordering

```text
SPEC-001 ... SPEC-015  ACCEPTED
              |
          SPEC-016  RELEASED
              |
          SPEC-017  IMPLEMENT / CONFORM   ← CURRENT
              |
          SPEC-018  LAUNCH READINESS
              |
          SPEC-019  MEASURED REVISION
```

Release authorizes implementation. It does not equal readiness or launch approval.

SPEC-0xx numbers are stage records in this chain. A released contract addition inside the current stage — a new domain artifact, a decision closure, or a client surface such as D-033 — is versioned through the release manifest and does not consume a stage number.
