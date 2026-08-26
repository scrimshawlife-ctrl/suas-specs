# CASES.md — Support Case state machine (SUAS v0.1)

**Status:** `draft` / `0.1.0` / SPEC-004 preflight; not implementation authority.  
**Authority:** released via [RELEASE_MANIFEST-0.1.6.md](RELEASE_MANIFEST-0.1.6.md). The inline `draft` marker is stale and is not authority ([VERSIONING.md](VERSIONING.md) §1).
**Related:** [DISPATCH.md](DISPATCH.md), [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md), [FOLLOWUP.md](FOLLOWUP.md), [SETTLEMENT.md](SETTLEMENT.md), [SUPPORT_SIGNALS.md](SUPPORT_SIGNALS.md), [EVENT_MODEL.md](EVENT_MODEL.md), [API.md](API.md), [SCALING.md](SCALING.md), [RESILIENCE.md](RESILIENCE.md), [DECISIONS.md](DECISIONS.md)

**Actors:** System, Responder, Organization Administrator, Veteran (limited), SUAS System Administrator (audited break-glass where specified).

---

## 1. Purpose

A **Support Case** is coordination around a Veteran. It is not a Service Request. One case may contain multiple Service Requests.

---

## 2. States

Exactly:

`OPEN` → `TRIAGED` → `ASSIGNED` → `ACTIVE` → `FOLLOWUP` → `RESOLVED` → `CLOSED`

| State | Meaning |
|---|---|
| `OPEN` | Case exists; not yet triaged |
| `TRIAGED` | Need/priority reviewed; not yet assigned |
| `ASSIGNED` | An active CaseAssignment exists; work may not have started |
| `ACTIVE` | Assigned responder is actively coordinating |
| `FOLLOWUP` | Primary coordination work is done/paused; Follow-Up remains |
| `RESOLVED` | Settlement exists; blocking work is settled |
| `CLOSED` | Terminal for this case cycle; history retained |

Returns/skips are allowed only where explicitly listed below.

---

## 3. Creation and deduplication

A case may be requested when:

1. an effective Support Signal is `YELLOW`, `ORANGE`, or `RED`; or
2. a Veteran/Responder explicitly records a concrete coordination need.

MVP operating default remains one non-closed coordination Case per Veteran (`INFERRED`; later multi-case policy requires a spec change).

The Case carries a nullable `priority_signal_level` (0.1.4) tracking the effective Support Signal level as a queue-filter fact only ([DATA_MODEL.md](DATA_MODEL.md) §6). `APPLY_EFFECTIVE_SIGNAL` is the command that writes it from a settled signal, transcribed from [SAFETY.md](SAFETY.md) §3.2: an effective `RED` opens or updates the non-closed Case; non-RED writes nothing; a `CLOSED` Case is not reopened (see [SIGNAL_SCORING.md](SIGNAL_SCORING.md) G-I-28).

### 3.1 Atomic creation invariant

Signal/event/job delivery may be duplicated or concurrent. Therefore case creation must be idempotent against a stable **case-open intent** and must not rely on `read no case → insert` without conflict protection.

For the MVP one-active-case default:

- concurrent create attempts for the same Veteran/tenant resolve to one winning non-closed Case;
- losing/replayed attempts return/reference that existing Case when semantically compatible rather than creating duplicates;
- only the winning logical creation emits `CASE_CREATED`;
- a new signal may update case priority/history through a documented idempotent action, but is not itself permission to create a second active Case;
- database constraint/transaction/lock strategy is implementation detail, but one-winner semantics are required.

The exact future rule for multiple concurrent cases remains `FUTURE`.

---

## 4. Transitions

Every transition records source, target, actor, prerequisites, timestamps, audit, and Domain Event where defined.

| Source | Target | Actor | Prerequisites | Domain Event |
|---|---|---|---|---|
| (none) | `OPEN` | System / Responder / Veteran | Veteran enrolled; creation invariant passes | `CASE_CREATED` |
| `OPEN` | `TRIAGED` | Responder | authorized queue access | — |
| `TRIAGED` | `ASSIGNED` | Responder claim / Org-admin assign | target membership ACTIVE; atomic assignment succeeds | `CASE_ASSIGNED` |
| `OPEN` | `ASSIGNED` | Responder claim / Org-admin assign | target membership ACTIVE; atomic assignment succeeds | `CASE_ASSIGNED` |
| `ASSIGNED` | `ACTIVE` | assigned Responder | explicit `ACTIVATE` command (0.1.4); no work action implicitly activates a Case | — |
| `ACTIVE` | `FOLLOWUP` | assigned Responder | Follow-Up exists or explicit transition with documented reason | `FOLLOWUP_CREATED` only if created |
| `FOLLOWUP` | `ACTIVE` | assigned Responder | new coordination work required | — |
| `ACTIVE` | `RESOLVED` | assigned Responder | Settlement present; no blocking non-terminal Service Requests | `CASE_RESOLVED` |
| `FOLLOWUP` | `RESOLVED` | assigned Responder | blocking Follow-Ups completed/cancelled; Settlement present | `CASE_RESOLVED` |
| `RESOLVED` | `CLOSED` | assigned Responder / Org-admin | Settlement recorded; close command authorized | — |
| `ASSIGNED` | `ASSIGNED` | assigned Responder / Org-admin | atomic reassignment: release prior + create successor assignment | `CASE_ASSIGNED` |
| `ACTIVE` | `ASSIGNED` | assigned Responder / Org-admin | atomic reassignment; old assignment released | `CASE_ASSIGNED` |
| `FOLLOWUP` | `ASSIGNED` | assigned Responder / Org-admin | atomic reassignment when follow-up ownership changes | `CASE_ASSIGNED` |
| `ASSIGNED` | `ACTIVE` | assigned Responder | `ESCALATE` with reason; case remains assigned and active | `CASE_ESCALATED` |
| `ACTIVE` | `ACTIVE` | assigned Responder | `ESCALATE` with reason | `CASE_ESCALATED` |
| `FOLLOWUP` | `ACTIVE` | assigned Responder | `ESCALATE` with reason; new active work required | `CASE_ESCALATED` |

