# SECURITY.md — Security controls and threats (SUAS v0.1)

**Related:** [AUTH.md](AUTH.md), [PRIVACY.md](PRIVACY.md), [COMPLIANCE.md](COMPLIANCE.md), [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md), [ADMIN.md](ADMIN.md), [EVENT_MODEL.md](EVENT_MODEL.md), [DEPLOYMENT.md](DEPLOYMENT.md), [PRODUCT.md](PRODUCT.md), [ONBOARDING.md](ONBOARDING.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [RESILIENCE.md](RESILIENCE.md)

---

## 1. Purpose

Treat veteran support data as **highly sensitive regardless of HIPAA**. Specify controls and threat categories. Do **not** claim HIPAA compliance.

```text
HIPAA_APPLICABILITY = DECISION_PENDING
```

D-006 remains open. Implementation must not display "HIPAA compliant" or similar.

The regime register is [COMPLIANCE.md](COMPLIANCE.md). That file does not make SUAS HIPAA-compliant or anything-compliant. Counsel facts for D-006 are in [D-006_FACT_SHEET.md](D-006_FACT_SHEET.md). That packet does not close D-006 and does not change `HIPAA_APPLICABILITY`.

---

## 2. Required controls

| Control | Rule |
|---|---|
| TLS | All network traffic in transit, including provider/webhook traffic |
| Encryption at rest | Database and backups encrypted. Key management `DECISION_PENDING` |
| RBAC | Roles in [AUTH.md](AUTH.md) / [ADMIN.md](ADMIN.md) |
| Tenant isolation | `tenant_id` on tenant-owned rows; no cross-tenant query without SUAS-admin audited path |
| Row-level authz | Authentication is not authorization; every read/write checks role + tenant + row + consent/system basis |
| MFA | Required for Responder, Org-admin, SUAS-admin |
| Secrets | No secrets in git, logs, or client bundles. Secret store `DECISION_PENDING` |
| Provider credentials | Server-side only; scoped per environment/provider where supported; rotation/revocation path required before production |
| Rate limits | Auth challenges, list endpoints, notification send, provider-facing request initiation where applicable |
| Sessions | Revocable; invalidate on revoke ([AUTH.md](AUTH.md)) |
| Audit | Immutable Audit Events ([EVENT_MODEL.md](EVENT_MODEL.md)) |
| Webhook authentication | Reject unauthenticated/invalid-signature provider and notification webhooks |
| Replay protection | Provider/notification webhook handling must be idempotent or detect replay/duplicate delivery |
| Outbound provider calls | Use configured adapter endpoints; do not accept arbitrary user-controlled destination URLs for server-side provider requests |
| Backups | Per environment; restore testing required ([DEPLOYMENT.md](DEPLOYMENT.md)) |
| Restore testing | Periodic; recorded |
| Retention | D-007 `DECISION_PENDING` |
| Deletion | Soft-delete plus process; events not casually purged |
| Least privilege | Host, DB, application, worker, and provider credential roles |
| No prod data in dev | Absolute |
| No sensitive data in logs | Prefer opaque identifiers; no request/response bodies containing veteran data |

---

## 3. Medi-Cal / billing boundary

Billing adapter is `FUTURE`. Do not store payment card data. Do not assert Medi-Cal billability. See [PRODUCT.md](PRODUCT.md) and [SETTLEMENT.md](SETTLEMENT.md).

```text
Fulfillment -> Funding Eligibility -> Funding Source -> Optional Billing Adapter
STATUS = FUTURE
```

---

## 4. Provider integration security boundary

Provider adapters are untrusted-boundary integrations even when the provider is an approved partner.

Rules:

1. Adapter inputs come from SUAS-owned validated domain/application objects, not raw client-provided provider payloads.
2. Adapter outputs and webhooks are validated against normalized schemas before changing SUAS state.
3. Provider-specific statuses cannot directly write canonical Service Request/Fulfillment status without the documented translation/command path.
4. Every external mutation uses SUAS idempotency/Fulfillment Attempt identity. Duplicate retries/webhooks must not duplicate fulfillment.
5. Unknown/ambiguous provider outcomes must reconcile before risky mutation retry. See [RESILIENCE.md](RESILIENCE.md).
6. Provider webhook authentication failure is rejected and audited without changing domain state.
7. Provider credentials are not exposed to browser/mobile clients.
8. Provider request/response bodies with veteran data are excluded from ordinary logs and traces.
9. Adapter configuration must prevent arbitrary server-side fetch destinations. If a provider API requires callbacks/URLs, allowed destinations/patterns must be configuration-owned rather than veteran/user-controlled.
10. Compromise or outage of one provider must not grant access to another tenant, provider configuration, or unrelated veteran data.

D-017 Uber Guest Rides adapter security requirements:

- OAuth client secret handling is exact: keep the client secret only in server-side secret storage/configuration, inject it only into the adapter runtime, redact it from logs/traces/errors, exclude it from client bundles and admin read APIs, rotate/revoke on suspected exposure, and fail closed when absent or malformed.
- Request the official token scope `guests.trips`; broader scopes are disallowed unless a later released decision names them.
- If Uber webhook ingress is implemented, verify the provider HMAC signature using the adapter-local webhook secret over the exact raw request body before parsing or enqueueing work. Reject missing/invalid signatures and replay/duplicate deliveries without domain transition.
- Treat provider access tokens, refresh tokens if any, webhook secrets, request IDs, receipt URLs/data, rider contact data, pickup/dropoff data, and trip status payloads as adapter-confined sensitive data.
- Provider-native create idempotency was not confirmed and must not be invented. SUAS FulfillmentAttempt idempotency and reconciliation records are the security boundary against duplicate ride creation.

D-018 Amadeus shelter adapter security requirements:

- Keep Amadeus credentials and provider tokens in server-side secret storage, scoped by environment, redacted from logs/errors/admin reads, and unavailable to clients.
- Treat property/rate/offer identifiers, search criteria, guest contact data, stay dates, accessibility notes, reservation references, and provider responses as adapter-confined sensitive data.
- SUAS MUST NOT collect, transmit, proxy, tokenize, or store raw card numbers, security codes, magnetic-stripe data, or provider payment-form content. A payment-dependent reservation fails closed as `BLOCKED_BY_PAYMENT_ARCHITECTURE`.
- A `card_free_enterprise` reservation path is permitted only when the owner-approved deployment record documents a contract requiring no SUAS raw-card handling; implementation configuration cannot manufacture that authority.
- Every hold/reserve/cancel mutation uses a stable FulfillmentAttempt idempotency identity. Timeout or ambiguous acceptance records `PROVIDER_UNKNOWN` and reconciles before duplicate-risk retry.
- Provider health degradation, authentication failure, rate limiting, or unsupported capability must preserve the Service Request and route truthfully to `ManualShelterAdapter` or another authorized adapter when policy permits.

---

## 5. Threat categories

Implementation and review must address each:

| Category | Example | Mitigation (specified) |
|---|---|---|
| Broken access control | Responder reads unassigned veteran check-ins | Row-level authz + consent/basis |
| Cross-tenant leakage | Org A query returns Org B cases | tenant_id + tests |
| Responder overreach | Enumerating Trusted Circle addresses | Deny by default; incident-only path |
| Trusted-contact overexposure | Membership used as visibility | Grants required |
| Compromised responder account | Stolen session | MFA, session revoke, audit, least privilege |
| Notification leakage | Message to wrong address or after revoke | Re-check grant; record consent_basis |
| Stale consent | Cached allow after revoke | Evaluate at use time |
| Insecure audit logs | Mutable logs, admin wipe | Immutable store; no app DELETE |
| Resource poisoning | Fake resource that misleads veterans | Org-owned writes, verification, freshness |
| Malicious notes/content | Script or phishing in CaseNote | Treat body as untrusted; encode at render |
| Accidental production-data exposure | Prod dump in TEST | Separate DBs; no prod-in-dev |
| Provider over-disclosure | Whole Case/Check-In sent for a ride booking | Capability-specific minimum projection + consent audit |
| Spoofed provider webhook | Attacker marks request fulfilled | Webhook auth + normalized validation + idempotency |
| Provider replay/duplicate | Same completion callback delivered repeatedly | Dedup/idempotent processing |
| Provider credential theft | Stolen API key used outside SUAS | Server-side secret storage, least privilege, rotation/revoke, monitoring |
| Provider status injection | Vendor text/status writes canonical state | Adapter normalization + command/state-machine enforcement |
| SSRF-style provider abuse | User controls server-side provider destination URL | Configuration-owned endpoints/allowlists; reject arbitrary destinations |
| Duplicate external mutation | Retry books two rides/rooms | Fulfillment Attempt idempotency + reconcile-before-retry |
| Overbroad Uber OAuth scope | Adapter obtains privileges outside Guest Rides | Allow only `guests.trips`; fail closed on unexpected configured scopes |
| Uber OAuth client-secret leakage | Secret appears in client bundle, logs, admin API, or repo | Server-side secret storage, redaction, no client exposure, rotation/revoke |
| Forged Uber webhook | Attacker posts fake trip status | HMAC over raw body before parse/enqueue; reject/audit invalid signature |
| Receipt over-disclosure | Receipt details leak veteran route/contact data | Adapter-local receipt retrieval/projection; no ordinary logs; minimum necessary display |

---

## 6. Non-goals

- Claiming HIPAA compliance
- Claiming SOC2/ISO without evidence (`NOT_COMPUTABLE`)
- Inventing legal notification deadlines ([INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md))
- Treating provider approval or contract signature as proof that its integration is secure

---

## 7. Testability

Critical suites include cross-tenant isolation, responder authorization, audit-event immutability, notification consent, trusted-circle visibility, and provider-boundary security.

Provider-boundary tests must prove:

- invalid/unsigned webhook -> reject, no domain transition;
- duplicate webhook -> one effective transition;
- duplicate provider mutation/retry -> one effective external intent;
- arbitrary user-controlled provider endpoint -> reject/not routable;
- provider adapter cannot receive fields outside its accepted projection fixture;
- provider response cannot bypass canonical state machine;
- provider credentials never appear in client bundles/log fixtures.

Security tests are mandatory even though `SECURITY` is not a separate readiness-gate label in [STATUS.md](STATUS.md); they support AUTH, CONSENT, PRIVACY, EXTERNAL_FULFILLMENT, SCALE, RESILIENCE, and OPERATIONS.
- Uber machine authentication uses OAuth 2.0 `client_credentials` with a server-side client secret. The client secret and resulting bearer token are secret material and must never enter browser bundles, client-visible configuration, logs, domain events, or generic resource rows.
