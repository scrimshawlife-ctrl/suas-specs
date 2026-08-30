# REPOS.md — Product repository inventory

**Audience:** coding agents and implementers who cloned this repo
**Kind:** inventory. Not a release artifact. Not a decision. Closes no D-0xx.
**Does not** bump the stack, reopen D-033, define complete, or authorize production.

Read this first. [SUAS-specs](https://github.com/scrimshawlife-ctrl/SUAS-specs) is canonical. Three implementation repositories stay in scope for every change to the product API, Veteran journey, auth, or environment class.

Epistemic labels in this file: `OBSERVED` is owner-stated inventory or a fact already recorded in released specs. `INFERRED` follows from those facts. This file invents neither a stack version nor a HIPAA, production, or VA-launch claim.

## Product surfaces (`OBSERVED`)

| Surface | Repository | Role |
|---|---|---|
| Specs | https://github.com/scrimshawlife-ctrl/SUAS-specs | Canonical released contract |
| Web + API | https://github.com/scrimshawlife-ctrl/suas | TypeScript Cloudflare Worker; serves `/api/v0` and `/app` |
| iOS | https://github.com/scrimshawlife-ctrl/suas-ios | Private Swift client. Fork of `louisroehrs/suas-ios`. Consumes `/api/v0`. |
| Android | https://github.com/scrimshawlife-ctrl/suas-android | Public Kotlin client. Fork of `RuntimeSquad/Suas`. Consumes `/api/v0`. |

There is no separate Flutter, React Native, or Kotlin Multiplatform harness.

Machine-readable API inventory for the Worker lives in that repo at `docs/openapi/v0.json`. Native clients pin that file. They do not hold a provider credential.

## How the repos relate

| Fact | Label |
|---|---|
| Specs are canonical. Implementation conforms. Semantic gaps return here. | `OBSERVED` ([AGENTS.md](AGENTS.md) rule 1, rule 3) |
| Native apps are ordinary `/api/v0` clients of the identified opt-in platform. They are not a second product. | `OBSERVED` ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §2, §4) |
| A change to the product API, Veteran journey, auth, or environment class must be considered against all three clients: `suas`, `suas-ios`, and `suas-android`. | standing rule in [AGENTS.md](AGENTS.md) |
| Shared testing host: https://suasqrf.com | `OBSERVED` staging. Not production. |
| Visual/interaction reference for the web Veteran surface: `https://suasqrf.org/app/` | `OBSERVED` in [README.md](README.md). Do not treat that host as this staging URL. |

`INFERRED`: work that only updates `suas` can still break iOS or Android if it changes `/api/v0`, auth, the Veteran journey, or environment class. Consider the other two clients before merging.

This file does not name a stack version. Use [VERSIONING.md](VERSIONING.md) and [STATUS.md](STATUS.md). Do not invent a pin from this inventory.

## Blocked

Do not enable these from configuration, a client default, or this inventory:

| Item | Status |
|---|---|
| Production operation, real Veteran data, live pilot | Blocked. SPEC-018 is the go/no-go. All readiness gates remain `NOT_READY`. |
| Application-store distribution | Blocked. SPEC-018. [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §2, §8, §12. |
| D-006 legal / HIPAA classification | `DECISION_PENDING`. Do not claim HIPAA applies. Do not claim HIPAA does not apply. |
| D-034 on-device data protection | `DECISION_PENDING`. Persist no Veteran domain data locally. |
| VA launch / production VA credentials / real-world VA operation | Blocked. D-035 does not authorize production VA. D-016 self-attestation remains available. |

Device push remains `FUTURE`. Shelter reservation remains payment-architecture-blocked absent a documented card-free enterprise contract.

## Out of this file

- Secrets, `.env` values, provider credentials, real contact details, or production payloads
- A definition of complete
- A new D-id, SPEC-0xx stage, or stack bump
- A reopen of D-033 ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) remains the released client contract)
