# D037_FUNDING_READINESS.md — Canonical funding-readiness surface

**Decision:** D-037  
**Stable identifier:** `SUAS-FUNDING-READINESS-001`  
**Status:** `proposed` / `DECISION_PENDING`  
**Epistemic state:** specification packet for owner review; not released for implementation  
**Does not close:** D-001, D-006, D-010, D-013, D-021–D-025, D-031, SPEC-018  
**Does not consume:** SPEC-019  
**Production authority:** none  
**Related:** [D037_INDEX.md](D037_INDEX.md), [D037_EVIDENCE.md](D037_EVIDENCE.md), [D037_OPPORTUNITY_MODEL.md](D037_OPPORTUNITY_MODEL.md), [D037_WORKFLOWS.md](D037_WORKFLOWS.md)

## Workflows

Canonical workflows for this surface live in [D037_WORKFLOWS.md](D037_WORKFLOWS.md):

- `WF-FR-001` Controlled Evidence Run
- `WF-FR-002` Evidence Evaluation
- `WF-FR-003` Funding Opportunity Assessment

This file is doctrine. Those workflows are the behavioral chain.

## 1. Purpose

Explain how ordinary SUAS engineering and research work can yield reusable evidence for later funding applications without letting funding incentives rewrite product or research integrity.

Governing principle:

Build the system for its released mission. Structure evidence so successful engineering and research work can also support a later application.

SUAS remains a consent-governed veteran support coordination platform. Funding readiness is an overlay on evidence doctrine. It is not a product capability, not a Veteran journey, and not a grant-management subsystem.

## 2. Organizational capability

Record only what this packet is allowed to record.

| Fact | Label | Notes |
|---|---|---|
| SUAS / its operating entity is positioned to pursue applicable U.S. federal opportunities through SAM registration | `OPERATOR_ASSERTED` | operator statement dated 2026-09-17; no SAM screenshot, UEI, CAGE, or SAM.gov artifact is in this repository |
| Eligibility remains opportunity-specific | `OBSERVED` as doctrine | no opportunity assessment in this repo may conclude universal eligibility |
| `$300` in cloud credits is available for SUAS-related work | `OPERATOR_ASSERTED` | provider, eligible services, expiration, and remaining balance are `NOT_COMPUTABLE` |
| UEI | `NOT_COMPUTABLE` | absent |
| SAM legal entity name / entity type | `NOT_COMPUTABLE` | absent; do not infer from GitHub profile or D-031 |
| Credit provider | `NOT_COMPUTABLE` | D-001 production hosting remains open and is not the answer |
| Credit expiration / restrictions | `NOT_COMPUTABLE` | absent |
| Named agency interest | `NOT_COMPUTABLE` | absent |

Missing evidence stays missing.

`OPERATOR_ASSERTED` is weaker than `OBSERVED`. An owner may later attach artifacts that promote a row to `OBSERVED`. This packet does not invent those artifacts.

## 3. Relationship to existing decisions

| Existing ID | Relationship |
|---|---|
| D-010 Service funding/billing sources | **Distinct.** D-010 is product billing (Medi-Cal and similar). D-037 is organizational application readiness. Closing or exercising D-037 does not close D-010. |
| D-001 Production hosting/cloud | Unchanged. Credit use does not select a production host. |
| D-006 / D-013 legal and counsel | Unchanged. A funding application is not a HIPAA claim. |
| D-021–D-025 capacity/SLO/RTO/reporting | Unchanged. Evidence Run metrics are not production SLO claims. |
| D-035 sandbox evidence authority | Pattern reuse only. D-037 does not widen VA scope. |
| SPEC-018 | Unchanged. Funding-reuse evidence is not pilot/production readiness. |
| SPEC-019 | Reserved for post-launch revision. D-037 does not consume that stage number. |

Funding considerations are advisory constraints unless a later released decision grants them greater authority.

## 4. Funding-readiness principles

1. Product mission precedes funding optimization.
2. Evidence precedes claims.
3. Reproducibility precedes demonstrations.
4. Provenance is mandatory.
5. Negative results remain valid evidence.
6. Operator intervention must remain observable.
7. Research results cannot be silently converted into marketing claims.
8. Funding requirements cannot silently mutate system doctrine.
9. Grant-specific requirements remain overlays until explicitly adopted into released canon.
10. Credits should preferentially fund evidence-producing workloads rather than baseline hosting.
11. Credits should not be consumed merely to exhaust them.
12. Opportunity assessments sit outside the product requirement chain and cannot write requirements.

