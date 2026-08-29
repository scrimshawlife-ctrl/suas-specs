# D035_INDEX.md — Veteran verification spec index

**Decision:** D-035  
**Lifecycle:** proposed / not release-authoritative

## Canonical read order

1. [DECISIONS.md](DECISIONS.md) — decision status and relationship to released stack.
2. [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md) — canonical product/domain contract.
3. [D035_PROTOCOL.md](D035_PROTOCOL.md) — provider selection, protocol/state machines, OAuth/API-key boundaries, failures, idempotency, observability.
4. [D035_VA_CONFIRMATION_ADAPTER.md](D035_VA_CONFIRMATION_ADAPTER.md) — concrete Veteran Confirmation API v1 adapter contract: `POST /status`, `apikey` header, environment/secret handling, demographic projection gate, normalization, retries, redaction, evidence.
5. [D035_ASSIMILATION.md](D035_ASSIMILATION.md) — cross-spec interpretation against onboarding/API/auth/consent/data/security/testing/environment/mobile/events/reporting.
6. [D035_TEST_VECTORS.md](D035_TEST_VECTORS.md) — deterministic acceptance and negative vectors.
7. [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md) — owner questions and settlement form.

## Authority rule

Until D-035 is explicitly settled and released:

```text
D-016 is authoritative.
VA verification is not required.
Self-attestation remains sufficient for the released pilot.
VA production operation is blocked.
```

If older proposed D-035 text conflicts with the current [VETERAN_VERIFICATION.md](VETERAN_VERIFICATION.md), [D035_PROTOCOL.md](D035_PROTOCOL.md), or provider-specific adapter contract, the later, more specific canonical rule applies for the D-035 proposal. Released specs remain authoritative until D-035 release.

## Provider-selection rule

Do not choose an adapter merely because its response is narrower.

Select the adapter by the minimum **total SUAS data flow** after Privacy Owner review:

```text
Veteran Confirmation API
  = narrow status response
  + demographic matching data supplied by SUAS
  + API-key security boundary

Service History/Eligibility status scope
  = Veteran-mediated OAuth/OIDC
  + token/callback security boundary
  + explicitly constrained veteran_status.read scope
```

The initial adapter is an owner decision in [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md).

## Required implementation outputs after release

A coding agent must not begin by guessing provider details. It must produce, in order:

```text
1. chosen adapter declaration
2. exact data projection/scope manifest + hash
3. domain port/types
4. attempt/authorization state persistence
5. adapter implementation
6. SUAS-owned API surface
7. onboarding UX states
8. audit/redaction controls
9. deterministic test vectors
10. sandbox evidence packet
11. owner/readiness settlement
```

For `VaVeteranConfirmationAdapter`, [D035_VA_CONFIRMATION_ADAPTER.md](D035_VA_CONFIRMATION_ADAPTER.md) is the provider-specific implementation contract and MUST be read before coding.

Production remains disabled until explicit production re-settlement.
