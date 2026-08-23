# SUPPORT_SIGNALS.md — Deterministic coordination signals (SUAS v0.1)

**Status:** `draft` / `0.1.0` / SPEC-003 preflight; not implementation authority.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).  
**Related:** [CHECKINS.md](CHECKINS.md), [SIGNAL_SCORING.md](SIGNAL_SCORING.md), [SAFETY.md](SAFETY.md), [CASES.md](CASES.md), [CONSENT.md](CONSENT.md), [EVENT_MODEL.md](EVENT_MODEL.md), [TESTING.md](TESTING.md), [DECISIONS.md](DECISIONS.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md)

**Actors:** System (compute), Veteran (source of Check-In), Responder (may override with reason), SUAS System Administrator (publishes `signal_version`).

---

## 1. Purpose

A Support Signal is a **coordination priority label**, not a diagnosis, clinical assessment, or suicidality determination.

Values are exactly:

`GREEN` | `YELLOW` | `ORANGE` | `RED`

---

## 2. Computation contract

The primary signal must be:

| Property | Requirement |
|---|---|
| Deterministic | Same canonical inputs + same `signal_version` + same questionnaire version → same `level` and semantically equivalent `basis` |
| Inspectable | `basis` records the canonical inputs/rules used without unnecessary sensitive payload duplication |
| Versioned | `signal_version` is a published immutable identifier |
| Unit-tested | Golden vectors per published version |
| Reproducible | Historical calculations remain explainable without mutation |
| Idempotently settled | Duplicate job delivery does not create duplicate logical computation results |

**No generative model may produce the primary signal.**

D-011 is `DECIDED` for `qv-001` + `sv-001`. Exact questionnaire content, deterministic rules, incomplete-input behavior, basis requirements, and golden vectors are released in [SIGNAL_SCORING.md](SIGNAL_SCORING.md). Implementations must not mutate those published identities or invent alternate weights/thresholds under them.

---

## 3. Computation identity

For a Check-In-derived primary calculation, the logical computation identity is the tuple:

```text
check_in_id
signal_version
input_questionnaire_version
computation_kind = PRIMARY
```

The persisted representation may use a derived `computation_key`, unique constraint, or equivalent mechanism, but it must preserve the following semantics:

1. Re-delivering the same computation request settles to the same logical primary calculation.
2. Concurrent workers cannot create two authoritative primary rows for the same computation identity.
3. A deliberate recomputation under a **new** `signal_version` is a different computation identity and writes a new row.
4. An override is not a primary recomputation; it is a distinct immutable Support Signal linked through `override_of_signal_id`.
5. Recovery/replay must not silently mutate or duplicate the historical primary result.

For an explicit need without a Check-In, the computation identity must include a stable source record/reference defined by the later accepted domain/data model; `check_in_id = null` alone is insufficient as an idempotency identity.

---

## 4. Recorded fields

Primary/override rows record at least:

- `support_signal_id`
- `signal_version`
- `input_questionnaire_version`
- `computed_at`
- `basis`
- `level`
- `veteran_profile_id`
- `check_in_id` when Check-In-derived
- stable source reference when not Check-In-derived
- computation identity/key or equivalent uniqueness evidence for primary calculations
- override linkage/actor/reason when applicable

Exact physical columns are reconciled later in [DATA_MODEL.md](DATA_MODEL.md); the semantics above are authoritative for SPEC-003 review.

---

## 5. Settlement and event semantics

A primary calculation is **settled** only after the immutable Support Signal row is durably persisted.

Rules:

1. The computation job may be delivered more than once.
2. Persistence must resolve duplicates atomically by computation identity.
3. Exactly one logical `SUPPORT_SIGNAL_CHANGED` fact is emitted when the newly persisted effective signal constitutes a domain change that the event contract requires.
4. A duplicate worker replay that resolves to the already-settled row does not emit a second logical change event.
5. Event publication must be transactionally coupled or use an outbox/equivalent replay-safe mechanism; a database commit followed by a lost process must not permanently lose the required event.
6. Operations must be able to detect a completed Check-In whose expected signal settlement/event publication is missing or delayed.

This is **exactly-once observable business meaning**, not a claim that infrastructure delivers messages exactly once.

---

## 6. Historical integrity

No silent mutation of historical calculations.

- A new `signal_version` does not rewrite old rows.
- Recalculation writes a new row under a distinct valid computation identity.
- Overrides write a new row with `override_of_signal_id`, `override_actor_id`, and `override_reason`.
- The original computed signal remains immutable.

---

## 7. Override policy

- **Who:** assigned Responder or SUAS-admin.
- **When:** documented disagreement with the computed coordination label.
- **Required:** reason, actor, timestamp, link to original/effective signal.
- Override is not diagnosis and does not erase the computed signal.
- Red-state behavior in [SAFETY.md](SAFETY.md) applies to the effective signal used for coordination.
- Lowering a `RED` is audited and cannot retroactively remove already-surfaced safety UI or historical actions.

### 7.1 Effective-signal selection (deterministic, 0.1.4)

The current effective signal is selected deterministically from the chain of primary calculations/overrides: the **most recent by `computed_at`**, with ties broken by **`support_signal_id` descending**, and an `OVERRIDE` **superseding the signal it overrides**. This is selection, not scoring, and is independent of the D-011 threshold decision; implementation must never infer it from row insertion order alone. Reconciled into [DATA_MODEL.md](DATA_MODEL.md) §4.

Two-override / chain rule (0.1.6, transcribes the 0.1.4 selection already implemented): a row is **excluded** from the candidate set if **any** later row names it in `override_of_signal_id`. Remaining candidates are ordered by `computed_at DESC`, then `support_signal_id DESC`; the first remaining row is effective. Therefore:

- two overrides of the **same** target both remain candidates; recency (then id) wins;
- a sequential override chain (`A` ← `B` ← `C`) excludes each named target, so `C` wins if it is the newest remaining row.

---

## 8. Relationship to the canonical loop

SIGNAL is the first canonical-loop stage. `YELLOW`, `ORANGE`, or `RED` may cause a Support Case to open/update according to [CASES.md](CASES.md). A Support Signal is not itself a Service Request.

Signal-driven case effects must consume the settled Support Signal/event idempotently. Duplicate event/job delivery must not create duplicate Cases or repeated hidden transitions.

---

## 9. Visibility

Per [CONSENT.md](CONSENT.md): `can_view` + `support_signal`. Trusted Circle membership is insufficient. Notifications at a level require `can_receive` + that level.

Service Providers do not receive the full Support Signal or `basis` by default; external fulfillment disclosure follows the minimum-necessary provider projection rules.

---

## 10. Non-goals

- diagnosis;
- suicide prediction/suicidality scoring;
- generative interpretation of free text as primary signal;
- mutating prior signals when rules change;
- treating queue delivery as a new calculation;
- claiming exactly-once infrastructure delivery;
- deriving effective signal by unspecified database ordering.

---

## 11. Testability

Critical suite: **support-signal determinism and settlement**.

- golden vectors: fixed canonical inputs/version → fixed level + basis;
- duplicate concurrent computation settles one logical primary result;
- duplicate job replay emits no duplicate logical change event;
- new signal version creates a distinct immutable calculation;
- override creates a linked immutable row;
- effective-signal selection is deterministic under the accepted 0.1.4/§7.1 rule, including the two-override / chain case;
- committed Check-In + interrupted worker can be recovered to the correct settlement;
- no generative path exists in primary compute.
