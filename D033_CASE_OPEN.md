# Opening a Support Case from a phone

**Stack:** `0.6.0`  
**Parents:** [API.md](API.md) §8, [CASES.md](CASES.md) §3.1, [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) §9

[D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) §2.1 said `src/http/routes/cases.ts` had no `POST /api/v0/cases`. That was true of an older commit. It is not true on current `suas` main.

## What is live

`POST /api/v0/cases` opens or returns the Veteran’s one non-closed Support Case (`openCase`, CASES.md §3.1). Tests live in `tests/integration/http-cases.test.ts`. An unauthenticated call returns `401`.

Send `Idempotency-Key`. A replay returns the same `case_id`. A new Case is `201`. A reuse is `200` with `replayed: true`.

## What phones must do

| Do | Do not |
|---|---|
| `POST /api/v0/cases` with Bearer + `Idempotency-Key` | `POST /app/qrf/deploy` |
| Then `POST /api/v0/cases/{id}/service-requests` for food, ride, shelter, or peer support | Treat HTML deploy as the phone command |
| Keep the same idempotency key when the network drops | Mint a new key because a response was lost |

Web may keep the HTML deploy form. That form is not the phone contract.
