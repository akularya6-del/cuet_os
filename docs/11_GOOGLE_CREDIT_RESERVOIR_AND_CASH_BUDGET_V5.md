# 11_GOOGLE_CREDIT_RESERVOIR_AND_CASH_BUDGET_V5

**Finite capital, dated.** Account A currently has **₹18,887.70 remaining from a ₹28,320.75 Free Trial and expires 2026-10-02 [USER-PROVIDED CONSOLE SCREENSHOT VERIFIED 2026-09-09]**. Account B is deliberately deferred until 2026-12-07; its balance, activation, terms, and expiry remain **[UNKNOWN]**. This file defines verification, allocation, burn discipline, the reservoir modes, and the $55 cash answer.

---

## 1. Two-account policy (A/B)

| Rule | Content |
|---|---|
| A = PRIMARY (ACTIVE NOW) | first-party Gemini inference and durable batch outputs through Vertex. **[USER-PROVIDED CONSOLE SCREENSHOT VERIFIED 2026-09-09] ₹18,887.70 remaining; expires 2026-10-02.** |
| B = DEFERRED | Do not request or use Account B before 2026-12-07 unless Account A becomes unusable and the human says B is necessary. Balance, activation, terms, and expiry are **[UNKNOWN]**. |
| Never pool | credits are per-billing-account; no technical "pooling" exists. The current dispatcher rejects Account B until its human review. |
| Never co-mingle identity | each account stays its own billing + project + org structure; shared credit cards only where Google requires (pay attention to which card is on file — a trial that converts could bill it) |
| Legality note | Google's Free Trial terms cover first-party Google Cloud AI use but exclude Gemini API usage through AI Studio and third-party managed generative-AI partner models **[OFFICIAL VERIFIED 2026-09-09]**. Account B is not treated as available before its scheduled verification. |
| Quotas | per-project quotas are separate [INFERENCE from per-project rate-limit structure — VERIFY in console]; failover thus also buys quota headroom |
| Security | separate projects prevent one bad experiment from billing both; IAM: owner-only; no service-account keys in the repo |

## 2. Verification procedure (run once, then monthly)