### 4.0 Case commands (0.1.4)

The named case commands are `TRIAGE`, `CLAIM_CASE`/`ASSIGN_CASE`, `ACTIVATE`, `ESCALATE`, `RESOLVE`, `CLOSE`, and `REOPEN`. `ACTIVATE` is the only edge from `ASSIGNED` to `ACTIVE`: activation is always an explicit command, never an implicit side effect of recording work.

### 4.1 Escalation correction

`ESCALATE` is **not** a universal state jump from any non-terminal state. An unassigned `OPEN`/`TRIAGED` case cannot be escalated by an "assigned Responder" because no such assignment exists.

For unassigned high-priority cases, queue priority/Org-admin assignment is the mechanism. A future explicit unassigned escalation action requires its own accepted transition.

### 4.2 Reopen

`CLOSED` → `OPEN` is the only reopen edge (0.1.4): a `RESOLVED` Case is closed before it can be reopened into a new resolution cycle, so there is no `RESOLVED → OPEN` edge. It is allowed only through a documented reopen command by an authorized owning-org actor or SUAS-admin break-glass path with reason and audit. Prior Settlement/history remain immutable; resolution of the reopened cycle requires a new Settlement record/linkage as later data-model semantics specify.

---

## 5. Atomic assignment and claim

`CLAIM_CASE` and exclusive `ASSIGN_CASE` are contested commands.

Required semantics:

1. The command carries/derives expected current state and assignment condition.
2. The state/assignment check and winning assignment write occur atomically.
3. Exactly one contender wins when exclusive ownership applies.
4. A loser receives a conflict (`409` or equivalent contract error) with no partial assignment/event.
5. Idempotent replay by the same logical command returns the original winning result rather than creating another CaseAssignment.
6. `CASE_ASSIGNED` is emitted once per logical assignment/reassignment.
7. Reassignment releases the prior active assignment and creates the successor in one transaction/equivalent atomic unit.

Queue read freshness is advisory; authorization/claim validity is always re-checked at mutation time.

---

## 6. Notes, requests, follow-up

- Case Note is not a transition, Follow-Up, or Contact Attempt.
- Contact Attempts use documented contact commands.
- Service Requests are distinct child work items.
- Follow-Ups are first-class.
- Escalation is an explicit command with reason; no note keyword changes state.

---

## 7. Resolution and closure

- `RESOLVED` requires a Settlement.
- Blocking Service Requests/Follow-Ups must satisfy the documented terminal rules. A Service Request **blocks** Case resolution iff its status is **not** one of the terminal statuses `{CLOSED, CANCELLED, EXPIRED, UNFULFILLABLE}` (0.1.4); a request in any other status (including `CONFIRMED`, which is non-terminal for this rule) still blocks resolution.
- `CLOSED` retains all history.
- Signal returning `GREEN` does not auto-close a Case.
- Generative AI must not determine resolution/closure.
- Resolve/close commands are idempotent and stale-state protected; duplicate delivery cannot create duplicate Settlement/closure effects.

---

## 8. Authorization and visibility

- Assigned Responder: documented read/write actions.
- Org queue Responder: bounded limited fields for unassigned cases in same tenant.
- Trusted Contact: explicit grants only.
- SUAS-admin access is audited and does not imply routine workflow ownership.

### 8.1 Veteran visibility (D-015 `DECIDED`, v0.1.0)

Veteran can see own:

- Check-Ins;
- Service Request status;
- Settlement fields written for them;
- addressed Follow-Up prompts;
- Support Case existence/status.

Veteran cannot see:

- full Case Notes;
- Contact Attempts;
- other veterans;
- responder queue internals;
- other organizations/tenants.

---

## 9. Queue/scaling requirements

Responder queues must be bounded/paginated. Priority sorting/filtering must not require loading every Case into application memory.

Queue queries may be stale between read and action; mutation-time checks remain authoritative.

At minimum, queue access paths support tenant + status + priority + assignment ownership, with exact physical indexes validated later under SPEC-006/SPEC-010.

---

## 10. Non-goals

- EHR charting;
- hidden state values;
- deleting Cases for cleanup;
- auto-close on `GREEN`;
- non-atomic claim/assignment;
- treating queue visibility as a lock;
- creating duplicate Cases from duplicate signal/event delivery;
- impossible unassigned `OPEN → ACTIVE` escalation.

---

## 11. Testability

Critical suite: **case transitions/concurrency**.

- only documented edges succeed;
- concurrent Case creation under one-active-case policy yields one logical Case/`CASE_CREATED`;
- concurrent `CLAIM_CASE` yields one winner and conflicts for losers;
- replayed winning claim is idempotent;
- reassignment atomically releases old and creates new assignment;
- unassigned `OPEN`/`TRIAGED` cannot use assigned-responder escalation path;
- resolve without Settlement fails;
- duplicate resolve/close commands do not duplicate effects;
- closure retains history;
- veteran cannot read Case Notes/Contact Attempts;
- queue never crosses tenant boundary.