## 5. Research integrity boundary

Three classes of statement stay distinct.

### Product evidence

Evidence that SUAS functions as designed against a released contract. Sources include TESTING.md suites, evidence-gate packets, and D-035 sandbox evidence. Product evidence does not become a funding performance claim without an explicit evaluation record.

### Experimental evidence

Evidence produced under a defined research protocol (`SUAS-EVIDENCE-RUN-001` and successors). The protocol, configuration freeze, environment class, and purpose class travel with the artifact.

### Funding claims

Statements made in an application or external communication. A funding claim MUST cite one or more sealed evidence artifacts plus an evaluation record. A claim without that lineage is prohibited in SUAS materials.

Prohibited conversions:

- unsupported performance claims;
- cherry-picked trials represented as general performance;
- silently discarded negative results;
- unrecorded experiment configuration changes;
- synthetic evidence presented as field evidence;
- demonstrations presented as validated research results;
- speculative capability presented as implemented capability;
- DEMO purpose class presented as RESEARCH purpose class;
- STAGING presented as PRODUCTION.

## 6. Environment and purpose classification

Reuse [ENVIRONMENT.md](ENVIRONMENT.md) §2. Do not add `DEV`, `CONTROLLED_EXPERIMENT`, `DEMO`, or `FIELD` as `SUAS_ENV` values.

Overlay a **purpose class** on the existing environment class. Both are required on every evidence artifact.

| Purpose class | Permitted `SUAS_ENV` | May be cited as |
|---|---|---|
| `ENGINEERING` | `LOCAL`, `TEST`, `STAGING` | product-evidence of implementation behavior |
| `CONTROLLED_EXPERIMENT` | `TEST`, `STAGING` | experimental evidence under a frozen protocol |
| `DEMO` | `LOCAL`, `STAGING` | demonstration only |
| `FIELD` | `PRODUCTION` only after SPEC-018 | field evidence |

Rules:

1. Evidence preserves originating `SUAS_ENV` and purpose class.
2. `DEMO` cannot be relabeled `CONTROLLED_EXPERIMENT` or `FIELD`.
3. `LOCAL` / `TEST` / `STAGING` cannot be relabeled `FIELD`.
4. Synthetic fixtures cannot be relabeled field results.
5. Purpose class is configuration metadata for evidence, not a new runtime environment and not a feature flag that enables production-unavailable surfaces.

## 7. Security, privacy, governance

Funding readiness does not override [SECURITY.md](SECURITY.md), [PRIVACY.md](PRIVACY.md), [CONSENT.md](CONSENT.md), or [COMPLIANCE.md](COMPLIANCE.md).

Minimum-necessary evidence. Do not expand collection to look fundable.

| Topic | Rule |
|---|---|
| Operator identifiers | Prefer a durable pseudonymous operator reference. Legal names in evidence artifacts require an explicit retention decision (D-007 still open). |
| Veteran data | LOCAL/TEST/STAGING remain forbidden for real veteran data. Evidence Run 001 uses synthetic fixtures only. |
| Secrets | Never copied into evidence artifacts, grant exports, or credit-cost records. |
| Model inputs/outputs | Redact to the fields the protocol names. Provider-raw payloads stay out of domain evidence storage, matching D-035 posture. |
| External provider retention | Record that a provider may retain inference inputs. Treat retention as `NOT_COMPUTABLE` until the named provider's terms are attached. |
| Access control | Evidence artifacts are privileged operator material, not Veteran-visible and not Organization-Admin-visible by default. |
| Artifact integrity | Sealed artifacts are immutable. Corrections create a successor with lineage. |
| Retention / deletion | Follow D-007 once closed. Until then, experimental artifacts use an explicit `retention_class` of `UNRESOLVED` and are not mixed into production stores. |
| Grant reporting exports | Generated from sealed artifacts only. An export is a derived artifact, not a mutation of the source. |
| HIPAA / compliance claims | Unchanged `DECISION_PENDING`. Funding language must not say HIPAA-compliant. |

## 8. Traceability

Product chain (unchanged):

