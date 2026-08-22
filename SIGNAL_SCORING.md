# SIGNAL_SCORING.md — D-011 fill-in template (SUAS)

**Status:** `TEMPLATE` / `NOT_RELEASED`  
**Decision:** D-011 remains `DECISION_PENDING`  
**Authority:** none. Released `0.1.6` remains the implementation contract ([RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md)).  
**Related:** [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §2, [CHECKINS.md](CHECKINS.md) §3–§4.1, [DECISIONS.md](DECISIONS.md) D-011, [TESTING.md](TESTING.md) §12, [SAFETY.md](SAFETY.md) §3.2, [VERSIONING.md](VERSIONING.md) §3, [ADMIN.md](ADMIN.md)

This file is empty on purpose. Fill the tables. Do not invent weights, thresholds, golden vectors, questionnaire wording, or clinical claims in a change that only adds or points at this template. A later release may close D-011 only after B1–B5 are filled and a `RELEASE_DECISIONS-0.1.x.md` plus matching manifest are written.

---

## 0. What this is / is not

A Support Signal is a **coordination priority label**, not a diagnosis, clinical assessment, or suicidality determination ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §1). Values are exactly:

`GREEN` | `YELLOW` | `ORANGE` | `RED`

This template:

- is the fill-in home for D-011 rows B1–B5;
- may also record optional G-I-28 action fields that depend on scores existing;
- does **not** close D-011;
- does **not** publish a production `signal_version` or `QuestionnaireVersion`;
- does **not** authorize production scoring, real veteran data, or SPEC-018 readiness;
- does **not** claim HIPAA applicability, psychometrics, or validated clinical instruments ([CHECKINS.md](CHECKINS.md) §3, [DECISIONS.md](DECISIONS.md) D-006).

Dimension **names** below are already released in [CHECKINS.md](CHECKINS.md) §3. Questions, options, required flags, and weights are not.

---

## B1 — Questionnaire content

Fill questions, closed options, required flags, and option weights. Add or delete rows. Question count per dimension is owner-filled, not implied by the blank starter row.

Free text is excluded from canonical scoring input ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §10). Do not add free-text items that solicit medical history or SSN ([CHECKINS.md](CHECKINS.md) §9).

### `sleep`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### `connection`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### `stress`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### `basic_needs`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### `coping`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### `safety`

| question_key | prompt | required (yes/no) | option_id | option_label | option_weight |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

---

## B2 — Deterministic map

Fill how canonical answers + `signal_version` + questionnaire version produce `level` and inspectable `basis`. Same inputs + same versions must yield the same `level` and semantically equivalent `basis` ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §2).

**No generative model may produce the primary signal.**

| Field | Owner fill |
|---|---|
| How option weights combine (per question / per dimension / overall) |  |
| How combined values map to `GREEN` |  |
| How combined values map to `YELLOW` |  |
| How combined values map to `ORANGE` |  |
| How combined values map to `RED` |  |
| Any dimension or option that forces a level (if none, write `none`) |  |
| What `basis` must record (canonical inputs/rules; no unnecessary sensitive payload) |  |

| rule_id | When (canonical condition) | Resulting `level` | What `basis` records |
|---|---|---|---|
|  |  |  |  |

---

## B3 — Incomplete input

Until this row is filled and D-011 closes, production compute from `INCOMPLETE` stays forbidden ([CHECKINS.md](CHECKINS.md) §4.1). The current released default is **refuse**.

Choose exactly one. Do not invent a third option.

| Choice | Mark one (`yes` / leave blank) | If missing-input function, write the function here |
|---|---|---|
| Refuse (no production Support Signal from `INCOMPLETE`) |  | — |
| Written deterministic missing-input function |  |  |

---

## B4 — Golden vectors

Fixed canonical inputs + versions → expected `level` + `basis` for that published pair. Stay `UNRELEASED_FIXTURE` until this table is released with D-011 ([TESTING.md](TESTING.md) §12).

| vector_id | questionnaire_version | signal_version | canonical answers | expected `level` | expected `basis` notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

---

## B5 — Version identities

Runtime content versions stay distinct from the specification stack version ([VERSIONING.md](VERSIONING.md) §3). A new `signal_version` or questionnaire version writes new rows and never mutates history ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §6).

| Field | Owner fill |
|---|---|
| `questionnaire_version` id |  |
| `signal_version` id |  |
| Publication note (immutable; new version = new rows) |  |

---

## G-I-28 action (optional ride-along)

[SAFETY.md](SAFETY.md) §3.2 already requires that an effective `RED` open or update a Support Case with `priority_signal_level=RED`. P-22 modeled the field, not the command that writes it. Fill if closing with D-011; otherwise leave blank.

| Field | Owner fill |
|---|---|
| Command name |  |
| Idempotency identity |  |
| Which levels open vs update a Support Case |  |
| Behavior if a Support Case is already `CLOSED` |  |

Not D-011: effective-signal **selection** ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §7.1), abandoned Check-In idle timeout ([CHECKINS.md](CHECKINS.md) §4.2), island/crisis numbers (D-026).

---

## Later close checklist (not this change)

A later owner-controlled release may close D-011 only when all of the following are true:

1. B1–B5 are filled (G-I-28 optional here; required before signal-driven case write).
2. `RELEASE_DECISIONS-0.1.x.md` records the close.
3. [DECISIONS.md](DECISIONS.md) D-011 moves to `DECIDED`.
4. A new [RELEASE_MANIFEST](RELEASE_MANIFEST-0.1.6.md) lists the filled artifact.
5. Golden vectors in B4 are released (no longer `UNRELEASED_FIXTURE` only).

This template change does none of those steps.
