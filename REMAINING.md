# What to do next

Read with [ROADMAP.md](ROADMAP.md) and [GAP_ANALYSIS.md](GAP_ANALYSIS.md). Current pin is `0.6.0`.

## Now (SPEC-017)

1. Keep phones and web on `/api/v0` only.
2. ~~Worker: stop requiring a person-chosen tenant on JSON sign-in.~~ **Done on `suas` (`5d7d58b`).** `tenant_id` is optional; enrolled email resolves the tenant. Clients may still send a build-pinned synthetic tenant as a filter. The person must not pick an organization.
3. ~~Confirm or correct Wave C fail-closed defaults.~~ **Settled `ACCEPT_AS_SPECIFIED` on `2026-09-25`** — [WAVE_C_OWNER_CONFIRMATION_PACKET.md](WAVE_C_OWNER_CONFIRMATION_PACKET.md).
4. ~~Owner mark SPEC-017 evidence for STATUS claim.~~ **Marked `NO` on `2026-09-25`** — [SPEC017_EVIDENCE_PACK.md](SPEC017_EVIDENCE_PACK.md). Do not edit [STATUS.md](STATUS.md) completion language.
5. **Next:** refresh `suas` [docs/SPEC017_COMPLETION_AUDIT.md](https://github.com/scrimshawlife-ctrl/suas/blob/main/docs/SPEC017_COMPLETION_AUDIT.md) against pin `0.6.0` (it is still headed at `0.2.0`), then re-open the evidence accept block.
6. Living-doc hygiene: keep `suas/SPEC017_NEXT.md`, Android README, and iOS README aligned with HEAD.
7. Android leftover: keep dummy `MainActivity` truthful for tests (test-harness banner shipped; peer-support launcher shipped).

## Not now

- Production host, real Veteran data, app-store listing.
- Spending the $300 cloud credits without a named evidence run.
- Inventing chat, duty matching, or dashboard math.
- Inventing SMS, food vendors, payment, or restore-time numbers.

## Then (SPEC-018)

Only after the owner closes the launch decisions and attaches test evidence.

## After launch (SPEC-019)

Measured changes from a real pilot. Funding readiness stays on the D-037 overlay.
