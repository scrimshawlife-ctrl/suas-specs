# D037_DRIFT_AUDIT.md — Cross-artifact consistency audit

**Decision:** D-037  
**Date:** `2026-09-17`  
**Settlement:** owner `ACCEPT_AS_SPECIFIED` on [PR #25](https://github.com/scrimshawlife-ctrl/suas-specs/pull/25)

## Method

Inspected repository canon listed in [D037_INDEX.md](D037_INDEX.md). Re-audited after GCP placement, destination convention, and SEC-001.

## Findings repaired in-packet

| Risk | Handling |
|---|---|
| Funding language becoming product doctrine | overlay; assessments cannot write requirements |
| Grant requirements leaking into runtime | no runtime tasks until limited authority |
| New `SUAS_ENV` values | purpose class overlay |
| D-001 silently closed by credits | product plane forbidden; evidence plane only |
| Cloudflare Worker relocated to GCP | `EXISTING_SURFACE` / `GCP_FORBIDDEN_THIS_PACKET` |
| Cloud SQL selected | D-005 stays open |
| Vertex as Support Signal | forbidden in placement + threat model |
| Live `gs://` invented | pattern specified; URI `NOT_COMPUTABLE` |
| Extra collection for fundability | SEC-001 forbids it |

## Residual items requiring operator judgment

| Item | State |
|---|---|
| Promote SAM / `$300` to OBSERVED | needs owner artifacts |
| UEI, legal entity, credit SKUs, expiration, balance | `NOT_COMPUTABLE` |
| Credit provider name | `OPERATOR_ASSERTED` Google Cloud |
| Live GCS bucket / project id | `NOT_COMPUTABLE` |
| Runtime emit of Run 001 fields | `NOT_COMPUTABLE` |
| Existing STAGING instance | `NOT_COMPUTABLE` |
| Named evaluator roster | `NOT_COMPUTABLE` |
| Limited implementation authority | not granted |

## Audit result

Packet remains internally consistent as specification text. FR-2–FR-5 remain `NOT_READY`. Coding agents must not change runtime repositories from this overlay.
