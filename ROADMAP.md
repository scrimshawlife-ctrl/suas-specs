# ROADMAP.md — Path to production

**Stack:** `0.6.0` / `released`  
**Implementation authority:** `RELEASED_FOR_IMPLEMENTATION`  
**Release manifest:** [RELEASE_MANIFEST-0.6.0.md](RELEASE_MANIFEST-0.6.0.md)

Plain list of holes: [GAP_ANALYSIS.md](GAP_ANALYSIS.md).  
Plain list of next work: [REMAINING.md](REMAINING.md).

The owner completed the specification acceptance chain on 2026-08-18 PT. Later releases (native clients, email sign-in, funding overlay) did not start a new SPEC-0xx stage.

## Finished specification stages

SPEC-001 through SPEC-015 are accepted. SPEC-016 is the first released cut. Later manifests (0.2.0 scoring, 0.3.0 phones, 0.6.0 email sign-in) add contracts inside that chain. They do not skip SPEC-017 or SPEC-018.

## SPEC-017 — Implementation conformance

**Status:** recorded (implementation evidence against 0.6.0; not production).

Build `suas`, `suas-ios`, and `suas-android` against pin `0.6.0`. Compare the build with the released files. Send leftovers back here. Code does not invent product rules.

Finishing this stage does not allow production use or a live pilot. Evidence: [SPEC017_EVIDENCE_PACK.md](SPEC017_EVIDENCE_PACK.md) YES; runtime audit on `suas` `docs/SPEC017_COMPLETION_AUDIT.md`.

## Current stage — SPEC-018

**Status:** blocked — owner settled `KEEP_BLOCKED` (`2026-09-26`).

Needs closed launch decisions, measured evidence, and gates that actually move. Packet: [SPEC018_OWNER_LAUNCH_PACKET.md](SPEC018_OWNER_LAUNCH_PACKET.md). See [REMAINING.md](REMAINING.md).

## SPEC-019 — After launch

**Status:** future.

Measured pilot changes. Not grant paperwork. D-037 funding readiness is a separate overlay.

## Order

```text
SPEC-001 ... SPEC-015  accepted
              |
          SPEC-016  released
              |
          SPEC-017  done
              |
          SPEC-018  launch readiness   ← current (blocked)
              |
          SPEC-019  measured revision
```

A release lets you implement. It is not permission to serve veterans.
