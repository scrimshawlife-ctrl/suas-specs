# D037_GCP_PLACEMENT.md — Google Cloud placement overlay

**Decision:** D-037  
**Stable identifier:** `SUAS-GCP-PLACEMENT-001`  
**Status:** specified overlay / `ACCEPT_AS_SPECIFIED` parent  
**Date:** `2026-09-17`  
**Does not close:** D-001, D-002, D-003, D-005, D-022, D-023, SPEC-018  
**Production authority:** none  
**Runtime authority:** none  
**Spend authority:** none  

Owner instruction 2026-09-17: specify which parts of SUAS belong on Google Cloud infrastructure.

This file answers that question as an evidence-plane map. It does not select Google Cloud as the production host.

## 1. Governing split

Two planes stay distinct.

| Plane | Role | Decision that owns it |
|---|---|---|
| Product plane | Released modular monolith, clients, production data, production effects | D-001 / D-005 / D-022 and SPEC-018 |
| Evidence plane | Controlled experiments, sealed artifacts, credit-funded measurement | D-037 this file |

Google Cloud is the **advisory evidence plane** for the operator-asserted `$300` credits. It is not the product plane.

`OPERATOR_ASSERTED` 2026-09-17: the credit provider is Google Cloud. Eligible SKUs, expiration, and remaining balance stay `NOT_COMPUTABLE` until files land in [D037_FUND_INTAKE.md](D037_FUND_INTAKE.md).

## 2. Placement classes

| Class | Meaning |
|---|---|
| `GCP_EVIDENCE_SHOULD` | If credits are used at all, this workload belongs in an isolated GCP project |
| `GCP_EVIDENCE_MAY` | Allowed in that project when existing TEST/STAGING cannot produce the artifact |
| `GCP_FORBIDDEN_THIS_PACKET` | D-037 may not place this on GCP |
| `EXISTING_SURFACE` | Stays on the current implementation surface; credits must not migrate it |
| `UNDECIDED` | Owned by an open D-00x; this file cannot assign a vendor |

## 3. Isolated GCP project rule

If an evidence-plane project is later authorized, it is a project whose only job is evidence.

Required properties of that project:

- name and number recorded in a later evidence artifact, not invented here
- no production `SUAS_ENV`
- `SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false`
- no real veteran records addressable
- no production secrets
- no billing account shared with a future production project until D-001 closes
- IAM principals are privileged operators only
- evidence objects use `retention_class=UNRESOLVED` until D-007 closes

Prefer one project. Do not create a second project to exhaust credits.

## 4. Architecture map

Rows follow [ARCHITECTURE.md](ARCHITECTURE.md). Classes apply to where the running dependency lives, not to source code location.

### 4.1 Product plane — do not move for credits

| Component | Class | Notes |
|---|---|---|
| Veteran / Responder / Admin web clients | `EXISTING_SURFACE` | consume `/api/v0`; not GCP apps |
| Native iOS / Android clients | `EXISTING_SURFACE` | D-033; device-side; never GCP |
| Stateless SUAS API tier (modular monolith) | `UNDECIDED` + `GCP_FORBIDDEN_THIS_PACKET` | D-001 open. README names the current web repo as a Cloudflare Worker. This packet must not relocate it. |
| PostgreSQL system of record | `UNDECIDED` + `GCP_FORBIDDEN_THIS_PACKET` | D-005 open. Cloud SQL is not selected. |
| Durable jobs / workers | `UNDECIDED` + `GCP_FORBIDDEN_THIS_PACKET` | D-022 open. Cloud Tasks / Pub/Sub are not selected. |
| Domain + audit event store | `EXISTING_SURFACE` / `UNDECIDED` | stays with the product plane SoR |
| Email | `EXISTING_SURFACE` | D-004 Resend only |
| SMS | `UNDECIDED` | D-003 |
| Auth provider | `UNDECIDED` | D-002 |
| Uber / Amadeus / Manual adapters | `EXISTING_SURFACE` | adapter-local; real effects blocked until SPEC-018 |
| Support Signal compute | `EXISTING_SURFACE` | TEST/CI stay `SUAS_SUPPORT_SIGNAL_MODE=fixture`; no Vertex primary signal |
| Production telemetry / SLO stack | `UNDECIDED` | D-023. Evidence telemetry must not be relabeled production SLO. |

### 4.2 Evidence plane — Google Cloud if credits are used

