# 11_GOOGLE_CREDIT_RESERVOIR_AND_CASH_BUDGET_V5

**Finite capital, dated.** $599 across two Google accounts is the project's compute endowment, running as a time-based relay: **A = $299, expires ~2026-12-07; B = $300, activates ~2026-12-07 [USER VERIFIED 2026-09-08]**. This file defines verification, allocation, burn discipline, the reservoir modes, and the $55 cash answer.

---

## 1. Two-account policy (A/B)

| Rule | Content |
|---|---|
| A = PRIMARY (ACTIVE NOW) | daily Vertex usage: Gemini 3.x inference, Claude-on-Vertex verification runs, batch extractions. **[USER VERIFIED 2026-09-08] $299 balance, expires ~2026-12-07 (90-day life)** |
| B = RELAY RESERVE (DORMANT) | **[USER VERIFIED 2026-09-08] $300, activates ~2026-12-07** — becomes active primary on activation day (time-based relay, not a 70%-balance trigger); if A fails early, promote B immediately. B's own expiry: **[UNKNOWN → record on activation day]** |
| Never pool | credits are per-billing-account; no technical "pooling" exists; routing alternates accounts only via config switch (`scripts/dispatch.py --account B`), never mid-batch |
| Never co-mingle identity | each account stays its own billing + project + org structure; shared credit cards only where Google requires (pay attention to which card is on file — a trial that converts could bill it) |
| Legality note | Google's Free Trial = $300 / 90 days per new billing account [OFFICIAL cloud.google.com/signup-faqs]; the user's stated A/B facts match this shape exactly. **[USER VERIFIED 2026-09-08]** that B activates ~90 days out — on activation day still confirm B's credit type, SKU coverage, and terms; if verification shows any doubt, B's spend stays minimal and the plan reverts to A-only economics extended via §7. Flagged as a standing risk in 13 §2-A5 |
| Quotas | per-project quotas are separate [INFERENCE from per-project rate-limit structure — VERIFY in console]; failover thus also buys quota headroom |
| Security | separate projects prevent one bad experiment from billing both; IAM: owner-only; no service-account keys in the repo |

## 2. Verification procedure (run once, then monthly)

1. Console → Billing → **Credits** per account: type (trial/welcome vs promotional), amount remaining, **expiration date**. Record into `memory/ledgers/credit_ledger.csv` with tag [OFFICIAL VERIFIED date].
2. Confirm which SKUs the credit covers (trial credits apply to most Vertex usage; some promotional credits are SKU-restricted — test with a ₹1-scale call and read the invoice line).
3. Confirm Vertex (Agent Platform) usage actually draws from credit, not the card: billing report after first test call.
4. Record project IDs, region choices (choose one primary region for data residency + quota simplicity), and per-model quotas seen in the console.
5. Set billing budget alerts at 50/80/100% of expected monthly burn AND a hard spending cap where supported (guards against four-figure surprise invoices — V4 recorded a community four-figure overnight Vertex bill [TIER C 2026-04-30]; **the ledger is the real cap**, Google's are late).

## 3. The verified relay schedule (the decisive facts are now known)

**[USER VERIFIED 2026-09-08]: A = $299, expires ~2026-12-07. B = $300, activates ~2026-12-07.** This resolves the V4 expiry unknown into a clean time-based relay:

| Phase | Window | Active capital | Mission |
|---|---|---|---|
| P1 Front-load | now → ~2026-12-07 | A: $299 | spend-down on compounding assets: question bank to ≥3,000 validated Qs, source extraction, study guides, eval suites; burn ceiling ≈ $3.2/day; target near-zero residue by ~Dec 1 (no hoarding — B arrives on schedule) |
| P2 Mock-season premium | ~2026-12-07 → B's expiry | B: $300 | premium mock post-mortems, cross-family adjudication, Agent Platform experiments; **first task on activation day: record B's exact expiry + SKU test into credit_ledger.csv** |
| P3 Final stretch | B's expiry → exam (~May 2027 [UNKNOWN until NTA]) | none | free floor + Codex subscription + §7 gated cash; by design exam-month compute is minimal (scripts + free tier) because durable assets were already built |

Two contingencies remain: (a) **B late or fails activation** → P1 discipline extends: A's last 20% becomes the Jan–Feb verification reserve and the §7 cash gate governs the gap; (b) **B carries a second 90-day clock** (would end ~2027-03-07) → acceptable: March-on mocks are analysis-light (scorer.py + subscription), premium adjudication ends with B. Expiry dates re-checked monthly and staring at the user from `BUDGET` output every week.

## 4. Reservoir policy (tiers and modes)

```
FREE QUOTA (NotebookLM, Gemini free tier, Groq, OpenRouter-free, Codex cached search)
→ SUBSCRIPTION QUOTA (Codex Plus windows: orchestration, verification, interactive)
→ GOOGLE CREDIT (Vertex: Gemini volume, Claude-on-Vertex verification, batch compute)
→ CASH API (DeepSeek, OpenRouter paid, Anthropic API)  ← gated by §7
→ EMERGENCY RESERVE (floor tools + deferred work)
```

| Mode | Trigger | Behavior |
|---|---|---|
| NORMAL | credit burn ≤ $15/mo AND >60% balance left | default allocations (03 §3) |
| HEAVY | burn >$15/mo OR balance 30–60% | T2 volume shifts to free floor; T4 on credits requires explicit one-line justification; weekly burn review |
| PEAK | balance <30% OR sprint phase | credits only for T5/T6 gates and sprint-critical batch; everything else free/subscription |
| EMERGENCY | credits exhausted/expired OR billing frozen | free floor + subscription only; deferred-work queue; §7 cash gate drops to its strictest reading |

## 5. Ledger and forecast (deterministic)

`credit_ledger.csv` rows: date, account, balance_before, delta, engine, task_ref, evidence tag. `scripts/credit_audit.py` (nightly + on `BUDGET`): burn/week by account and engine, projected depletion date (linear + sprint-weighted), expiry-adjusted usable balance, mode recommendation, alert lines for STATE.md. Cost table lives in `config/budget.json` with per-token prices **each carrying an as-of tag** (15 §2): Gemini 3 Pro $2/$12 ≤200K ctx [TIER B 2026]; 3.1 Pro $4/$18 >200K [TIER B]; Claude Sonnet 5 $2/$10, Opus 5 $5/$25 [TIER A 2026-09-06]; DeepSeek V4 Flash $0.22/$0.66 off-peak [OFFICIAL 2026-09-08]. FX ₹94.5/USD [VERIFIED 2026-09-06]; recheck monthly (W14).

## 6. What credits CAN and CANNOT buy

CAN: Gemini API/Vertex inference; **Claude models via Vertex Model Garden** [OFFICIAL 2026-09-03] — the V5 unlock that keeps the verifier pattern nearly free; open/partner models in Model Garden; Vertex batch prediction; modest Agent Platform compute. CANNOT: Anthropic API direct, OpenAI API, DeepSeek, OpenRouter (all external — cash only). Design consequence: cross-family verification migrates to Vertex-Claude; cash is preserved for the deep reserve.

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
