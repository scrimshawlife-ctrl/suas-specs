# RELEASE_MANIFEST-0.5.0.md — D-035 capability settlement

**Release version:** `0.5.0`  
**Release date:** `2026-08-29`  
**Owner:** `@scrimshawlife-ctrl`  
**Supersedes:** `0.4.0`  
**Decision ledger:** [RELEASE_DECISIONS-0.5.0.md](RELEASE_DECISIONS-0.5.0.md)  
**Lifecycle:** `RELEASED_FOR_IMPLEMENTATION`  
**Production readiness:** `NOT_READY`

## Release scope

v0.5.0 settles D-035 as an optional, status-only VA sandbox capability. The released implementation boundary is limited to LOCAL fixture and VA SANDBOX. D-016 self-attestation remains the permitted fallback.

## Released artifacts

- [RELEASE_DECISIONS-0.5.0.md](RELEASE_DECISIONS-0.5.0.md)
- [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md)
- [DECISIONS.md](DECISIONS.md)
- [D035_INDEX.md](D035_INDEX.md)

## Explicit prohibitions

No production VA credentials, production redirect URI, `offline_access`, broader VA data access, background re-verification, reporting use under D-035, DD-214 or SSN collection, or real production Veteran operation is authorized.

## Readiness boundary

`PILOT_LAUNCH=blocked` and `PRODUCTION_LAUNCH=blocked`. D-007 deletion/export/purge controls remain independently governed and unchanged. D-025 remains controlling for reporting.

**Provenance:** Notion Sprint 001 Hub + Loop 805 Slice 14 + Hash: owner-reviewed-staging-acceptance-33278273697
