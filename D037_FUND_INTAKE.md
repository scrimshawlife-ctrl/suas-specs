# D037_FUND_INTAKE.md — Owner artifact slots

**Decision:** D-037  
**Tasks:** `FR-T-FUND-001`, `FR-T-FUND-002`  
**Date:** `2026-09-17`  
**Authority:** documentation only  
**Does not move:** FR-2, FR-3, FR-4, FR-5  
**Does not claim:** `GRANT_READY`, `GRANT_ELIGIBLE`, `FUNDING_SECURED`

This file is the drop point for owner-supplied organizational artifacts. Empty slots stay `NOT_COMPUTABLE`. An agent must not invent UEI, CAGE, SAM legal name, credit provider, expiration, or eligibility.

Place files under `evidence/organizational/` in a later commit that cites this table. Do not commit secrets, bank account numbers, tax IDs beyond what SAM already publishes, or live API keys.

## FR-T-FUND-001 SAM / federal registration

| Slot | Current label | Artifact path | Notes |
|---|---|---|---|
| SAM registration / approval exists | `OPERATOR_ASSERTED` 2026-09-17 | _none_ | owner statement only |
| UEI | `NOT_COMPUTABLE` | _none_ | |
| CAGE | `NOT_COMPUTABLE` | _none_ | optional |
| SAM legal entity name | `NOT_COMPUTABLE` | _none_ | do not infer from GitHub or D-031 |
| Entity type / applicant identity | `NOT_COMPUTABLE` | _none_ | |
| SAM.gov screenshot or official PDF | `NOT_COMPUTABLE` | _none_ | |
| Registration expiration | `NOT_COMPUTABLE` | _none_ | |

Promotion rule: a slot becomes `OBSERVED` only when a file exists at a named path in this repository and the row is updated in the same commit. Presence of this intake file is not evidence.

## FR-T-FUND-002 credit provider

| Slot | Current label | Artifact path | Notes |
|---|---|---|---|
| `$300` credits available | `OPERATOR_ASSERTED` 2026-09-17 | _none_ | |
| Provider name | `NOT_COMPUTABLE` | _none_ | not D-001 |
| Eligible services | `NOT_COMPUTABLE` | _none_ | |
| Expiration | `NOT_COMPUTABLE` | _none_ | |
| Remaining balance | `NOT_COMPUTABLE` | _none_ | |
| Terms / restrictions PDF or URL | `NOT_COMPUTABLE` | _none_ | |

Credits remain unspent. This intake does not allocate the advisory envelope in D037_EVIDENCE.md §6.

## FR-T-FUND-003 opportunities

No opportunity is registered. WF-FR-003 requires a source URL before any status other than `NOT_COMPUTABLE`.

## Owner action

Attach the documents. Name the paths in this table. Leave every unfilled slot as written.
