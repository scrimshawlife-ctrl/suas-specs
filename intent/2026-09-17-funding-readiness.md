# Intent: Funding readiness and cloud-evidence assimilation

**Status:** `draft`  
**Next stage:** `spec.md` (packet `D037_*`)  
**Author:** operator request via spec-agent  
**Date:** `2026-09-17`

This record is process only. It is not a spec, not a plan, and not a release. It does not define complete.

## Problem

SUAS now has two organizational capabilities that the specification set does not yet record:

1. operator-asserted SAM registration sufficient to *pursue* applicable U.S. federal opportunities;
2. operator-asserted availability of `$300` in cloud credits intended for evidence-producing work.

The current canon already knows how to produce evidence (D-035 sandbox authority, `evidence-gate`, TESTING.md gates, ENVIRONMENT.md classes). It does not know how to keep those capabilities from becoming a grant-management product, a silent doctrine mutation, or an unsupported eligibility claim.

D-010 (`Service funding/billing sources`) is a different question and must stay separate.

## Proposed outcome

A proposed, non-released specification packet (`D-037` / `SUAS-FUNDING-READINESS-001`) that:

- records the two capabilities without inventing UEI, provider, expiration, eligibility, or performance;
- extends the existing evidence vocabulary instead of inventing a second product loop;
- specifies Evidence Run 001, measurement classes, an advisory credit envelope, and an opportunity-assessment schema that cannot write product requirements;
- produces implementation tasks that stay in `SUAS-specs` until an owner release authorizes runtime work.

Terminal condition requested: `SUAS_FUNDING_READINESS_SPECIFIED`. Not `GRANT_READY`, `GRANT_ELIGIBLE`, `EXPERIMENT_VALIDATED`, or `FUNDING_SECURED`.

## Affected users / systems

- Surfaces: `SUAS-specs` only for this intent.
- Runtime (`suas`, `suas-ios`, `suas-android`): out of scope until derived tasks are released.
- Actors: SUAS System Administrator / researcher / project administrator. No Veteran-facing journey change.

## Constraints / non-goals

- Do not redesign SUAS around grants.
- Do not create a grant-management product.
- Do not consume SPEC-019 (reserved for post-launch revision).
- Do not add a fifth `SUAS_ENV` value.
- Do not close D-001, D-006, D-010, D-013, D-021–D-025, or SPEC-018.
- Do not spend credits, run experiments, or claim eligibility from this intent.
- Funding requirements remain overlays until explicitly adopted into released canon.

## Open questions

- Legal entity that holds the SAM registration (`NOT_COMPUTABLE` in this repository; D-031 remains open for island/ride contracting and is not reused as an answer).
- UEI, SAM status date, cage code, entity type (`NOT_COMPUTABLE`).
- Cloud-credit provider, eligible services, expiration, remaining balance (`NOT_COMPUTABLE`).
- Whether any existing `suas` observability surface can emit the Evidence Run 001 field set without a later released contract (`NOT_COMPUTABLE` until a runtime inventory is performed under a released task).

## Verified / assumed claims

| Claim | Label | Basis |
|---|---|---|
| `SUAS-specs` is canonical; runtime may not redefine semantics | `OBSERVED` | [AGENTS.md](../AGENTS.md), [README.md](../README.md) |
| Logical environments are exactly `LOCAL`, `TEST`, `STAGING`, `PRODUCTION` | `OBSERVED` | [ENVIRONMENT.md](../ENVIRONMENT.md) §2 |
| Evidence-gate skill and D-035 evidence authority already exist | `OBSERVED` | [SKILLS.md](../SKILLS.md), [D035_SANDBOX_EVIDENCE_AUTHORITY.md](../D035_SANDBOX_EVIDENCE_AUTHORITY.md) |
| All twelve readiness gates remain `NOT_READY` | `OBSERVED` | [STATUS.md](../STATUS.md) |
| D-010 is service billing/funding, not organizational grants | `OBSERVED` | [DECISIONS.md](../DECISIONS.md) |
| SAM registration exists and is usable to pursue applicable federal opportunities | `OPERATOR_ASSERTED` | this request; no repository artifact |
| `$300` cloud credits exist for SUAS-related work | `OPERATOR_ASSERTED` | this request; no repository artifact |
| Provider, expiration, UEI, remaining credit balance | `NOT_COMPUTABLE` | absent from repository evidence |
| Any named agency interest or eligible opportunity | `NOT_COMPUTABLE` | no opportunity assessment exists |
| Evidence Run 001 has been executed | `NOT_COMPUTABLE` | no run artifact exists |

## Author / date

- **Author:** spec-agent acting on operator request
- **Date:** `2026-09-17`
