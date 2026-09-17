# Corrections to the native-client plan (2026-09-17)

Read this next to [D033_NATIVE_CLIENT_PLAN.md](D033_NATIVE_CLIENT_PLAN.md) and [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md). Those files stay as written for history. These lines replace the stale ones.

## Case open

The plan said `src/http/routes/cases.ts` had no `POST /api/v0/cases`. That was true of commit `49a01308`. It is not true on current `suas` main.

`POST /api/v0/cases` is registered. It calls `openCase`. One non-closed Case per Veteran. Tests: `tests/integration/http-cases.test.ts`. No session → `401`.

Phones use that JSON command. They do not post `/app/qrf/deploy`.

The integration-file row that called this an open gap is closed for the Worker. It remains open for iOS (still posting HTML deploy) and Android (no API client yet).

## Sign-in, chat, numbers

Current short rules: [D033_SIGN_IN_PARITY.md](D033_SIGN_IN_PARITY.md), [D033_CHAT_PARITY.md](D033_CHAT_PARITY.md), [D033_METRICS_PARITY.md](D033_METRICS_PARITY.md), [D033_CASE_OPEN.md](D033_CASE_OPEN.md).
