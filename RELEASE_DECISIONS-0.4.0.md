# RELEASE_DECISIONS-0.4.0.md — D-035 sandbox evidence authority

**Release:** `0.4.0`  
**Owner:** `@scrimshawlife-ctrl`  
**Owner action date:** pending owner merge  
**Supersedes for D-035 limited implementation authority only:** none  
**Inherited ledgers:** [RELEASE_DECISIONS-0.3.0.md](RELEASE_DECISIONS-0.3.0.md) for D-033/D-034, [RELEASE_DECISIONS-0.2.0.md](RELEASE_DECISIONS-0.2.0.md) for D-011, [RELEASE_DECISIONS-0.1.5.md](RELEASE_DECISIONS-0.1.5.md) for D-012, [RELEASE_DECISIONS-0.1.3.md](RELEASE_DECISIONS-0.1.3.md) for D-018, [RELEASE_DECISIONS-0.1.2.md](RELEASE_DECISIONS-0.1.2.md) for D-017, and [RELEASE_DECISIONS-0.1.0.md](RELEASE_DECISIONS-0.1.0.md) otherwise  
**Target:** limited sandbox-evidence implementation authority; not final capability acceptance or production-operating approval  
**Production readiness:** `NOT_READY`

| ID | Global decision status | v0.4.0 boundary |
|---|---|---|
| D-035 | `DECISION_PENDING` | Grants the gate qualifier `IMPLEMENTATION_EVIDENCE_AUTHORIZED` solely for the status-only VA Service History and Eligibility OAuth path in LOCAL fixture and VA SANDBOX. The exact scope is `openid profile veteran_status.read`; self-attestation remains available; production remains blocked. |

## Consequences

1. [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md) is the released limited authority. It does not make the broader D-035 proposed contracts final authority.
2. The implementation may produce only the evidence listed there, using synthetic data and VA sandbox credentials/configuration where independently provisioned.
3. `NOT_CONFIRMED != NOT_A_VETERAN`; verification outcomes cannot independently block an explicit support request.
4. No automatic OAuth-to-API-key fallback, `offline_access`, broader VA scope, production credential, production mode, reporting use, background re-verification, or real production Veteran operation is authorized.
5. D-016 remains the authoritative fallback rule. D-035 can be marked `DECIDED` only after the specified evidence is reviewed and explicitly accepted in a later settlement.

## Unchanged release-wide boundary

All readiness gates remain `NOT_READY`. This release does not authorize production deployment, a live pilot, real Veteran data, production VA access, provider effects, reporting authority, D-007 deletion/purge activity, or any production operation.