| Workload | Class | Logical GCP service class | Envelope row |
|---|---|---|---|
| Sealed evidence artifact store | `GCP_EVIDENCE_SHOULD` | object storage (Cloud Storage class) | Storage / evidence datasets `$35` |
| Evidence destination URI for `FR-T-INFRA-002` | `GCP_EVIDENCE_SHOULD` | one bucket + path convention in that project | same |
| Run 001 compute when existing `suas` TEST/STAGING cannot host | `GCP_EVIDENCE_MAY` | stateless container/job class (Cloud Run / Compute class) | Controlled deployment `$80` |
| Run 001 telemetry / audit export copy | `GCP_EVIDENCE_MAY` | logging/monitoring class | Telemetry `$60` |
| IAM / secret-access drills for the evidence project | `GCP_EVIDENCE_SHOULD` | IAM + Secret Manager class inside the evidence project | Security / IAM `$25` |
| Cost records for credited usage | `GCP_EVIDENCE_SHOULD` | billing export or manual `ExperimentCostRecord` | all rows |
| Non-safety-critical model experiments explicitly frozen into a later run | `GCP_EVIDENCE_MAY` | managed inference class (Vertex class) | Model / inference `$70` |
| Acceptance / contingency | reserved | not a service | `$30` |

Cloud Storage as the evidence destination does not make Cloud Storage the product object store.

Cloud Run as a Run 001 host does not make Cloud Run the product API tier.

Vertex is forbidden as a primary Support Signal or any safety-critical decision surface. It is allowed only when a later frozen protocol names a non-safety-critical experiment and FR-R-015 still holds.

## 5. Environment mapping

| `SUAS_ENV` | Purpose class | GCP evidence project |
|---|---|---|
| `LOCAL` | `ENGINEERING` / `DEMO` | not required |
| `TEST` | `ENGINEERING` / `CONTROLLED_EXPERIMENT` | optional export of sealed artifacts into the bucket |
| `STAGING` | `CONTROLLED_EXPERIMENT` / `DEMO` | permitted host for Run 001 compute or destination for artifacts produced elsewhere |
| `PRODUCTION` | `FIELD` after SPEC-018 only | `GCP_FORBIDDEN_THIS_PACKET` |

Run 001 remains `TEST` or `STAGING` + `CONTROLLED_EXPERIMENT`. A GCP project used for Run 001 is labeled `STAGING` or the artifacts are exported into GCP from a `TEST` run. The project does not become a fifth `SUAS_ENV`.

## 6. What must never be placed on the evidence project

- real veteran records
- production session secrets
- Resend / Uber / Amadeus / VA production credentials
- payment data of any kind
- unredacted Check-In answers
- provider-raw inference payloads
- grant-application drafts that are not derived from sealed artifacts
- the product PostgreSQL
- the product API process

## 7. Preference order when hosting Run 001

1. Existing `suas` TEST / CI with artifacts copied to the GCP evidence bucket.
2. Existing `suas` STAGING, same copy path.
3. GCP evidence-project compute only when 1 and 2 cannot produce a reconstructable run.

This order is the INFRA inventory conclusion: class-compatible existing surfaces first, new vendor-shaped compute last. Google Cloud is named here as the credit provider, not as a reason to abandon an already-running TEST surface.

## 8. Requirements added

| ID | Requirement | Kind |
|---|---|---|
| FR-R-016 | Product plane and evidence plane stay separately hosted until D-001 closes | doctrine |
| FR-R-017 | If credits are consumed, they are consumed only on `GCP_EVIDENCE_SHOULD` / `GCP_EVIDENCE_MAY` workloads in an isolated project | advisory |
| FR-R-018 | Google Cloud placement in this file does not close D-001 or D-005 | integrity |

## 9. Tasks

| ID | Task | State |
|---|---|---|
| FR-T-INFRA-003 | Specify GCP vs non-GCP placement for architecture components | `DONE` 2026-09-17 this file |
| FR-T-INFRA-002 | Evidence destination URI | still `OPEN`; when declared, prefer `gs://` in the isolated evidence project |
| FR-T-FUND-002 | Attach GCP credit terms | still `OPEN`; provider name now `OPERATOR_ASSERTED` as Google Cloud |

No runtime task is created. Option 2 remains ungranted.

## 10. Non-claims

- Google Cloud is not the production host.
- Cloud SQL is not the production database.
- Cloudflare is not displaced.
- Credits are not spent by this file.
- FR-2 remains `NOT_READY`.
