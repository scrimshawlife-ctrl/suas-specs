# RELEASE_MANIFEST-0.4.0.md — D-035 sandbox evidence authority release

**Release version:** `0.4.0`  
**Release date:** pending owner merge  
**Owner:** `@scrimshawlife-ctrl`  
**Supersedes:** `0.3.0`  
**Base release:** [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md)  
**Decision ledgers:** [RELEASE_DECISIONS-0.4.0.md](RELEASE_DECISIONS-0.4.0.md) for D-035 limited authority; inherited ledgers govern all earlier decisions  
**Lifecycle:** `released` when this PR is owner-merged  
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION` only within the D-035 gate qualifier  
**Production readiness:** `NOT_READY`

## Release scope

v0.4.0 releases a narrow implementation-evidence authority for D-035. It does not close D-035. It authorizes only the status-only VA Service History and Eligibility OAuth path in LOCAL fixture and VA SANDBOX, solely to generate the evidence required for a later final settlement.

The released authority is [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md). D-016 self-attestation remains sufficient; the approved scope set is `openid profile veteran_status.read`; `offline_access` and broader VA data access remain forbidden; production remains blocked.

## Released artifact set

All v0.3.0 artifacts remain released. v0.4.0 additionally releases:

- [D035_SANDBOX_EVIDENCE_AUTHORITY.md](D035_SANDBOX_EVIDENCE_AUTHORITY.md);
- [RELEASE_DECISIONS-0.4.0.md](RELEASE_DECISIONS-0.4.0.md);
- this manifest; and
- the release-lineage and gate-qualifier updates in [DECISIONS.md](DECISIONS.md), [D035_INDEX.md](D035_INDEX.md), [D035_DECISION_PACKET.md](D035_DECISION_PACKET.md), [VERSIONING.md](VERSIONING.md), [STATUS.md](STATUS.md), [AGENTS.md](AGENTS.md), [HANDOFF.md](HANDOFF.md), [CHANGELOG.md](CHANGELOG.md), and [README.md](README.md).

## Runtime pins

- Expected specification stack: `0.4.0`.
- API selector: `/api/v0` unchanged.
- Event schema: `0.1.0` unchanged.
- Database schema remains implementation-owned and uses its explicit monotonic migration identity.

## Not closed by this release

- D-035 remains `DECISION_PENDING` pending evidence review and final owner settlement.
- D-007, D-025, and all existing production/pilot readiness gates remain unresolved.
- Production VA credentials, production redirect URI, real Veteran data, live pilot use, reporting authority, and any real external operation remain blocked.

## Readiness boundary

All readiness gates remain `NOT_READY`. This release authorizes no production operation and no outcome claim beyond synthetic/local fixture or VA sandbox evidence generation.
