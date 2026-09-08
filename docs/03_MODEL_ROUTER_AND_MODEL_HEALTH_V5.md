# 03_MODEL_ROUTER_AND_MODEL_HEALTH_V5

**The routing law.** Goal: the user almost never picks a model. The router picks, explains itself in one line, and is allowed to say "no model needed."

---

## 1. The seven routing tiers

| Tier | Name | Engines | Typical cost | Examples |
|---|---|---|---|---|
| T0 | NO MODEL / SCRIPT | `scripts/*.py`, templates, NotebookLM search | ₹0 | score math, ledger updates, spaced-repetition scheduling, log appends |
| T1 | FREE TOOL | NotebookLM, AI Studio free tier, Groq free, OpenRouter free, Codex cached web search | ₹0 | source lookups, flashcard seeds, quick fact checks |
| T2 | CHEAP MODEL | DeepSeek V4 Flash (off-peak $0.22/$0.66 per 1M [OFFICIAL 2026-09-08]), Gemini Flash via free tier (promo to 2026-12-31 [OFFICIAL]), GLM Flash, Qwen Flash | ≤ $0.005/task | question bulk generation, classification, tagging, summaries, error clustering |
| T3 | WORKHORSE (in-Codex) | Codex default profile (medium effort) | subscription quota | interactive explanation, code edits, routing judgment, verification |
| T4 | STRONG (gated) | Codex heavy profile (xhigh), Gemini 3.x Pro via Vertex credits, GPT-6-Astra-class | credits or heavy quota | mock post-mortems, weekly strategy synthesis, hard concept plans |
| T5 | PREMIUM ADJUDICATION | Claude Sonnet 5 / Opus 5 (Anthropic API cash **or Vertex credits** [OFFICIAL: Claude on Google Cloud, docs 2026-09-03]), GPT-6 Astra | gated (§7) | canonization, red-team finals, contested answers |
| T6 | MULTI-MODEL PANEL | T2/T3/T5 arms from ≥2 different families | gated (§7) | strategy pivots, syllabus/rule changes, model migrations |

## 2. Router inputs (collected by `scripts/router.py` — deterministic)

task_type · importance (1–5) · complexity (1–5) · uncertainty (1–5) · reversibility (R/H) · data sensitivity class (13 §4) · expected token volume · latency tolerance · remaining quotas (Codex `/status` posture, Gemini free-tier day count, DeepSeek day budget) · credit balances (credit_ledger) · cash spent this month (cash_ledger) · model health flags (health.json) · expected score impact (0–10, user or heuristic) · current reservoir mode (11 §4: NORMAL/HEAVY/PEAK/EMERGENCY).

Output: JSON `{tier, engine, profile, reason, est_cost_usd, gate_required}` + one-line human reason. Codex **executes the recommendation** unless the human overrides (override is logged).

## 3. Default routing per task family (the 80% table)

| Task | Route |
|---|---|
| Morning check-in, STATE review | T0 scripts + T3 (≤2 K tokens) |
| Log a study block | T0 only |
| Generate 20 drill questions | T2 bulk (DeepSeek off-peak) + T0 validators |
| Validate/repair generated questions | T0 structural → T3 spot-check 5–10% |
| Explain one concept | T3 first; T4 only after 2 failed attempts to land |
| Score a mock | T0 (scorer) + T2 (error classification) + T4 (interpretation, weekly batch) |
| Research a claim | T1 capture + T2 extraction + T3 synthesis + T5 only on canonization |
| Weekly review | T3 + T4 (1×, gated) |
| Red-team pass | T6 panel (13 §3) |
| Anything during PEAK/EMERGENCY | freeze T2 premium volumes; T0/T1 always allowed |

## 4. The shell boundary (V5's cost law, restated operationally)

If a task's output is data (JSON/CSV), it runs as `python scripts/<task>.py` calling a T2/T1 API — never as in-Codex generation — UNLESS volume ≤ 5 items or latency < 10 s matters. Codex reads only the summary. Rationale: Codex Plus quota is a 5-hour/weekly window with no published number [OFFICIAL VERIFIED]; DeepSeek off-peak is ~285× cheaper per output token than Opus-class API [ESTIMATE from official prices, 2026-09-08]; every in-Codex token spent on bulk is a token unavailable for orchestration and verification, which are the actual bottleneck skills.

