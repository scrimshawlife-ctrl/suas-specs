# STATUS.md — SUAS specification status (v0.6.0)

**Specification lifecycle:** `released`
**Phase:** `IMPLEMENTATION_AUTHORIZED`
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`
**Release manifest:** [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md)
**Decision ledger:** [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md) for D-004; inherited ledgers govern other decisions.
**Pilot readiness:** `NOT_READY`
**Production readiness:** `NOT_READY`

## Product surfaces

Named inventory: [REPOS.md](REPOS.md). Specs are canonical. Native clients consume `/api/v0` from `suas`.

| Surface | Repository | Role |
|---|---|---|
| Specs | https://github.com/scrimshawlife-ctrl/SUAS-specs | Canonical released contract |
| Web + API | https://github.com/scrimshawlife-ctrl/suas | TypeScript Cloudflare Worker; `/api/v0`, `/app` |
| iOS | https://github.com/scrimshawlife-ctrl/suas-ios | Native Swift client; consumes `/api/v0` |
| Android | https://github.com/scrimshawlife-ctrl/suas-android | Native Kotlin client; consumes `/api/v0` |

A change to the product API, Veteran journey, auth, or environment class must be considered against all three clients.

## Implementation status (`OBSERVED` through 2026-10-08 PT; not a gate change)

This section records implementation facts so readers do not have to dig through three repositories. It moves no readiness gate and closes no D-id.

| Fact | Detail |
|---|---|
| Synthetic STAGING build | `https://suasqrf.com` runs `suas` `0f7aeae` (suas PR #187), deployed by the manual `worker-deploy` workflow (run `37685578663`). Deploys happen only when an owner runs that workflow by hand. |
| Path-parameter fix | Path-parameter routes such as `GET /api/v0/cases/{id}/service-requests` no longer answer `400` on Workers (suas #187). The `staging-path-param-check` workflow (suas #188) runs after each successful `worker-deploy`; its first run passed with `200` on both checked routes (run `37686583961`). |
| LOCAL demo mode | `npm run dev:demo` in `suas` starts a LOCAL Worker with migrations and a synthetic seed. Sign in as `demo@example.invalid` with code `123456`; `newvet@example.invalid` is enrolled with no case. The fixed code exists only with `SUAS_ENV=LOCAL`, an explicit opt-in, and a local database (suas #189). |
| Native demo modes | Android debug launchers "SUAS Demo (no server)" and "SUAS Local Worker" (suas-android PR #13, merged `ece7bef`). iOS shared schemes `Demo` (`-SUASDemoMode`) and `Local` (`-SUASLocal`), DEBUG only (suas-ios PR #10, merged `89e37ae`). Release builds carry no demo fixture. The iOS `release-bundle` CI job archives an unsigned Release build and fails if it holds `demo-fixtures.json`, a `.gpx` file or demo service markers; Release also excludes `DemoLocation.gpx` (suas-ios PR #13, merged `6b6ad4e`). The Android debug `MainActivity` stays a labeled, non-exported test harness, checked by `MainActivityHarnessTest` (suas-android PR #16, merged `d26a6a6`). |
| Demo fixtures | `suas` owns `contract/demo-fixtures.json` and regenerates it with `npm run demo:fixtures`. The apps hold copies that are not hand-edited. All demo data is synthetic. |
| Application versions | `suas` `0.2.0` (tag `v0.2.0`, merge `a68eb12`, PR #190), `suas-android` `0.1.0` (tag `v0.1.0`, merge `ece7bef`, PR #13) and `suas-ios` `0.1.0` (tag `v0.1.0`, merge `89e37ae`, PR #10), released 2026-10-07 PT. All implement stack `0.6.0`. Scheme: [VERSIONING.md](VERSIONING.md) §8. |
| CI and repository context | Client workflows use Node 24 action majors and `ubuntu-24.04` runners; `suas` pins wrangler `4.148.0` in `worker-deploy` and `recovery-runtime-acceptance` (suas #191 and #192, suas-android #15, suas-ios #12). Each of the four repositories has a `CONTEXT.md` (SUAS-specs #45). |
| CI verification gap | From 2026-10-07 4:05 PM PT, GitHub Actions jobs on the private `suas-ios` repo did not start because of an account billing block. suas-ios #13 and suas-android #16 were merged on local checks only, at the owner's direction. Public repositories can still run hosted jobs. The board card "Confirm release-bundle CI on suas-ios main after billing fix" stays Ready until that job runs on `main`. |
| Mac device checks | 2026-10-08 PT: Simulator Demo, Local, and shipped sign-in, the unsigned Release archive, Android emulator screenshots, and the local re-run of the blocked-CI batch passed. Record: [docs/handoffs/MAC_DEVICE_RESULTS-2026-10-08.md](docs/handoffs/MAC_DEVICE_RESULTS-2026-10-08.md). Draft suas-ios #15 (self-hosted Mac runner) and draft suas-android #18 (emulator journeys) are green and unmerged. This row moves no readiness gate. |
| Work tracking | [SUAS Product Board](https://github.com/users/scrimshawlife-ctrl/projects/6). Owner-blocked items stay `Blocked`. |

## Governance frontier

SPEC-001 through SPEC-015 are accepted. SPEC-016 established the first released cut. v0.3.0 supersedes v0.2.0 and closes D-033 by releasing the native mobile client surface while preserving `/api/v0`, event schema `0.1.0`, canonical state machines, notification channel availability, and all readiness boundaries. v0.2.0 (inherited) closed D-011 by releasing `qv-001`, `sv-001`, incomplete-input behavior, basis requirements, and golden vectors. SPEC-017 implementation conformance against pin `0.6.0` is recorded ([SPEC017_EVIDENCE_PACK.md](SPEC017_EVIDENCE_PACK.md) YES; runtime audit on suas docs/SPEC017_COMPLETION_AUDIT.md). SPEC-018 remains the go/no-go stage for any real pilot or production operation.

## Current release additions

- [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md) grants `IMPLEMENTATION_EVIDENCE_AUTHORIZED` only for D-035 evidence generation in LOCAL fixture and VA SANDBOX. D-035 remains `DECISION_PENDING`; D-016 fallback and production block remain unchanged.

- [MOBILE_SURFACE.md](MOBILE_SURFACE.md) releases the native mobile client contract and closes D-033. The surface is `ENABLED` for implementation and not for production operation.
- D-034 (on-device protection of locally retained veteran data) is opened, not closed.
- Device push remains `FUTURE`; this release adds no push configuration and assigns no decision to that channel.
- [ARCHITECTURE.md](ARCHITECTURE.md) §4 gains a fourth client row; [MVP_REFERENCE.md](MVP_REFERENCE.md) §11 and [TESTING.md](TESTING.md) §7 extend by device class; [ENVIRONMENT.md](ENVIRONMENT.md) §3 gains a client-build subsection.
- Stale inline `draft` headers on [ARCHITECTURE.md](ARCHITECTURE.md) and [MVP_REFERENCE.md](MVP_REFERENCE.md), and the stale `0.1.3` stack header and SPEC-017 status in [ROADMAP.md](ROADMAP.md), are corrected; the manifest governs ([VERSIONING.md](VERSIONING.md) §1).

Inherited from v0.2.0:

- [SIGNAL_SCORING.md](SIGNAL_SCORING.md) releases `qv-001` + `sv-001` and closes D-011.
- Deterministic incomplete-input behavior and golden vectors are implementation-authoritative.
- Domain-file wording for D-015 / D-016 remains inherited from v0.1.6 and matches the v0.1 defaults already `DECIDED` in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md).
- SPEC-003 points at the 0.1.4 effective-signal selection rule in [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §7.1 / [DATA_MODEL.md](DATA_MODEL.md) §4, including the two-override / chain case.
- Leftover high-traffic inline `draft` headers are stamped stale; this manifest governs ([VERSIONING.md](VERSIONING.md) §1).

Inherited from v0.1.5: [SAFETY_COPY.md](SAFETY_COPY.md) and the D-012 copy/destination/truthfulness contract. Inherited from earlier patches: [ENVIRONMENT.md](ENVIRONMENT.md), [HANDOFF.md](HANDOFF.md), adapter-local D-017/D-018, and the 0.1.4 conformance codifications.

## Release meaning

v0.6.0 authorizes implementation of the released Resend EMAIL adapter and browser passwordless session transport for already-enrolled accounts, alongside inherited native-client and scoring contracts. It does not authorize production deployment, real veteran data, live pilot operation, application-store distribution, device push, payment-card handling, real external provider bookings/reservations, compliance claims, production SLO/RTO/RPO claims, or sensitive aggregate reporting.

## Readiness gates

All remain `NOT_READY`:

`AUTH`, `CONSENT`, `CHECK-IN`, `COORDINATION`, `EXTERNAL_FULFILLMENT`, `UI_CONFORMANCE`, `SAFETY`, `PRIVACY`, `SCALE`, `RESILIENCE`, `OPERATIONS`, `REPORTING`.

A gate changes only with reproducible evidence under [TESTING.md](TESTING.md).

## Decision boundary

D-012 is closed by [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md). D-017 is closed by [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md). D-018 is closed by [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md). D-015 and D-016 remain the v0.1 defaults decided in [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md). D-011 is closed by [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md). D-033 is closed by [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md), which opens D-034. D-004 is closed by [RELEASE_DECISIONS-0.6.0.md](RELEASE_DECISIONS-0.6.0.md). D-019–D-025 and D-026–D-032 remain open unless later releases supersede them.

## Next stage

SPEC-017 implementation evidence is recorded for `0.6.0`. Next stage is SPEC-018 (blocked). Implementers still pin `0.6.0`. Native clients authorized for implementation not production/store. Nothing advances a readiness gate.
