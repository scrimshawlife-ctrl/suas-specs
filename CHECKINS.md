# CHECKINS.md — Versioned questionnaires (SUAS v0.1)

**Status:** `draft` / `0.1.0` / SPEC-003 preflight; not implementation authority.  
**Related:** [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [SIGNAL_SCORING.md](SIGNAL_SCORING.md), [EVENT_MODEL.md](EVENT_MODEL.md), [DOMAIN_MODEL.md](DOMAIN_MODEL.md), [DATA_MODEL.md](DATA_MODEL.md), [PRODUCT.md](PRODUCT.md), [PRIVACY.md](PRIVACY.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md)

**Actors:** Veteran (respondent), SUAS System Administrator (publisher), Responder (reader only with basis), System (durable signal trigger).

---

## 1. Purpose

A Check-In is a Veteran's completion or partial completion of a published questionnaire. It is an **input artifact**. It is not a Support Signal, Support Case, or Service Request.

---

## 2. Entities

| Entity | Role |
|---|---|
| `QuestionnaireVersion` | Immutable published questionnaire (`qv-*`) |
| `Question` | Item on a version; may declare a dimension |
| `AnswerOption` | Closed-choice option |
| `CheckIn` | One attempt by a Veteran |
| `CheckInResponse` | One answer on that attempt |

---

## 3. Dimensions

A published version may include questions in these dimensions:

`sleep`, `connection`, `stress`, `basic_needs`, `coping`, `safety`

Exact questions, option weights, and required/optional flags are `NOT_COMPUTABLE` until a QuestionnaireVersion is published. The fill-in home is [SIGNAL_SCORING.md](SIGNAL_SCORING.md) B1 (`TEMPLATE` / `NOT_RELEASED`); empty tables there are not a published version. Do not invent clinical instruments or claim validated psychometrics.

---

## 4. Check-In states

`STARTED` → `IN_PROGRESS` → `COMPLETED` | `ABANDONED` | `INCOMPLETE`

| State | Meaning |
|---|---|
| `STARTED` | Record created; no required answers yet |
| `IN_PROGRESS` | At least one response saved |
| `COMPLETED` | All required questions answered and submitted |
| `INCOMPLETE` | Submitted/timed out with required questions missing and explicitly marked |
| `ABANDONED` | Veteran or system marked abandoned |

### 4.1 Incomplete

An `INCOMPLETE` Check-In may produce a Support Signal only if the published `signal_version` defines deterministic missing-input behavior. Until D-011 is closed, **do not compute a production Support Signal from incomplete input**. Unreleased test fixtures may exercise the interface but must be labeled as such.

### 4.2 Abandoned

Idle timeout is `DECISION_PENDING`. Abandoned Check-Ins remain stored. They do not emit `CHECKIN_COMPLETED`, trigger production Support Signal computation, or open a Support Case by themselves.

### 4.3 Corrections

Completed Check-Ins are not silently rewritten. A veteran correction creates a **new Check-In**. Responders cannot edit veteran answers.

### 4.4 Timing

Record server-authoritative `started_at`, `completed_at`, and `abandoned_at` as applicable. Client clocks may be recorded as non-authoritative metadata but must not determine canonical ordering alone.

### 4.5 Questionnaire migration

When a new QuestionnaireVersion is published:

- in-flight Check-Ins continue on their original version;
- new Check-Ins use the current `PUBLISHED` version;
- historical rows retain their original `questionnaire_version`;
- old questions are not rewritten in place.

---

## 5. Publication

SUAS-admin lifecycle: `DRAFT` → `PUBLISHED` → `SUPERSEDED`.

Published versions are immutable. Publication must be atomic from the reader's perspective: a new Check-In must resolve to one complete published questionnaire version, never a partially published set.

See [ADMIN.md](ADMIN.md) and [VERSIONING.md](VERSIONING.md).

---

## 6. Completion and signal trigger

`COMPLETED` is a committed domain state, not a best-effort UI event.

Rules:

1. The Check-In completion transaction commits before success is returned to the client.
2. Completion emits one logical `CHECKIN_COMPLETED` fact for the Check-In.
3. That fact requests Support Signal computation through durable asynchronous work in production.
4. Queue/job delivery may occur more than once; duplicate delivery must not create duplicate logical signal settlement for the same computation identity.
5. A failed or delayed signal job does not roll the Check-In back from `COMPLETED`.
6. Operations must be able to detect a completed Check-In whose required signal computation has not settled.
7. A replay/recovery path must use the same computation identity rather than inventing a second logical calculation.

The signal computation identity is defined in [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md).

---

## 7. Events and audit

- Domain: `CHECKIN_COMPLETED` only on the first successful transition to `COMPLETED`.
- Audit: start, save, complete, abandon, questionnaire publish, rejected duplicate/illegal completion where operationally relevant.

Retries of the same completion command must not emit multiple logical `CHECKIN_COMPLETED` facts.

See [EVENT_MODEL.md](EVENT_MODEL.md).

---

## 8. Authorization

- Veteran: create/update own in-progress Check-In; read own history.
- Responder: read answers only with `can_view` + `checkin_answers` or the documented assigned-responder basis in [CONSENT.md](CONSENT.md).
- Trusted Contact: only with explicit `can_view` + `checkin_answers`; membership is insufficient.
- Service Providers do not receive Check-In answers by default; provider disclosure follows the minimum-necessary rules in [CONSENT.md](CONSENT.md) and [PRIVACY.md](PRIVACY.md).

---

## 9. Non-goals

- diagnosis;
- continuous passive telemetry as a Check-In;
- third-party clinical assessment import;
- free-text that solicits medical history or SSN;
- using queue delivery count as business-state meaning;
- treating a completed Check-In as proof that a Support Signal has already settled.

---

## 10. Testability

- published questionnaire immutability;
- atomic publication/read behavior;
- in-flight Check-In stays on old version after publish;
- completed Check-In cannot be silently edited;
- abandoned/incomplete do not emit `CHECKIN_COMPLETED`;
- repeated complete command is idempotent at the logical-event level;
- duplicate signal-job delivery produces one logical computation settlement;
- delayed/failed signal job is observable and recoverable without mutating Check-In history;
- CHECK-IN gate in [TESTING.md](TESTING.md) and [STATUS.md](STATUS.md).
