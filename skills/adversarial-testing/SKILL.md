---
name: adversarial-testing
version: 1.0.0
kind: specification
status: active
authority: canonical-spec
inputs: [security_contract, surface_inventory, roles, failure_expectations]
outputs: [negative_test_contract]
fail_closed: true
self_test: skills/self-tests/adversarial-testing.yaml
---

# adversarial-testing

## Purpose
Define deterministic negative-path evidence for SUAS boundaries that must fail closed.

## Trigger
Use for auth, authorization, tenant isolation, replay/idempotency, provider failures, disabled features, malformed inputs, ambiguous mutations, reports/admin access, or any boundary-sensitive change.

## Inputs
- Governing security/domain contract.
- Surface inventory: API, DB, jobs, caches, adapters, reports, admin.
- Environment and credential roles.
- Expected failure behavior and prohibited side effects.

## Procedure
1. Read `AGENTS.md`, security/auth/environment specs, and applicable release contract.
2. Enumerate relevant attack/negative cases: unauthenticated, unauthorized, wrong-role, wrong-tenant, stale/revoked credential, malformed input, replay, duplicate delivery, unavailable provider, disabled feature, timeout, and ambiguous provider outcome.
3. Map each case to each relevant surface boundary.
4. Define expected status/result, persistence behavior, external-effect behavior, audit/provenance expectation, and retry semantics.
5. Include cross-tenant negatives for all surfaces carrying tenant-scoped state.
6. Require rejected operations to cause no unauthorized persistent or external business effect.
7. Require ambiguous mutations to reconcile before risky retry.
8. Record reproducible setup, evidence, and verdict for each case.

## Invocation example
`Define fail-closed coverage for the operator reporting surface, including cross-tenant and disabled-mode cases plus prohibited persistent/external effects.`

## Output schema
```yaml
test_set_id: string
environment: string
cases:
  - id: string
    boundary: string
    attack: string
    expected: string
    persistent_effect_allowed: false
    external_effect_allowed: false
    result: PASS|FAIL|NOT_COMPUTABLE
    evidence: string|null
cross_tenant_coverage: [string]
findings: [string]
verdict: PASS|FAIL|NOT_COMPUTABLE
```

## Prohibited actions
- Do not treat absence of a known exploit as proof of isolation.
- Do not omit persistent/external side-effect checks.
- Do not use production data or unauthorized credentials.

## Self-test
Run `skills/self-tests/adversarial-testing.yaml`. The fixture must fail if a rejected wrong-tenant request creates any persistent or external business effect.

## Completion criteria
Complete only when every applicable fail-closed boundary has explicit negative coverage or is marked NOT_COMPUTABLE with the missing prerequisite identified.