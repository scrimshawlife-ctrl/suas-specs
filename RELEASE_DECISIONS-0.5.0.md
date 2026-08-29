# RELEASE_DECISIONS-0.5.0.md — D-035 final sandbox capability settlement

**Release:** `0.5.0`  
**Owner:** `@scrimshawlife-ctrl`  
**Owner decision:** `ACCEPT`  
**Decision date:** `2026-08-29`  
**Supersedes:** `RELEASE_DECISIONS-0.4.0.md` for D-035 only  
**Production readiness:** `NOT_READY`

## D-035 settlement

| ID | Global decision status | Released boundary |
|---|---|---|
| D-035 | `DECIDED` | Optional VA-backed Veteran-status verification using `VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY` in LOCAL fixture and VA SANDBOX only. D-016 self-attestation remains available. |

### Accepted contract

- Capability: `OPTIONAL_VA_VETERAN_STATUS_VERIFICATION`.
- Adapter family: `VA_SERVICE_HISTORY_ELIGIBILITY_STATUS_ONLY`.
- OAuth scopes: `openid profile veteran_status.read`.
- Authorization: OAuth 2.0 / OIDC Authorization Code Grant with PKCE S256.
- Re-verification: `ONE_TIME_ONBOARDING_ONLY`; no background re-verification; no `offline_access`.
- Fallback: `SELF_ATTESTATION_REMAINS_AVAILABLE` under D-016.
- Semantic invariant: `ACCEPT`; `NOT_CONFIRMED != NOT_A_VETERAN`.
- Support invariant: VA failure, cancellation, outage, or non-confirmation MUST NOT independently block an explicit support request.
- Retention: normalized verification evidence only; no raw VA payloads or access/refresh tokens in domain storage.

### Evidence acceptance

The owner accepted the staging evidence packet covering scope containment, PKCE/state/replay/JWT validation, privacy and redaction posture, environment isolation, and accessibility review. The exact VA sandbox client identifier and redirect registration remain in the owner-controlled provider record and are intentionally not reproduced here.

Evidence anchors:

- SUAS implementation commit: `8aa72e83bdb0793624413bef46f022031c052332`.
- Staging acceptance: https://github.com/scrimshawlife-ctrl/suas/actions/runs/33278273697
- Staging environment: `https://suas-synthetic-staging.suas.workers.dev`.
- Dedicated Hyperdrive: `c911341ef88243e6a2ecf87e81c26984`.
- Dedicated Neon project: `icy-dream-35162273`.

### Authority boundary

This decision adds no reporting authority; D-025 remains controlling. D-007 remains independently unresolved. Production VA credentials, production redirect configuration, real Veteran data, and production launch remain blocked.

**Provenance:** Notion Sprint 001 Hub + Loop 805 Slice 14 + Hash: owner-reviewed-staging-acceptance-33278273697
