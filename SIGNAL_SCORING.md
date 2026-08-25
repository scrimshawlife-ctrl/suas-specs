# SIGNAL_SCORING.md — D-011 Support Signal scoring contract (SUAS)

**Status:** `released` by [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md) on owner merge  
**Decision:** D-011 `DECIDED` for `qv-001` + `sv-001`  
**Authority:** [RELEASE_MANIFEST-0.2.0.md](RELEASE_MANIFEST-0.2.0.md)  
**Related:** [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §2, [CHECKINS.md](CHECKINS.md) §3–§4.1, [DECISIONS.md](DECISIONS.md) D-011, [TESTING.md](TESTING.md) §12, [SAFETY.md](SAFETY.md) §3.2, [VERSIONING.md](VERSIONING.md) §3, [ADMIN.md](ADMIN.md)

A Support Signal is a **coordination priority label**, not a diagnosis, clinical assessment, suicidality determination, or validated psychometric score. Values are exactly:

`GREEN` | `YELLOW` | `ORANGE` | `RED`

No generative model may produce the primary signal. Free text is excluded from canonical scoring input. The questionnaire must not solicit medical history or SSN.

---

## B1 — Questionnaire content

Question keys and option IDs are stable canonical identifiers within `qv-001`. Six core questions are required. Three follow-ups are optional. An unanswered optional question does not make a Check-In `INCOMPLETE` and does not contribute a weight.

### `sleep`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `sleep_manage_7d` | During the past 7 days, how much has sleep made it harder to manage your daily needs? | yes | `NOT_AT_ALL` | Not at all | 0 |
| `sleep_manage_7d` | — | yes | `A_LITTLE` | A little | 1 |
| `sleep_manage_7d` | — | yes | `A_LOT` | A lot | 2 |
| `sleep_manage_7d` | — | yes | `UNABLE_TO_MANAGE` | I have been unable to manage | 3 |

### `connection`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `reliable_connection_now` | How connected do you feel to people or services you can rely on right now? | yes | `WELL_CONNECTED` | Well connected | 0 |
| `reliable_connection_now` | — | yes | `SOMEWHAT_CONNECTED` | Somewhat connected | 1 |
| `reliable_connection_now` | — | yes | `BARELY_CONNECTED` | Barely connected | 2 |
| `reliable_connection_now` | — | yes | `NOT_CONNECTED` | Not connected | 3 |

### `stress`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `stress_manage_7d` | During the past 7 days, how much has stress made it harder to handle what needs your attention? | yes | `NOT_AT_ALL` | Not at all | 0 |
| `stress_manage_7d` | — | yes | `A_LITTLE` | A little | 1 |
| `stress_manage_7d` | — | yes | `A_LOT` | A lot | 2 |
| `stress_manage_7d` | — | yes | `UNABLE_TO_MANAGE` | I have been unable to manage | 3 |

### `basic_needs`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `basic_needs_48h` | How secure are your food, shelter, transportation, and essential supplies for the next 48 hours? | yes | `SECURE` | Secure | 0 |
| `basic_needs_48h` | — | yes | `ONE_MANAGEABLE_CONCERN` | One manageable concern | 1 |
| `basic_needs_48h` | — | yes | `IMPORTANT_GAP` | An important gap | 2 |
| `basic_needs_48h` | — | yes | `IMMEDIATE_NEED` | An immediate need | 3 |
| `basic_need_urgency` | How soon do you need help with your most important basic need? | no | `NO_HELP_NEEDED` | No help needed | 0 |
| `basic_need_urgency` | — | no | `AFTER_48_HOURS` | After 48 hours | 1 |
| `basic_need_urgency` | — | no | `WITHIN_48_HOURS` | Within 48 hours | 2 |
| `basic_need_urgency` | — | no | `TODAY` | Today | 3 |

### `coping`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `coping_24h` | How able do you feel to get through the next 24 hours with the support available to you? | yes | `ABLE` | Able | 0 |
| `coping_24h` | — | yes | `MOSTLY_ABLE` | Mostly able | 1 |
| `coping_24h` | — | yes | `STRUGGLING` | Struggling | 2 |
| `coping_24h` | — | yes | `UNABLE` | Unable | 3 |
| `support_reachable` | If things become harder, can you reach a person or service that can support you? | no | `YES` | Yes | 0 |
| `support_reachable` | — | no | `PROBABLY` | Probably | 1 |
| `support_reachable` | — | no | `NOT_SURE` | Not sure | 2 |
| `support_reachable` | — | no | `NO` | No | 3 |

### `safety`

| question_key | prompt | required | option_id | option_label | option_weight |
|---|---|---:|---|---|---:|
| `safe_now` | Do you feel safe right now? | yes | `YES` | Yes | 0 |
| `safe_now` | — | yes | `MOSTLY_WITH_CONCERN` | Mostly, but I have a concern | 1 |
| `safe_now` | — | yes | `NO_SUPPORT_SOON` | No; I need support soon | 2 |
| `safe_now` | — | yes | `NO_IMMEDIATE_HELP` | No; I need immediate help | 3 |
| `immediate_danger` | Are you in immediate danger or do you need emergency help now? | no | `NO` | No | 0 |
| `immediate_danger` | — | no | `NOT_SURE` | Not sure | 2 |
| `immediate_danger` | — | no | `YES` | Yes | 3 |

The approved crisis interface in [SAFETY_COPY.md](SAFETY_COPY.md) is independent of signal settlement. A Support Signal must never be presented as proof of emergency dispatch.

---

## B2 — Deterministic map

### Canonical dimension calculation

For each dimension `d`:

```text
dimension_score(d) =
  max(weight of each answered or B3-imputed question in dimension d)
```

Unanswered optional questions are excluded. Optional answers may raise but never dilute the dimension score.

Rules execute in the order below. The first matching rule wins.

| rule_id | Canonical condition | level | basis requirement |
|---|---|---|---|
| `R-RED-01` | `safe_now = NO_IMMEDIATE_HELP` | `RED` | Record exact option ID, safety score, and rule ID |
| `R-RED-02` | `immediate_danger = YES` | `RED` | Record exact option ID, safety score, and rule ID |
| `R-ORANGE-01` | Safety dimension score equals 2 | `ORANGE` | Record contributing safety option IDs, score, and rule ID |
| `R-ORANGE-02` | Any non-safety dimension score equals 3 | `ORANGE` | Record contributing option IDs, dimension scores, and rule ID |
| `R-ORANGE-03` | At least two dimensions have scores greater than or equal to 2 | `ORANGE` | Record qualifying dimensions/scores and rule ID |
| `R-YELLOW-01` | Any dimension score equals 1 or 2 | `YELLOW` | Record contributing option IDs, dimension scores, and rule ID |
| `R-GREEN-01` | Every dimension score equals 0 | `GREEN` | Record dimension scores and rule ID |

Only explicit safety answers can produce `RED`. Missing or imputed input cannot force `RED`.

### Canonical `basis`

`basis` records:

- `questionnaire_version`;
- `signal_version`;
- answered `question_key → option_id` pairs;
- missing required question keys;
- imputed question keys;
- all six dimension scores;
- exactly one `matched_rule_id`.

It does not copy prompts, labels, free text, or unrelated veteran data. Semantic equivalence, not byte-for-byte serialization, is required.

---

## B3 — Incomplete input

`sv-001` uses this deterministic missing-input function:

1. If any required safety question is missing, refuse computation with `MISSING_REQUIRED_SAFETY_INPUT`. Persist no Support Signal row.
2. For every missing required non-safety question, use weight `2` for that calculation.
3. Record every missing and imputed question key in `basis`.
4. Exclude unanswered optional questions.
5. Apply the ordered B2 rules normally.
6. Missing or imputed input alone cannot produce `RED`.

A computation with non-safety imputation may produce `YELLOW` or `ORANGE`.

---

## B4 — Released golden vectors

All vectors use `questionnaire_version=qv-001` and `signal_version=sv-001`.

Define the complete required-answer baseline `A0`:

```json
{
  "sleep_manage_7d": "NOT_AT_ALL",
  "reliable_connection_now": "WELL_CONNECTED",
  "stress_manage_7d": "NOT_AT_ALL",
  "basic_needs_48h": "SECURE",
  "coping_24h": "ABLE",
  "safe_now": "YES"
}
```

“`A0` with” means replace the named baseline entries and, where stated, add optional entries. This produces a complete fixed canonical input.

| vector_id | canonical answers | expected outcome | expected basis facts |
|---|---|---|---|
| `GV-001` | `A0` | `GREEN` | Scores `0,0,0,0,0,0`; `R-GREEN-01`; no missing/imputed keys |
| `GV-002` | `A0` with `sleep_manage_7d=A_LITTLE` | `YELLOW` | Sleep 1; others 0; `R-YELLOW-01` |
| `GV-003` | `A0` with `basic_needs_48h=IMPORTANT_GAP` | `YELLOW` | Basic needs 2; others 0; `R-YELLOW-01` |
| `GV-004` | `A0` with `stress_manage_7d=A_LOT`, `reliable_connection_now=BARELY_CONNECTED` | `ORANGE` | Stress 2; connection 2; `R-ORANGE-03` |
| `GV-005` | `A0` with `basic_needs_48h=IMMEDIATE_NEED` | `ORANGE` | Basic needs 3; `R-ORANGE-02` |
| `GV-006` | `A0` with `safe_now=NO_SUPPORT_SOON` | `ORANGE` | Safety 2; `R-ORANGE-01` |
| `GV-007` | `A0` with `safe_now=NO_IMMEDIATE_HELP` | `RED` | Safety 3; `R-RED-01` |
| `GV-008` | `A0` plus `immediate_danger=YES` | `RED` | Safety 3; `R-RED-02` |
| `GV-009` | `A0` without `safe_now` | refused; no Support Signal | `MISSING_REQUIRED_SAFETY_INPUT`; no persisted basis |
| `GV-010` | `A0` without `sleep_manage_7d` | `YELLOW` | Sleep 2; missing/imputed `sleep_manage_7d`; `R-YELLOW-01` |
| `GV-011` | `A0` without `sleep_manage_7d` and `stress_manage_7d` | `ORANGE` | Sleep 2; stress 2; both keys missing/imputed; `R-ORANGE-03` |
| `GV-012` | `A0` plus `basic_need_urgency=TODAY` | `ORANGE` | Basic needs 3; `R-ORANGE-02` |
| `GV-013` | `A0`; all optional questions unanswered | `GREEN` | Same as GV-001; optional keys absent, not missing/imputed |
| `GV-014` | `A0` plus `immediate_danger=YES` | `RED` | Explicit safety conflict resolves by precedence to `R-RED-02` |

The conformance suite also proves repeat calculation semantic equivalence, computation-identity idempotency, replay safety, and immutability under a new `signal_version`; those are settlement/version tests, not additional scoring vectors.

---

## B5 — Version identities

| Field | Released value |
|---|---|
| Specification stack | `0.2.0` |
| `questionnaire_version` | `qv-001` |
| `signal_version` | `sv-001` |
| API selector | `/api/v0` unchanged |
| Event schema | `0.1.0` unchanged |
| Publication rule | Published content is immutable. Any content or scoring change creates a new runtime version and new historical rows. |

Git SHA, application version, and database migration version remain separate identities under [VERSIONING.md](VERSIONING.md).

---

## G-I-28 action — transcribed from SAFETY.md §3.2

[SAFETY.md](SAFETY.md) §3.2 already requires an effective `RED` to open or update a Support Case with `priority_signal_level=RED`. D-011 defines scoring only. This section names the command that writes the already-released RED obligation. It is not a new D-0xx. It does not authorize production scoring, real provider effects, or any readiness-gate advance.

### APPLY_EFFECTIVE_SIGNAL

| Question | Answer (transcribed, fail-closed) |
|---|---|
| **Command** | `APPLY_EFFECTIVE_SIGNAL`. System actor. Runs in the same transaction as the settled Support Signal insert. |
| **Idempotency** | One apply per settled `support_signal_id`. Replay of the same settlement is a no-op. Concurrent creates still resolve to one non-closed Case ([CASES.md](CASES.md) §3.1). |
| **Non-RED effects** | None. [SAFETY.md](SAFETY.md) §4 says `YELLOW`/`ORANGE` *may* open or update a case; that is not a must. Explicit Veteran/Responder case-open remains the path for those levels ([CASES.md](CASES.md) §3 item 2). A later non-RED signal does not downgrade or close a RED case ([SAFETY.md](SAFETY.md) §3.2). |
| **CLOSED-case** | `CLOSED` is not an active coordination state. RED opens a **new** Case. It does not `REOPEN` the closed Case (`REOPEN` remains the human command in [CASES.md](CASES.md) §4.2). |

Not D-011: effective-signal selection ([SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md) §7.1), abandoned Check-In idle timeout ([CHECKINS.md](CHECKINS.md) §4.2), or island/crisis-number decisions.
