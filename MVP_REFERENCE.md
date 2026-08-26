# MVP_REFERENCE.md — Visual and interaction reference contract (SUAS v0.1)

**Lifecycle:** `released` via [RELEASE_MANIFEST-0.3.0.md](RELEASE_MANIFEST-0.3.0.md). The former inline `draft` / `0.1.0` marker was stale; the manifest governs ([VERSIONING.md](VERSIONING.md) §1).  
**Reference MVP:** `https://suasqrf.org/app/` (current public reference surface; public crawl also resolves the deployed MVP content through its current host).  
**Reference observation date:** 2026-08-18 PT.  
**Related:** [PRODUCT.md](PRODUCT.md), [ONBOARDING.md](ONBOARDING.md), [RESPONDER_WORKFLOWS.md](RESPONDER_WORKFLOWS.md), [RESOURCES.md](RESOURCES.md), [AUTH.md](AUTH.md), [SAFETY.md](SAFETY.md), [CONSENT.md](CONSENT.md), [PRIVACY.md](PRIVACY.md), [TESTING.md](TESTING.md), [STATUS.md](STATUS.md)

---

## 1. Purpose

The existing SUAS MVP is the production **visual and interaction reference**. Production must preserve its recognizable product identity, action-first hierarchy, principal navigation, responder/QRF immediacy, and low-friction mobile feel unless a canonical production constraint requires a documented divergence.

The reference is not source-code authority and does not override authentication, consent, privacy, safety, accessibility, provider truth, or canonical domain semantics.

When prototype behavior conflicts with an accepted specification, the accepted specification wins and production implements the closest truthful/safe interaction equivalent.

---

## 2. Conformance classes

| Class | Meaning |
|---|---|
| `MUST_MATCH` | Preserve recognizable hierarchy, role, placement importance, and visual/product identity; not pixel equality |
| `MUST_PRESERVE_BEHAVIOR` | Preserve the user goal and recognizable interaction sequence while production semantics/copy may change |
| `MAY_EVOLVE` | May improve without changing product intent or creating cognitive overload |
| `MUST_CHANGE_FOR_PRODUCTION` | Prototype behavior/copy conflicts with canonical auth/safety/privacy/accessibility/domain/truthfulness rules |

No required element may silently disappear.

---

## 3. Observed MVP interaction spine

The observed reference includes these recognizable surfaces/actions, which production must account for explicitly:

1. **Brand/mission opening** followed by an immediate `TAKE ACTION` section.
2. **Role selection / Join the Mission** with Veteran vs Responder/Peer Counselor identity.
3. Two primary actions: **`I NEED SUPPORT`** and **`I WANT TO SERVE`**.
4. Veteran support surface with **QRF deploy** as the dominant action.
5. Immediate resource block placed above/before broader resource categories.
6. Category cards visually including **Housing, Food, Counseling, Transportation, Activities, Job Training**.
7. QRF searching/deploying state with visible progress, **Call**, **Message**, and **Cancel** affordances.
8. **QRF Dashboard** with on-duty state, response metrics, Quick Resource Share, Alerts, Chat, and Home.
9. Persistent/simple **Home** and **Chat** navigation on operational mobile surfaces.
10. Distinct high-privilege admin overview surface.
11. Long-form local Resource screens with clear category headers, direct phone/email/web actions, and back navigation.

The production system need not preserve unsupported claims, prototype statistics, unverified individual contact data, or unsafe copy merely because they appear in the reference.

---

## 4. Visual/product principles

Production SUAS MUST preserve:

1. **Action first:** help/service choices remain visible immediately.
2. **Low cognitive load:** direct language, large action targets, short navigation paths, progressive disclosure.
3. **Human-service orientation:** not an EHR, insurance portal, or generic enterprise CRM.
4. **Fast role recognition:** Veteran, Responder/QRF, and Admin surfaces are visibly distinct.
5. **Resource immediacy:** critical help and MVP resource categories are easy to discover.
6. **Responder immediacy:** on-duty state, active needs, alerts, communication, and Quick Resource Share stay prominent.
7. **Mobile first:** no precision interactions/horizontal scrolling on critical paths.
8. **Strong operational states:** searching, pending, accepted, unavailable, degraded, cancelled, and completed states are visible and truthful.
9. **No enterprise-density drift:** production hardening must not bury the MVP under dashboards/settings.

---

## 5. Required surface inventory

