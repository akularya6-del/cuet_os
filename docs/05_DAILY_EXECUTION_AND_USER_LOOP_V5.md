# 05_DAILY_EXECUTION_AND_USER_LOOP_V5

**The day engine.** The human experience stays trivial; the machinery stays invisible. Timings are IST and tuned to off-peak economics (DeepSeek peak = UTC 01:00–04:00 & 06:00–10:00 Mon–Fri [OFFICIAL 2026-09-08] → IST 06:30–09:30 & 11:30–15:30; **IST evenings and all weekend are off-peak** — bulk jobs run then).

---

## 1. The loop (state machine)

```
MORNING: START → check-in (≤5 Q) → bottleneck → today's #1 action
WORK:    study blocks (50/10) → silence by default → block log (1 line)
AFTER:   REVIEW (end-of-day, ≤10 min) → ledgers updated → tomorrow seeded
NIGHT:   launchd jobs: memory compact, off-peak T2 batches, credit/budget audit,
         model-health probe, improvement proposal (12 §7)
```

## 2. Morning — what the user types and what happens

User opens Terminal: `cd ~/cuet-os && codex --profile cuet`, types **START**.

1. Codex runs `python scripts/bootstrap_check.py --quick` (deterministic, <3 s): STATE.md freshness, ledger integrity, credit warnings, reservoir mode, `/status` posture note.
2. Codex reads STATE.md + check-in pack (≤2 K tokens).
3. Check-in — you answer **exactly 5 questions** (05 §3 form; a sixth field, YESTERDAY RESULT, is auto-filled from ledgers and only needs correcting if wrong). One line each.
4. Codex identifies today's bottleneck from ledgers (error clusters, mock gaps, decay checks) and proposes **one highest-value action** with a one-line expected-score-impact statement. User approves or overrides.
5. First study block starts within 10 minutes of START. If it hasn't, the OS says so and stops adding process.

## 3. The check-in form (whole thing, copy-paste)

```
DATE:            (auto)
SLEEP:           /10
ENERGY:          /10
AVAILABLE HRS:   h
TODAY CONSTRAINT: (one line)
TOP CONFUSION:    (one line, or "none")
```

V4's 5-question set survives; `YESTERDAY RESULT` is now auto-filled from ledgers (REVIEW wrote it), so the form stays at 6 short fields. Everything else (streak, pending retests, reservoir mode, quota posture) is computed, not asked.

## 4. Day modes (carried from V4 — hours are the dial)

| Mode | Total study | Composition trigger |
|---|---|---|
| Minimum | 120 min | sick/chaos day — 2 blocks, no system work |
| Normal | 270 min | default: 3–4 blocks |
| Strong | 330 min | energy ≥8 + no constraint |
| Recovery | 90 min | post-mock evening or burnout signal |
| Deep | 360 min | holiday with energy ≥8 |
| Sprint | phase-defined (P3) | Mar–Apr mock season |
| Mock | per 08 §6 | scheduled Saturdays |

Mode is picked at check-in from SLEEP/ENERGY/constraint; user can override. The OS never "encourages" upgrading a mode — adherence beats heroics.

## 5. During study — when AI may speak (silence is the default)

**AI speaks only at these moments:** (1) after ≥10 min of unaided struggle on one blocker — EXPLAIN is Socratic: one hint, then re-attempt, answer only on second request; (2) block end — capture; (3) scheduled drill windows; (4) safety/error-logging the user initiates.
**AI must stay silent during:** timed practice, mock sections, recall attempts, the first 10 minutes of any struggle, revision sprints.
**Must NOT be used at all for:** generating answers during timed work (exam integrity, 08 §6), "studying by chatting" (retrieval practice is the point), novelty tool tours.
**Misconception rule:** every explanation that resolves a confusion ends with Codex emitting an error_log entry (taxonomy code, 07 §5) via `ledger.py` — confusions are data, not conversation.
**Drill rule:** weakness detected in-session → queue `DRILL` for the block end, never mid-flow.

## 6. After each block — the 1-line log (automation-first)

User pastes one line (or speaks it; Codex formats):
`BLOCK: topic | 50min | 25Q | 18 correct | silly-2,concept-3,gap-2 | conf: limits-and-continuity | next: retest Thu`

Codex → `ledger.py block` commits it; mastery/error/decay updates are **computed** (07 §6–7), not asked. No forms beyond this line. If the user logs nothing, START tomorrow asks for yesterday's missing blocks once, then moves on — guilt is not a mechanism.

## 7. End-of-day REVIEW (≤10 min, ~21:30)

Codex + scripts produce the DAILY META-REVIEW by inspecting: planned vs actual minutes; error counts by taxonomy; repeated mistakes (same taxonomy+topic ≥3 days/7); AI usage (calls, tiers, quota burn); model failures; premium-call justification; OS overhead minutes; research items touched; memory updates applied; future-bottleneck flags (1/3/7/14/30-day horizons). Output = 5 lines max, plus `tomorrow_seed.md`. The REVIEW ends with tomorrow's first action pre-decided — mornings start with execution, not planning.

## 8. Day-in-the-life (derived from this architecture; timings real)

**Normal day:** 06:50 wake → 07:01 `codex` START → 07:04 check-in answered → 07:06 bottleneck = "coordinate-geometry accuracy" → 07:15–08:05 Maths block (silence; one EXPLAIN at minute 34 after failed attempt) → 08:05 one-line log → 08:15–09:05 GAT block → breakfast; 11:30–12:20 Chemistry (peak-rate window — no T2 jobs needed, all local) → 16:00–16:40 PE theory + 20-question T2 drill delivered from overnight queue → 18:00 business hour (OS silent) → 21:30 REVIEW → 5-line meta → sleep. Night jobs: 22:30 memory compact; 23:00 off-peak DeepSeek batch (60 questions queued from today's errors); 23:20 credit audit; 23:40 improvement proposal (12 §7).

**Strong day:** same skeleton, Deep 360 mode: extra 50-min evening block; OS proposes an R1 gate attempt for a stalled topic; two T2 batches.

**Recovery day (post-mock):** 90 min only: 30 min error review of mock report (Codex T4 output from last night), 40 min retest of failed items, 20 min planning; REVIEW logs "recovery"; no new content.

**Mock day (Saturday):** 09:00 mock setup per 08 §6 — AI fully silent 09:00–12:00 (human-only sitting) → 12:01 OMR/answers photographed → 12:05 `scorer.py` deterministic score → afternoon rest (no analysis) → 21:30 REVIEW shows score + tomorrow's remediation plan; full post-mortem runs overnight via T2 classification + one T4 interpretation so Sunday morning starts with patterns, not raw marks.

## 9. What the user never does

Never picks models (03). Never edits ledgers by hand (01). Never fills long forms (§3, §6). Never sits through system work during study hours (§5). Never wonders "what should I study next" (REVIEW seeds it). Never runs the AI more than the plan allows — the OS is the one saying "enough."
