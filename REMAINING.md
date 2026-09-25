# What to do next

Read with [ROADMAP.md](ROADMAP.md) and [GAP_ANALYSIS.md](GAP_ANALYSIS.md). Current pin is `0.6.0`.

## Now (SPEC-017)

1. Keep phones and web on `/api/v0` only.
2. ~~Worker: stop requiring a person-chosen tenant on JSON sign-in.~~ **Done on `suas` (`5d7d58b`).** `tenant_id` is optional; enrolled email resolves the tenant. Clients may still send a build-pinned synthetic tenant as a filter. The person must not pick an organization.
3. Confirm or correct the fail-closed Wave C defaults if the owner wants a different rule.
4. Record SPEC-017 completion in [STATUS.md](STATUS.md) only after the owner accepts the evidence.
5. Living-doc hygiene: keep `suas/SPEC017_NEXT.md`, Android README, and iOS README aligned with HEAD (Android `/api/v0` and iOS staging case-open are already shipped).
6. Android leftover from [GAP_ANALYSIS.md](GAP_ANALYSIS.md): keep dummy `MainActivity` truthful for tests (peer-support launcher card shipped).

## Not now

- Production host, real Veteran data, app-store listing.
- Spending the $300 cloud credits without a named evidence run.
- Inventing chat, duty matching, or dashboard math.
- Inventing SMS, food vendors, payment, or restore-time numbers.

## Then (SPEC-018)

Only after the owner closes the launch decisions and attaches test evidence.

## After launch (SPEC-019)

Measured changes from a real pilot. Funding readiness stays on the D-037 overlay.