| Surface | Reference anchor | Conformance |
|---|---|---|
| Landing / action surface | `TAKE ACTION`; `I NEED SUPPORT`; `I WANT TO SERVE` | `MUST_MATCH` hierarchy |
| Enrollment / role selection | Join the Mission; Veteran vs Responder | `MUST_PRESERVE_BEHAVIOR`; auth copy may change |
| Veteran support home | QRF dominant action + Immediate Resources + categories | `MUST_MATCH` hierarchy |
| QRF deploy/request flow | tap/deploy → searching/pending → contact/cancel | `MUST_PRESERVE_BEHAVIOR`; semantics change as §7 |
| Immediate resources | crisis/help resources above general catalog | `MUST_MATCH` placement role; copy governed by SAFETY/D-012 |
| Resource categories | Housing/Food/Counseling/Transportation/Activities/Job Training visual grid/list | `MUST_MATCH` recognizable category surface; operational mapping in §6 |
| Resource list/detail | category heading + direct contact actions + back nav | `MUST_PRESERVE_BEHAVIOR` |
| Responder/QRF dashboard | on-duty state, active-work emphasis, Quick Resource Share | `MUST_MATCH` operating emphasis |
| Responder availability | on-duty/readiness state | `MUST_PRESERVE_BEHAVIOR` |
| Active needs / alerts | alerts/current work | `MUST_PRESERVE_BEHAVIOR`; canonical Case/Request state applies |
| Chat / communication | persistent Chat entry | `MUST_PRESERVE_BEHAVIOR`; visibility/consent applies |
| Persistent mobile nav | Home + Chat simplicity | `MUST_MATCH` navigation simplicity |
| Admin overview | distinct privileged overview | `MAY_EVOLVE`; role/tenant scope must become clearer than prototype |

---

## 6. Category/display mapping

User-facing labels may preserve familiar MVP vocabulary while canonical product state stays exact.

| Reference label | Canonical behavior |
|---|---|
| Food | operational `FOOD` Service Request/Resource capability |
| Transportation | operational `TRANSPORTATION` |
| Housing | operational MVP action only when it means temporary `SHELTER`; permanent `HOUSING` workflow remains `FUTURE` |
| Peer/QRF / Human Support | operational `PEER_SUPPORT` |
| Counseling | `HEALTHCARE_NAVIGATION`/clinical-adjacent workflow remains `FUTURE`; may be `COMING_SOON`/information-only, not hidden operational Service Request |
| Activities / Community | `COMMUNITY` remains `FUTURE`; may preserve an informational/community-resource card without creating a canonical Service Request or pretending COMMUNITY is released |
| Job Training | future/unreleased; may remain visibly `COMING_SOON`/information-only |

A reference card may remain for visual continuity while being explicitly non-operational. Display continuity is not permission to create an unreleased domain category.

---

## 7. Mandatory production divergences

### 7.1 Enrollment copy

Prototype language implying **“No email”** conflicts with the current passwordless identity contract.

Production must:
- preserve short, low-friction role/enrollment flow;
- require the configured email and/or phone channel needed by [AUTH.md](AUTH.md);
- not require VA API/DD-214/in-person proofing unless later specified;
- replace contradictory copy.

Class: `MUST_CHANGE_FOR_PRODUCTION`.

### 7.2 QRF deployment truthfulness

The reference tells the user to deploy the QRF and implies a nearby responder will be notified immediately.

Production must preserve the recognizable deploy/search/contact/cancel sequence, but the action means:

> create/submit an explicit `PEER_SUPPORT` need/request and attempt responder coordination according to actual coverage, availability, consent, and operations.

Production must not:
- guarantee a responder exists;
- guarantee immediate notification/contact unless the system actually knows it occurred;
- claim geographic proximity without an accepted/location-authorized basis;
- require continuous GPS;
- imply emergency-service dispatch.

Truthful states may include `REQUESTED`, `SEARCHING`, `RESPONDER_NOTIFIED`, `RESPONDER_ACCEPTED`, `NO_RESPONDER_CURRENTLY_AVAILABLE`, `DEGRADED`, `CANCELLED` as **UI labels mapped to canonical Case/Request/notification facts**, not new hidden domain states.

QRF label → canonical fact mapping (0.1.4):

| UI label | Canonical fact that backs it |
|---|---|
| `REQUESTED` | a `PEER_SUPPORT` Service Request has been created/submitted |
| `SEARCHING` | the request is in matching (or assigned without a recorded responder notification delivery) — the resting state absent a stronger fact |
| `RESPONDER_NOTIFIED` | a Notification about **this** request, addressed to the active responder, reached a sent/delivered status ([DATA_MODEL.md](DATA_MODEL.md) §9 subject reference); absent that linked delivery the surface rests on `SEARCHING` |
| `RESPONDER_ACCEPTED` | the request/assignment records responder acceptance evidence |
| `NO_RESPONDER_CURRENTLY_AVAILABLE` | matching is exhausted with no available responder |
| `DEGRADED` | a truthful degraded/no-availability operational state |
| `CANCELLED` | the request reached `CANCELLED` |

`RESPONDER_NOTIFIED` specifically requires a recorded delivery linked to the request; an assignment alone is not sufficient. `Call` and `Message` appear only when an authorized contact path actually exists.

Class: `MUST_CHANGE_FOR_PRODUCTION` semantics, `MUST_PRESERVE_BEHAVIOR` interaction.

### 7.3 Crisis / immediate-resource copy

