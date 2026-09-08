# 08_QUESTION_MOCK_DIAGNOSTIC_ENGINE_V5

**Where bulk AI earns its keep — and where it is forbidden.** Pipeline, validators, bank, and forecast carried from V4; execution re-bound to Codex + off-peak scripts.

---

## 1. Question pipeline (weakness → bank → retest)

```
WEAKNESS (error cluster / decay fail / new topic)
→ BLUEPRINT (Codex T3: 10–20 line spec: topic, difficulty mix, trap types, count)
→ GENERATION (T2 bulk via scripts: DeepSeek off-peak or Gemini free tier, JSON per schema)
→ L1 STRUCTURAL VALIDATION (script, 100%: schema, single correct key, distractor sanity,
   difficulty tags, no duplicated stems vs bank sha-check)
→ L2 MODEL VALIDATION (different-family engine answers blind; agreement required on key+difficulty)
→ L3 PREMIUM SAMPLE AUDIT (Codex or Claude-on-Vertex checks 5–10% random sample)
→ BANK (bank/{subject}/{topic}.jsonl, append-only, checksummed)
→ DELIVERY (drill window, timed)
→ RESULT (ledger append) → ERROR → RETEST (R1/R2 gates, 07 §6)
```

Escalation rule: L1 fail ×2 → generator prompt fixed and batch re-run (never hand-patch JSON); L2 disagreement >5% of batch → whole batch quarantined; L3 finds >2 defects in sample → batch rejected, generator demoted in `model_health` (03 §8).

## 2. Question schema (`schemas/question.schema.json`, enforced by L1)

`id · subject · topic · subtopic · type (mcq4/mcq5/assertion/arithmetic) · stem · options[4–5] · correct_index · explanation (≤80 words) · recognition_cue · difficulty (1–5) · trap_type (maps to error taxonomy E1–E10) · source (generator model+date+batch) · validation (l1, l2_engine, l3_by, timestamps) · usage history (times_served, times_correct) · status (active/quarantined/retired)`.

## 3. Quality law

No question reaches delivery without L1 100% + L2 pass. Explanation mandatory (wrong-option reasons for difficulty ≥3). No AI-generated question is ever used to *assess* mastery unless it passed L2 — banks can contain defects; assessments may not inherit them. Quarantine (`bank/_quarantine.jsonl`) holds rejects with reason codes for 7 days (fix/retag/retire), then auto-retires. Bank integrity: `scripts/bank_audit.py` (weekly) — duplicate-stem hash scan, trap-type distribution vs exam blueprint, difficulty histogram, stale-usage report.

## 4. Economics (measured, tagged)

Per-question cost ≈ $0.0002–0.0031 (V4 measurement basis; recompute monthly from token_ledger). At off-peak DeepSeek Flash ($0.22/$0.66 per 1M [OFFICIAL 2026-09-08]), 1,000 questions ≈ $0.40–0.80 [ESTIMATE — verify on first bill]. Batch runs: nightly 22:30–23:30 IST (off-peak), weekend afternoons (off-peak, all day Sat/Sun). Gemini free tier absorbs overflow until its promo ends 2026-12-31 [OFFICIAL ai.google.dev]; after that, overflow goes to paid Gemini-with-credits (Vertex) — still $0 cash.

## 5. Mock pipeline (Saturday cadence in P3; monthly before that)

```
MOCK (human-only sitting, official timing, no AI, phone away)
→ deterministic scoring: scripts/scorer.py (+5/−1 from marking_scheme.json; per-section splits,
   attempt/accuracy/question-rate) — SCORE IS COMMITTED IN 60 SECONDS, ZERO AI
→ error extraction: per-question codes (student marks E-codes on the sheet; scorer validates
   codes vs correct/attempt matrix)
→ cheap classification (T2: groups errors, finds trap patterns vs bank trap_type)
→ pattern analysis (Codex T4, ONE run, same evening or next morning: interpretation,
   intervention proposal, timing-strategy check)
→ premium adjudication ONLY if section moved ≥10 marks vs trailing mean or T4 is uncertain (03 §6 E4)
→ intervention (content fix via 07, procedure fix via checklist, or pacing fix)
→ RETEST of failed items after 48h (gate: ≥80% on retest to close the loop)
→ FORECAST update
```

**Forecast formula (carried from V4):** `forecast = 0.5·last + 0.3·prev + 0.2·prev2` per section, band = ±1σ of last 5 mocks, clamped ±15 per update. Forecast lives in `memory/ledgers/mock_results.jsonl`; the band — not the point estimate — drives decisions. One bad mock changes nothing by itself (12 §3); two consecutive out-of-band lows trigger a T6 panel before any strategy change.

## 6. Mock-day UX (AI integrity rules)

- **BEFORE** (Friday evening): Codex prints timing plan, OMR checklist, gear list; freezes all reminders for the window. **DURING**: AI silent; no smart devices at the desk; the OS treats the sitting as sacred — any AI use voids the mock's diagnostic value and is logged as a violation. **AFTER** (same minute): photograph/transcribe answers; run `scorer.py`; user sees score + section split immediately (instant feedback, honest numbers). **EVENING**: rest or light review only; heavy analysis is forbidden same-evening (emotional distortion). **OVERNIGHT**: T2 classification + T4 interpretation run via launchd + `codex exec`. **NEXT MORNING**: patterns + intervention plan ready; remediation blocks scheduled into the week. **RETEST**: 48 h later, bank-sourced fresh items on failed subtopics.

## 7. Sprint mode (P3 only)

8-week cycles: 16 mocks, ~2,500 drill questions, one dedicated weakness per week. Budget from credits (projected $40–60/8-weeks at V4 rates — from CREDITS, not cash; recheck against 11 ledger). Sprint adds: weekly mini-post-mortem (15 min, T3), bank-trap calibration vs latest mock, timing re-budgets. Sprint ends with a mandatory KEEP/CHANGE/REMOVE of the sprint mechanics themselves.

## 8. Anti-gaming rules (for the human, stated honestly)

No retaking a mock to "fix the number" (first sitting is the datum; re-sits are logged as such and excluded from forecast). Noopen-book sittings counted as mocks. No skipping post-mortems — mocks without analysis are entertainment. No practicing only liked subjects (allocator outranks preference, 07 §4).