1. Console → Billing → **Credits** per account: type (trial/welcome vs promotional), amount remaining, **expiration date**. Record into `memory/ledgers/credit_ledger.csv` with tag [OFFICIAL VERIFIED date].
2. Confirm which SKUs the credit covers (trial credits apply to most Vertex usage; some promotional credits are SKU-restricted — test with a ₹1-scale call and read the invoice line).
3. Confirm Vertex (Agent Platform) usage actually draws from credit, not the card: billing report after first test call.
4. Record project IDs, region choices (choose one primary region for data residency + quota simplicity), and per-model quotas seen in the console.
5. Set billing budget alerts at 50/80/100% of expected monthly burn AND a hard spending cap where supported (guards against four-figure surprise invoices — V4 recorded a community four-figure overnight Vertex bill [TIER C 2026-04-30]; **the ledger is the real cap**, Google's are late).

## 3. Current spend-down schedule

Account A is the only verified reservoir. Account B is outside the active plan until 2026-12-07.

| Phase | Window | Active capital | Mission |
|---|---|---|---|
| P1 Front-load | now → 2026-10-02 | A: ₹18,887.70 observed remaining | spend only on score-bearing durable assets: validated question batches, source extraction, study guides, and evaluation sets; target low residue without displacing study time |
| P2 Account-B review | 2026-12-07 | B: [UNKNOWN] | ask once for activation/status, balance, expiry, SKU scope, project, region, and alerts; no earlier assumptions |
| P3 Final stretch | after Account-B review → exam (~May 2027 [UNKNOWN until NTA]) | [UNKNOWN] | route from verified facts available at that time; do not pre-spend or pre-allocate Account B |

No Account-B contingency is made before 2026-12-07. Account A cannot be reserved beyond its verified 2026-10-02 expiry.

## 4. Reservoir policy (tiers and modes)

```
FREE QUOTA (NotebookLM, Gemini free tier, Groq, OpenRouter-free, Codex cached search)
→ SUBSCRIPTION QUOTA (Codex Plus windows: orchestration, verification, interactive)
→ GOOGLE CREDIT (Vertex: first-party Gemini volume and batch compute)
→ CASH API (DeepSeek, OpenRouter paid, Anthropic API)  ← gated by §7
→ EMERGENCY RESERVE (floor tools + deferred work)
```

| Mode | Trigger | Behavior |
|---|---|---|
| NORMAL | credit burn ≤ $15/mo AND >60% balance left | default allocations (03 §3) |
| EXPIRING | verified expiry ≤30 days and balance ≥30% | front-load score-bearing durable assets; avoid residue, but never displace study blocks or weaken validators |
| HEAVY | burn >$15/mo OR balance 30–60% | T2 volume shifts to free floor; T4 on credits requires explicit one-line justification; weekly burn review |
| PEAK | balance <30% OR sprint phase | credits only for T5/T6 gates and sprint-critical batch; everything else free/subscription |
| EMERGENCY | credits exhausted/expired OR billing frozen | free floor + subscription only; deferred-work queue; §7 cash gate drops to its strictest reading |

## 5. Ledger and forecast (deterministic)

`credit_ledger.csv` rows include native currency, balances, delta, expiry, engine, task reference, and evidence tag. `ledger.py credit` is the single append path; `router.py` computes mode without summing currencies and prioritizes verified near-expiry credit. A separate nightly `credit_audit.py` remains unimplemented and must not be scheduled. Current Vertex prices and evidence dates live in `config/budget.json`; source provenance is in `research/sources/`.

## 6. What credits CAN and CANNOT buy

CAN: first-party Gemini inference through Vertex, Vertex batch prediction, and modest Agent Platform compute when a real managed-agent need exists. CANNOT under the observed Free Trial terms: Gemini API charges through AI Studio and third-party managed generative-AI partner models such as Claude-on-Vertex **[OFFICIAL VERIFIED 2026-09-09]**. Anthropic API direct, OpenAI API, DeepSeek, and OpenRouter also remain outside Google credit. Cross-family verification therefore stays disabled until a separately eligible funding path is verified and approved.

## 7. The $55 cash question (definitive V5 answer)

The envelope is **$55/month hard ceiling — a gated reserve, not a budget**. Planned spend by regime:

| Regime | Typical cash/month | Composition |
|---|---|---|
| Credits active (now → expiry) | **$0–9** | DeepSeek off-peak overflow (~$1–3), FX/billing rounding, retry float; one-time $10 OpenRouter if not yet spent |
| Credits exhausted (post-expiry) | **$15–35** | DeepSeek primary volume + paid Gemini Flash tier + occasional Anthropic-API verification; only if free floor proves insufficient |
| Peak/sprint with credits | $0–15 | credits carry sprints; cash only for emergency overflow |
| Emergency/provider-failure month | up to $55, one-time, gated | restore continuity; post-month review must explain every dollar |

Gates (unchanged from V4, still mandatory): any non-recurring cash ≥$10 requires the **buy-nothing check** (free floor + subscription + credits cannot do it) + explicit human approval in-chat; recurring additions require a monthly-review vote; **$55 is a defect line, not a target** — crossing it triggers a red-team note (13 §2-A14) and an automatic simplification proposal. GLM subscription stays retired (re-subscribe triggers: HEAVY-month GLM API >$15 or Antigravity Gemini cuts >2 weeks).

## 8. Spend-down discipline (compounding-assets doctrine)

Credits buy durable things first: question bank, extracted-and-verified sources, study guides, evaluation suites (15 §4), baseline mock analytics. Credits do NOT buy: chit-chat reasoning, redundant second opinions outside gates, formatting work scripts can do, exploration without a VOI line. If the projected depletion date arrives earlier than planned usage, cut volume — never move cash spending up to compensate (cash is the longer-lived reserve; credits are the perishable one).