The reference gives immediate crisis resources prominently. Preserve that placement/immediacy. Exact approved safety copy and destinations are governed by [SAFETY.md](SAFETY.md) and released by D-012 in [SAFETY_COPY.md](SAFETY_COPY.md) (v0.1.5): the authorized crisis destinations are **911** and the **988 Suicide & Crisis Lifeline** (call or text). Render that approved copy; do not treat prototype wording/statistics as accepted clinical/safety claims, and do not ship any other hotline/number/URL as official.

Crisis and practical-support surfaces also obey the state-truthfulness rule (SAFETY.md §5.1 / SAFETY_COPY.md §5): `REQUESTED ≠ ACCEPTED ≠ DISPATCHED ≠ ARRIVED ≠ RESOLVED` are distinct and a later state is shown only when its recorded fact exists (consistent with §7.2).

Class: placement `MUST_MATCH`; exact copy now `MUST_MATCH` the D-012 approved wording (previously `MUST_CHANGE_FOR_PRODUCTION` while unapproved).

### 7.4 Mission/statistic/clinical language

Reference mission/landing copy contains strong claims and clinical/suicidality framing that are not automatically canonical product claims.

Production brand can preserve urgency, service, mission, and veteran-centered directness, but must conform to [PRODUCT.md](PRODUCT.md), [SAFETY.md](SAFETY.md), and [COMPLIANCE.md](COMPLIANCE.md). Unsupported statistics/clinical efficacy claims do not become production copy through visual fidelity.

### 7.5 Admin terminology

The prototype's high-privilege admin styling may remain visually distinct. Production may replace informal labels such as “God Mode” with explicit `SUAS Admin`/`Admin` terminology to preserve least-privilege clarity and auditability.

Class: `MAY_EVOLVE` / terminology must match canonical role semantics.

---

## 8. Resource-screen fidelity

Production Resource screens should preserve:
- strong category title/header;
- county/coverage context where verified;
- scannable cards/rows;
- direct phone/email/web actions where allowed;
- clear back navigation;
- visible freshness/availability truth when known;
- mobile readability despite long lists.

Production must not hard-code reference contact facts as eternal truth. Resource data is governed by [RESOURCES.md](RESOURCES.md), verification/freshness, provider neutrality, and current configured data.

Long lists must use progressive loading/pagination/virtualization as needed without losing the reference's simple browse experience.

---

## 9. Responder/QRF dashboard fidelity

Preserve recognizable emphasis on:

1. **On Duty / availability** as a primary responder control/state.
2. Active needs/alerts as immediate work.
3. Quick Resource Share for MVP resource capabilities.
4. Chat/communication.
5. Home/simple navigation.
6. Lightweight performance/operational summaries only when derived from real data.

Prototype placeholder metrics (`Responses`, `Rating`, `This Month`, `Avg Response`) may be retained only if exact definitions/data are specified. Do not display fabricated zero/placeholder values as production facts.

The responder dashboard remains a coordination console, not a clinical chart.

---

## 10. Responsive / accessibility requirements

Production MUST meet WCAG 2.2 AA unless strengthened later, including logical reading/focus order, keyboard operation on responder/admin desktop, visible focus, non-color-only signal meaning, large touch targets, text zoom/reflow, accessible icon names, reduced-motion compatibility, and urgent actions that remain operable under zoom/mobile conditions.

Accessibility corrections are not visual drift.

---

## 11. Visual-regression fixture contract

Repeatable screenshot/reference comparison covers at least:

1. landing/action surface;
2. role/enrollment surface;
3. veteran support home;
4. QRF request/searching/pending state;
5. QRF no-availability/degraded state;
6. resource category surface;
7. resource list/detail;
8. responder dashboard/on-duty state;
9. active needs/alerts;
10. chat entry/surface;
11. admin overview;
12. mobile navigation.

Each fixture records:
- viewport/device class;
- role;
- deterministic fixture data;
- reference source/revision/observation date;
- conformance class;
- approved divergence references.

A released client surface that is not a browser extends this contract with its own device class and reuses the surface list above; it does not create a second required-surface inventory ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §7).

Review detects hierarchy drift, missing actions, excessive navigation depth/density, broken responsive behavior, misleading states, and unauthorized redesign. Pixel equality is not required.

---

## 12. UI_CONFORMANCE gate

`UI_CONFORMANCE = READY` only when:

- every required surface exists;
- reference-critical hierarchy/actions are recognizable;
- QRF deploy flow is truthful about request/availability/contact state;
- future reference categories are not silently implemented as released domain workflows;
- production divergences trace to canonical specs;
- resource data is not treated as timeless hard-coded truth;
- visual-regression fixtures pass review;
- accessibility checks pass;
- veteran/responder mobile critical paths remain low-friction.

Current: `NOT_READY`.

---

## 13. Non-goals

- pixel-perfect prototype cloning;
- copying prototype statistics/clinical claims as production truth;
- freezing CSS/framework technology;
- allowing prototype copy to override auth/safety/privacy rules;
- requiring GPS because prototype says “near you”;
- treating visual similarity as permission to create hidden domain states;
- redesigning SUAS into a generic enterprise dashboard.