```text
Doctrine → Requirement → Journey → Workflow → State → Contract → Acceptance Criterion → Task → Evidence
```

Funding opportunities sit **outside** this chain and may only reference it. An opportunity assessment that would require a new product behavior returns a gap. It does not write the requirement.

D-037 requirements are labeled `FR-R-*` and live in this packet. They become released requirements only through a later release manifest.

## 9. Requirements

| ID | Requirement | Kind |
|---|---|---|
| FR-R-001 | SAM/federal-funding capability is documented without universal eligibility | doctrine |
| FR-R-002 | `$300` credit has an evidence-oriented planning envelope | advisory |
| FR-R-003 | Evidence Run 001 is fully specified | experiment spec |
| FR-R-004 | Evidence provenance fields are defined and optional where runtime cannot produce them | contract |
| FR-R-005 | Operator intervention is a first-class observable | contract |
| FR-R-006 | Failed, aborted, and partial runs remain representable evidence | contract |
| FR-R-007 | Metrics have deterministic definitions and a REQUIRED/OPTIONAL/FUTURE/NOT_COMPUTABLE class | measurement |
| FR-R-008 | Environment + purpose class prevent synthetic/demo masquerade | doctrine |
| FR-R-009 | Opportunity assessments cannot mutate canonical product requirements | doctrine |
| FR-R-010 | Research evidence and funding claims stay separated | doctrine |
| FR-R-011 | Security/privacy implications of evidence artifacts are addressed | doctrine |
| FR-R-012 | Cost evidence can later support compute-budget estimation | contract |
| FR-R-013 | Every new D-037 requirement traces to a workflow, contract, acceptance test, or explicit non-executable doctrine | traceability |
| FR-R-014 | Existing specifications remain internally consistent | audit |
| FR-R-015 | No speculative grant, provider, eligibility, performance, or research claim is introduced | integrity |

## 10. Acceptance criteria

Funding-readiness *specification* work is complete (`SUAS_FUNDING_READINESS_SPECIFIED`) when all of the following hold. None of these mark a product readiness gate `READY`.

1. FR-R-001 through FR-R-015 are present in this packet.
2. Evidence Run 001 specifies preconditions, happy path, alternate paths, and failure paths.
3. Metric classes and denominators exist for every REQUIRED metric.
4. Opportunity schema forbids eligibility conclusions without a source URL/reference.
5. Drift audit in [D037_DRIFT_AUDIT.md](D037_DRIFT_AUDIT.md) records residual `NOT_COMPUTABLE` items rather than filling them.
6. No runtime repository is modified from this packet.
7. Owner review may accept the packet as specified without treating acceptance as GRANT_READY.

## 11. Readiness gates for this overlay

These gates are **not** the twelve product gates in [TESTING.md](TESTING.md) §11.

| Gate | Meaning | Current state |
|---|---|---|
| `FR-1` Specification Ready | Packet internally consistent and owner-reviewable | `NOT_COMPUTABLE` until owner review; packet author state is `IMPLEMENTED` as text only |
| `FR-2` Experiment Ready | Evidence Run 001 preconditions satisfied | `NOT_READY` |
| `FR-3` Evidence Ready | A controlled run completed and produced valid evidence | `NOT_READY` |
| `FR-4` Evaluation Ready | Independent evaluation against declared metrics | `NOT_READY` |
| `FR-5` Funding Reuse Ready | A funding claim can be constructed entirely from sealed evidence | `NOT_READY` |

Allowed gate values: `PASS`, `FAIL`, `BLOCKED`, `NOT_READY`, `NOT_COMPUTABLE`.

Do not mark a gate `PASS` without evidence. Green CI, merged code, and the existence of this packet cannot promote FR-2 through FR-5.

## 12. Authority after owner review

Owner options, none of which are taken by publishing this packet:

1. `ACCEPT_AS_SPECIFIED` — packet becomes accepted specification; still not a stack bump and still not runtime authority.
2. `ACCEPT_LIMITED_IMPLEMENTATION_AUTHORITY` — later release qualifier, D-035 style, naming exactly which INFRA/OBSERVABILITY tasks may proceed and in which `SUAS_ENV`.
3. `RETURN_FOR_REVISION`.
4. `REJECT`.

Until one of those is recorded in a release decision ledger, coding agents must not change `suas`, `suas-ios`, or `suas-android` because of D-037.
