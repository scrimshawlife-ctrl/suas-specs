# CONTEXT.md: SUAS-specs context

Read this before proposing a specification change. Rules for agents and implementers: [AGENTS.md](AGENTS.md). Process: [CONTRIBUTING.md](CONTRIBUTING.md). Inventory: [REPOS.md](REPOS.md).

## What SUAS is

Shut Up and Serve is a consent-governed veteran support coordination platform.

Mission: coordinate the shortest safe and consented path between a veteran's current need and an available human or material support resource.

Canonical loop:

`SIGNAL → NEED → CONSENT → COORDINATION → FULFILLMENT → FOLLOW-UP → SETTLEMENT`

MVP categories:

- `FOOD`
- `TRANSPORTATION`
- `SHELTER`: temporary shelter/accommodation, not permanent housing
- `PEER_SUPPORT`

## What SUAS is not

- EHR
- diagnosis system
- suicide-prediction product
- automated emergency-dispatch system
- clinical efficacy measurement product
- production billing/Medi-Cal system

The full non-goal list is SUAS-specs [PRODUCT.md](https://github.com/scrimshawlife-ctrl/SUAS-specs/blob/main/PRODUCT.md) section 8.

## The four repositories

| Repository | Role |
| --- | --- |
| [`SUAS-specs`](https://github.com/scrimshawlife-ctrl/SUAS-specs) | Canonical released contract. Specs are authority; implementation gaps return here. |
| [`suas`](https://github.com/scrimshawlife-ctrl/suas) | TypeScript Cloudflare Worker: JSON API `/api/v0`, web `/app`, OpenAPI `docs/openapi/v0.json`. Synthetic STAGING `https://suasqrf.com`. |
| [`suas-ios`](https://github.com/scrimshawlife-ctrl/suas-ios) | Native iOS client (Swift). Consumes `/api/v0`. |
| [`suas-android`](https://github.com/scrimshawlife-ctrl/suas-android) | Native Android client (Kotlin Compose). Consumes `/api/v0`. |

A change to the product API, Veteran journey, auth, or environment class must be considered against all three implementation repositories. Work across all four is tracked on the [SUAS Product Board](https://github.com/users/scrimshawlife-ctrl/projects/6).

## This repository's role

`SUAS-specs` is the canonical source. The three implementation repositories conform to it; semantic gaps come back here instead of becoming code defaults. The specification owner is `@scrimshawlife-ctrl`. Contributors and agents may propose changes but cannot self-accept or self-release them ([CONTRIBUTING.md](CONTRIBUTING.md) section 1).

Where the truth lives:

| Question | File |
|---|---|
| Current stack, lifecycle, readiness gates | [STATUS.md](STATUS.md) (stack `0.6.0`, all gates `NOT_READY`) |
| What a release contains | `RELEASE_MANIFEST-x.y.z.md`, current [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md) |
| Decisions and who closed them | [DECISIONS.md](DECISIONS.md) register, plus `RELEASE_DECISIONS-x.y.z.md` ledgers |
| Version rules and identities | [VERSIONING.md](VERSIONING.md) (section 2 stack rules, section 3 identities, section 8 client versions and tags) |
| Stage order | [ROADMAP.md](ROADMAP.md): SPEC-017 done, SPEC-018 current and blocked (`KEEP_BLOCKED`, [SPEC018_OWNER_LAUNCH_PACKET.md](SPEC018_OWNER_LAUNCH_PACKET.md)), SPEC-019 future |
| What is still missing | [GAP_ANALYSIS.md](GAP_ANALYSIS.md), [REMAINING.md](REMAINING.md) |
| History | [CHANGELOG.md](CHANGELOG.md) (dates in PT) |

## API contract

The product API is `/api/v0`, served by `suas`. Native apps consume `/api/v0` only: no second version selector and no `/api/mobile` prefix ([MOBILE_SURFACE.md](MOBILE_SURFACE.md), D-033). The machine-readable inventory is `suas` `docs/openapi/v0.json`. Event schema is `0.1.0`.

## Demo and local mode

This repository has nothing to run. The implementation demo lives in the clients: `suas` `npm run dev:demo` (LOCAL Worker, `demo@example.invalid` / `123456`, `newvet@example.invalid`), the Android debug launchers, and the iOS `Demo` and `Local` schemes. [STATUS.md](STATUS.md) "Implementation status" and [REPOS.md](REPOS.md) record the current facts. The demo fixture is synthetic and is not readiness evidence ([TESTING.md](TESTING.md) section 12).

## Versioning and release

- The stack version is SemVer under [VERSIONING.md](VERSIONING.md) section 2. Releases so far: `0.1.0` to `0.1.6`, `0.2.0` to `0.6.0`.
- Each release has a `RELEASE_MANIFEST-x.y.z.md`, a decision ledger where a decision closes, and entries in VERSIONING.md, STATUS.md, and CHANGELOG.md. Lifecycle changes are owner-controlled.
- Tags `v0.1.0` to `v0.6.0` sit on the commit that added each manifest, each with a GitHub Release linking it.
- Documentation-only changes are recorded in CHANGELOG.md as additive entries marked "Not a version bump".
- Client app versions move independently (VERSIONING.md section 8): `suas` `0.2.0`, `suas-android` `0.1.0`, `suas-ios` `0.1.0`, all implementing `0.6.0`.

## Hard walls

- `/api/v0/dev/*` exists only on a LOCAL Worker (`SUAS_ENV=LOCAL`) and returns 404 on staging `https://suasqrf.com`.
- Do not invent a HIPAA class, percentages, or a production host. There is no production host.
- Blocked until the owner decides: D-034 (on-device protection of Veteran data; clients persist none), D-006 (health-information classification, counsel-owned), SPEC-018 (store distribution and launch, `KEEP_BLOCKED`), production VA verification (D-035 authorizes LOCAL fixture and VA SANDBOX only), and live operations, pilot, or real Veteran data.
- All demo and test data is synthetic: `@example.invalid` emails and 555-0100 to 555-0199 phone numbers.
- iOS keeps Louis's look: service blue `#1C529E`, grouped light home, need cards. Android keeps its SOS-first light home cards.
- Never commit secrets, `.env`, provider credentials, or real contact details.

## Links

- [AGENTS.md](AGENTS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [REPOS.md](REPOS.md), [STATUS.md](STATUS.md), [VERSIONING.md](VERSIONING.md), [DECISIONS.md](DECISIONS.md)
- Implementation: [`suas`](https://github.com/scrimshawlife-ctrl/suas) `CONTEXT.md`, [`suas-ios`](https://github.com/scrimshawlife-ctrl/suas-ios) `CONTEXT.md`, [`suas-android`](https://github.com/scrimshawlife-ctrl/suas-android) `CONTEXT.md`
- Board: [SUAS Product Board](https://github.com/users/scrimshawlife-ctrl/projects/6)