## 5. Task-value governor (MCV, carried from V4 — the arithmetic is unchanged)

`MCV = TASK VALUE (0–10) × UNCERTAINTY (1–5) × ERROR COST (1–5) × REVERSIBILITY (0.5 reversible / 1 hard) × EXPECTED SCORE IMPACT (0–10)`

| MCV | Decision |
|---|---|
| < 20 | T0–T2 only |
| 20–47 | T3 (workhorse) |
| 48–99 | T4 allowed, name the trigger in one line |
| 100–199 | T4 default; T5 if disagreement material |
| ≥ 200 | T6 panel; human informed before spend |

Worked examples:
- "Generate 30 quadratic MCQs" → value 6 × unc 2 × err 2 × rev 0.5 × imp 6 = **72** → but output is data → shell boundary → T2 bulk + validators (T4 sample check ≤10%).
- "Decide whether to switch PE prep strategy" → 8 × 4 × 5 × 1 × 8 = **1280** → T6 panel, gated, human approves.
- "Fix a typo in a drill" → **< 10** → T0/no model.

## 6. Escalation triggers (E1–E6, carried from V4, re-anchored)

E1 structural validator fails twice on generated content → escalate one tier. E2 two engines disagree materially on a factual/strategic answer → adjudicate (T5). E3 repeated user confusion on one concept after 2 explanations → T4 with full ACADEMIC pack. E4 mock section regression ≥ 10 marks vs trailing mean → T4 interpretation same evening. E5 research claim contested or stale → T5 canonization. E6 model health flag (§8) on the assigned engine → reroute around it.

De-escalation is equally mandatory (the "AI can refuse" rule): if memory, scripts, NotebookLM, or the official source suffice, the router answers **NO MODEL** and says so.

## 7. Multi-model / premium gates (no-redundancy law)

Multi-model runs require ALL of: (a) uncertainty is material (answer hard to verify deterministically), (b) stakes high (strategy, canon, mock interpretation), (c) disagreement would change an action, (d) independent-check value > cost+time. Otherwise: cheapest competent path. Premium cash spend additionally requires the 11 §7 gate (buy-nothing check + monthly cap + human approve). **Anti-echo-chamber amendment for V5:** panels judging Codex-produced work must include ≥1 non-OpenAI arm; Codex never sits on a panel evaluating its own output (04 §5).

## 8. Model health ledger

`models/health.json` tracks per engine: availability (%), p50 latency, tool-call success rate, format-error rate, hallucination incidents (logged), quota posture, price-as-of, deprecation risk. Updated by: bootstrap_check (daily, cheap probes only — T1 ping or scripted 1-token call), run logs (auto-append on failure), and the weekly review (human confirms). Route-around rule: 2 failures in 7 days on one engine → router marks it `degraded` and prefers alternates for a week; `degraded` engines cannot serve T4/T5 without human override. Deprecation watch = 15 §5 triggers.

## 9. Failure ladder (when the routed engine fails)

L1 retry once with same engine (transient). L2 switch engine within same tier (Flash↔GLM Flash↔Qwen Flash; free-tier↔free-tier). L3 drop one tier and degrade scope (fewer items, smaller pack). L4 Codex in-process fallback for small jobs only (≤ 10 items) — spend quota consciously. L5 defer to nightly batch (off-peak window) or to tomorrow's START. L6 report to human + log to model_health. The ladder never skips validators, never writes unvalidated content to bank/, and never exceeds budget gates.

## 10. Router learning (from outcomes, not vibes)

Every T4+ run and every T2 batch appends `{engine, task_type, tokens, cost, validator_result, rework_needed}` to token_ledger. Monthly, `scripts/router_report.py` computes **successful-output-per-rupee and per-minute** by engine×task. Decision rules (examples the data can trigger): if engine A costs 5× engine B for ≤3% validator-quality gain and no academic delta → default demotes A; if B cuts major-error rate materially → promote B. Changes to the default table itself are governance (12 §4) — proposal, test week, human approval.
