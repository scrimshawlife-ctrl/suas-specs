# Dashboard numbers on web, iOS, and Android

**Stack:** `0.6.0`  
**Parents:** [MVP_REFERENCE.md](MVP_REFERENCE.md) §9, [ANALYTICS.md](ANALYTICS.md)  
**Still open:** D-025 (how small counts are hidden)

A label on a dashboard is not a metric. A metric needs a numerator, a denominator when it is a rate, a time window, source events, and who can see it ([ANALYTICS.md](ANALYTICS.md) §2).

Those definitions do not exist yet for `Responses`, `Rating`, `This Month`, or `Avg Response`.

| Client | What may appear |
|---|---|
| Web `/app/responder` | The labels. The value is `NOT_COMPUTABLE` / no released definition. Not `0`. |
| iOS / Android responder screens | Same labels if the screen exists. Same missing-definition text. |

Do not print stars, monthly totals, “lives saved,” or a QRF success rate built from assignment or notification alone. Do not ship a JSON metrics route that returns zeros. Do not turn on `D025_REPORTING`. Do not scrape the web dashboard from a phone.

Veteran home does not grow a scoreboard. Support Signal labels are coordination labels, not a clinical score.
