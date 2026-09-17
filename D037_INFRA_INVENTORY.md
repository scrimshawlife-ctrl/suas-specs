# D037_INFRA_INVENTORY.md — FR-T-INFRA-001 staging host inventory

**Decision:** D-037  
**Task:** `FR-T-INFRA-001`  
**Parent:** FR-R-002, FR-R-003  
**Date:** `2026-09-17`  
**Scope:** public contracts in `suas-specs`  
**Runtime repositories inspected:** none  
**Runtime authority:** none  

Question: can existing `suas` STAGING host `SUAS-EVIDENCE-RUN-001` without selecting a new vendor?

This inventory does not close D-001, spend credits, declare a host, or authorize an experiment.

## Sources

- [README.md](README.md) product-surface table
- [REPOS.md](REPOS.md) (named inventory; not re-copied here)
- [ENVIRONMENT.md](ENVIRONMENT.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [D037_EVIDENCE.md](D037_EVIDENCE.md) §4.1 and §6
- [DECISIONS.md](DECISIONS.md) D-001 / D-005 / D-022 / D-023

## What is specified

| Fact | Label | Source |
|---|---|---|
| Logical environment class `STAGING` exists | `OBSERVED` as doctrine | ENVIRONMENT.md §2 |
| `STAGING` forbids real veteran data | `OBSERVED` as doctrine | ENVIRONMENT.md §2 |
| `STAGING` forbids real external effects except an allow-listed sandbox that cannot affect real people/resources | `OBSERVED` as doctrine | ENVIRONMENT.md §2, DEPLOYMENT.md §1 |
| Run 001 permitted env is `TEST` or `STAGING` | `OBSERVED` as D-037 doctrine | D037_EVIDENCE.md §4 |
| Run 001 requires `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false` | `OBSERVED` as D-037 doctrine | D037_EVIDENCE.md §4.1 |
| Web+API implementation repo is `scrimshawlife-ctrl/suas`, described as a TypeScript Cloudflare Worker | `OBSERVED` as README statement | README.md surfaces table |
| Production hosting/cloud provider remains an open decision | `OBSERVED` | D-001 open; DEPLOYMENT.md §4 |
| Database hosting remains an open decision | `OBSERVED` | D-005 |
| Durable-job implementation remains an open decision | `OBSERVED` | D-022 |
| Credit provider, expiration, eligible services | `NOT_COMPUTABLE` | D037_FUNDING_READINESS.md §2 |
| Named STAGING URL, account, Worker route, or database for Run 001 | `NOT_COMPUTABLE` | absent from this repository |
| Evidence destination URI | `NOT_COMPUTABLE` | FR-T-INFRA-002 still open |
| Whether current `suas` STAGING is deployed and healthy | `NOT_COMPUTABLE` | runtime not inspected |

## Hosting options that stay legal under current authority

None of these is a vendor selection. They are the classes already allowed.

1. **TEST / CI inside `suas`**  
   Satisfies `SUAS_ENV=TEST`, synthetic fixtures, no real effects. Sufficient for an engineering rehearsal of the product loop. Insufficient as a declared STAGING evidence host until someone records the CI job identity, fixture dataset hash, and evidence destination.

2. **Existing `suas` STAGING class, current stack, fake/manual/sink adapters**  
   Allowed by ENVIRONMENT.md if a STAGING deployment already exists. Hosting vendor is whatever that deployment already uses. D-037 must not introduce a second vendor to make the run look fundable.

3. **LOCAL operator reconstruction**  
   Permitted for `ENGINEERING` / `DEMO` purpose classes. Not permitted as Run 001 `CONTROLLED_EXPERIMENT` (LOCAL is outside the Run 001 allow-list).

4. **New cloud account purchased or credited for D-037**  
   Not authorized. D-001 is open. Credits are advisory. Option 2 (limited implementation authority) was not granted.

## Credit envelope interaction

D037_EVIDENCE.md §6 planning ceilings remain advisory. This inventory does not allocate them.

If a later qualifier authorizes Run 001 on an already-running STAGING instance whose marginal cost is zero or free-tier, the cost record may be `$0` / free-tier. That still requires FR-T-EXP-003 after a run exists.

Spending any portion of the asserted `$300` to stand up a new host is outside this task.

## Can STAGING host Run 001 without a new vendor?

| Clause | Answer |
|---|---|
| Spec class allows it | `YES` — `STAGING` + fake/manual/sink + no real veteran data matches §4.1 |
| Spec names an existing host that is ready | `NO` |
| Spec authorizes creating a host | `NO` |
| Runtime proof that `suas` STAGING exists and can persist audit/domain events for a sealed artifact | `NOT_COMPUTABLE` |
| New vendor required by this packet | `NO` — and forbidden until D-001 closes or a later qualifier names one |
| Evidence destination | missing (`FR-T-INFRA-002`) |

Net: **class-compatible, instance-unproven, destination-missing.** That is not FR-2 `PASS`.

## Blockers that keep FR-2 `NOT_READY`

1. No evidence-store URI or access policy (`FR-T-INFRA-002`).
2. Runtime field emission `NOT_COMPUTABLE` ([D037_OBS_INVENTORY.md](D037_OBS_INVENTORY.md)).
3. Experiment configuration not frozen (`FR-T-EXP-001`).
4. Limited implementation authority not granted.
5. D-001 still open, so this inventory cannot treat the README Cloudflare Worker statement as the Run 001 host.

## Result

| Claim | State |
|---|---|
| FR-T-INFRA-001 written inventory | `DONE` 2026-09-17 |
| Vendor selected | `NO` |
| Credits spent | `NO` |
| STAGING instance declared ready | `NO` |
| FR-2 | remains `NOT_READY` |
