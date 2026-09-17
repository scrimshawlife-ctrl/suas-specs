# D037_INFRA_INVENTORY.md — FR-T-INFRA-001 staging host inventory

**Decision:** D-037  
**Task:** `FR-T-INFRA-001`  
**Parent:** FR-R-002, FR-R-003  
**Date:** `2026-09-17`  
**Scope:** public contracts in `suas-specs` after PR #26  
**Runtime repositories inspected:** none  
**Runtime authority:** none  

Question: can existing `suas` STAGING host `SUAS-EVIDENCE-RUN-001` without selecting a new vendor?

This inventory does not close D-001, spend credits, declare a host, or authorize an experiment.

## What is specified

| Fact | Label | Source |
|---|---|---|
| Logical environment class `STAGING` exists | `OBSERVED` as doctrine | ENVIRONMENT.md §2 |
| `STAGING` forbids real veteran data and real external effects except allow-listed sandbox | `OBSERVED` as doctrine | ENVIRONMENT.md §2, DEPLOYMENT.md §1 |
| Run 001 permitted env is `TEST` or `STAGING` | `OBSERVED` as D-037 doctrine | D037_EVIDENCE.md §4 |
| Run 001 requires `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false` | `OBSERVED` as D-037 doctrine | D037_EVIDENCE.md §4.1 |
| Web+API repo described as a TypeScript Cloudflare Worker | `OBSERVED` as README statement | README.md |
| Production hosting remains open | `OBSERVED` | D-001; DEPLOYMENT.md §4 |
| Database hosting remains open | `OBSERVED` | D-005 |
| Durable-job implementation remains open | `OBSERVED` | D-022 |
| Credit provider, expiration, eligible services | `NOT_COMPUTABLE` | D037_FUNDING_READINESS.md §2 |
| Named STAGING URL, account, Worker route, or database | `NOT_COMPUTABLE` | absent |
| Evidence destination URI | `NOT_COMPUTABLE` | FR-T-INFRA-002 |
| Whether current `suas` STAGING is deployed and healthy | `NOT_COMPUTABLE` | runtime not inspected |

## Hosting options that stay legal

1. TEST / CI inside `suas` for an engineering rehearsal of the product loop. Not a declared STAGING evidence host until job identity, dataset hash, and destination are recorded.
2. Existing `suas` STAGING class with fake/manual/sink adapters if that deployment already exists. No second vendor.
3. LOCAL operator reconstruction for ENGINEERING/DEMO only. Not Run 001.
4. New credited or purchased cloud account. Not authorized.

Net: class-compatible, instance-unproven, destination-missing.

## Result

| Claim | State |
|---|---|
| FR-T-INFRA-001 written inventory | `DONE` 2026-09-17 |
| Vendor selected | `NO` |
| Credits spent | `NO` |
| STAGING instance declared ready | `NO` |
| FR-2 | remains `NOT_READY` |
