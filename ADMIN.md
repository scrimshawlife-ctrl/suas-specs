# ADMIN.md — Administration surfaces (SUAS v0.1)

**Related:** [AUTH.md](AUTH.md), [SECURITY.md](SECURITY.md), [PILOT.md](PILOT.md), [RESOURCES.md](RESOURCES.md), [CHECKINS.md](CHECKINS.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [ONBOARDING.md](ONBOARDING.md), [COMPLIANCE.md](COMPLIANCE.md), [PROVIDER_INTEGRATIONS.md](PROVIDER_INTEGRATIONS.md), [OPERATIONS.md](OPERATIONS.md), [ADMIN_SURFACE_DESIGN.md](ADMIN_SURFACE_DESIGN.md)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.1.3.md](RELEASE_MANIFEST-0.1.3.md)

---

## 1. Purpose

Define Organization Administrator and SUAS System Administrator authority. **Org Admin ≠ SUAS Admin.**

Administration configures accepted capabilities and operations; it must not invent new domain semantics, vendor-specific state machines, or bypass consent/security.

The complete proposed web information architecture, page contracts, interaction states, and API-gap ledger are in [ADMIN_SURFACE_DESIGN.md](ADMIN_SURFACE_DESIGN.md). That file remains a draft until owner-released; this file remains authority for roles and boundaries.

---

## 2. SUAS System Administrator

May manage, all with MFA and audit:

| Area | Boundary |
|---|---|
| Users / sessions | status, revoke, recovery/force logout; no silent impersonation |
| Organizations / memberships | create/suspend/archive, cross-org membership administration |
| Cases / Requests | audited break-glass/read/repair paths only as specified; not routine responder ownership |
| Resources / Service Offers | global admin/verification |
| Questionnaire versions | draft/publish/supersede; immutable once published |
| Signal-rule versions | publish only accepted rule artifacts; D-011 cannot be bypassed |
| Consent templates | publish versioned templates |
| Notification templates | publish versioned copy; no safety-critical logic |
| Pilot config | accepted Pilot settings |
| Provider adapter config | enable/disable accepted capability adapters by environment/tenant/coverage after the relevant provider decision is closed |
| Provider health/operations | read normalized adapter health/circuit/reconciliation status without exposing raw secrets |
| Audit / reports | scoped operational read surfaces |
| System config | feature/config flags that do not redefine released contracts |

---

## 3. Provider adapter administration

Provider selection remains D-017–D-020 and deployment configuration, not domain architecture. D-017 selects Uber for adapter-local transportation implementation; D-018 selects Amadeus for adapter-local temporary-shelter search/inventory implementation. Admin surfaces must not expose provider SDK/status, property, rate, offer, or reservation details as canonical state.

Admin surfaces may expose:
- opaque `adapter_id`;
- capability;
- integration mode;
- tenant/org scope;
- enabled/disabled state;
- coverage/routing priority configuration;
- normalized health/circuit/degraded status;
- last successful reconciliation/health-check metadata;
- secret-presence/credential-reference state such as `CONFIGURED|MISSING`, never the secret value.
- shelter reservation capability state such as `SEARCH_ONLY|BLOCKED_BY_PAYMENT_ARCHITECTURE|CARD_FREE_ENTERPRISE_CONFIGURED`, without card data or unsupported claims that a contract exists.

Admin surfaces must **not** expose:
- API keys/tokens/passwords;
- raw provider webhook secrets;
- arbitrary provider payload dumps;
- provider-specific status as canonical Service Request/Fulfillment state.
- payment-card numbers, security codes, magnetic-stripe data, provider payment forms, or raw payment tokens.

Enabling an adapter that lacks a closed decision/accepted capability is rejected. Disabling an adapter must not delete or rewrite existing FulfillmentAttempt history.

Manual Adapter paths remain first-class and visible as configuration, not as a failure mode.

`ManualShelterAdapter` is mandatory. Admin configuration must not bypass `BLOCKED_BY_PAYMENT_ARCHITECTURE`; `CARD_FREE_ENTERPRISE_CONFIGURED` requires the owner-approved deployment record specified by the v0.1.3 environment contract.

---

## 4. Organization Administrator

Scoped to one Organization:

- invite/suspend/revoke org memberships;
- manage responder `active_for_queue`;
- manage org-owned Resources/Service Offers;
- see org queue/operational health allowed by policy;
- manage org notification defaults that cannot override veteran consent;
- manage org-scoped provider routing/configuration **only if** that capability is explicitly delegated by an accepted admin policy and the underlying provider adapter was enabled globally/for that org.

Cannot:
- see another tenant's veterans/Cases/config;
- publish global questionnaires/signal/consent templates;
- grant self `SUAS_ADMIN`;
- read provider secrets;
- enable an unapproved provider/capability;
- override consent or canonical provider/fulfillment state rules.

---

## 5. Bootstrap / environment configuration

First-run remains [ONBOARDING.md](ONBOARDING.md).

Production bootstrap/status must identify whether required capabilities are actually configured without leaking credentials, including:
- auth/email/SMS availability;
- durable job execution availability;
- database/app environment readiness;
- enabled provider/manual capability paths required by the target launch;
- published questionnaire/consent/safety artifacts required for operation.

A missing optional provider may mark a capability/manual path unavailable/degraded; it must not be silently faked as configured.

---

## 6. Operational administration

Admin read surfaces may expose bounded operational state needed for [OPERATIONS.md](OPERATIONS.md):
- queue depth/oldest job age;
- dead-letter/failed-work counts;
- provider circuit/health/reconciliation backlog;
- notification delivery failure summaries;
- audit/event append health;
- restore/failure-drill status metadata;
- tenant-scoped load/backpressure indicators.

These are operational indicators, not clinical/veteran outcome scores.

---

## 7. Rules

- MFA required for every privileged admin session.
- All privileged writes emit Audit Events.
- Sensitive admin reads are audited where specified.
- Least privilege and tenant scope are enforced at mutation time.
- Admin actions use API command idempotency where retry could duplicate a business/configuration effect.
- Published/versioned artifacts are not edited in place.
- Production data never moves to non-production through ordinary admin export paths.

---

## 8. Non-goals

- clinical administration;
- billing/Medi-Cal administration in MVP;
- raw secret management UI unless a later security spec explicitly authorizes a secret-write flow;
- provider-specific booking console as the canonical SUAS workflow;
- silent impersonation;
- feature flags that redefine domain semantics.

---

## 9. Testability

Required tests include:
- Org Admin cross-tenant action denied without leakage;
- Org Admin cannot self-grant SUAS Admin;
- privileged admin action without MFA denied;
- provider adapter cannot be enabled without accepted/closed decision/config authority;
- provider secret value never returned from admin API/UI;
- disabling adapter preserves FulfillmentAttempt history;
- admin provider status shows normalized health, not vendor-domain state leakage;
- duplicate admin command with same idempotency key produces one logical configuration mutation;
- every successful privileged write emits Audit Event.
