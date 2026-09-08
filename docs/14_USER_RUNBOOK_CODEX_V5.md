# 14_USER_RUNBOOK_CODEX_V5

**The human operating manual in plain language.** If you read only one implementation file, read this one. Everything here is also in the PDF manual in friendlier formatting.

---

## WHAT I DO EVERY MORNING
Open Terminal. Type `cd ~/cuet-os && codex`. When Codex is ready, type `START`. Answer 6 short questions (sleep, energy, hours, constraint, top confusion — one line each). Approve the day's #1 action it proposes (or say what you'd rather do). Close the laptop lid on system talk and go study.

## WHAT I TYPE (the whole command language)
`START` (morning) · `STATUS` (what's happening) · `PLAN` (adjust the plan) · `DRILL <topic>` (practice questions on a weakness) · `EXPLAIN <concept>` (teach me one thing) · `MOCK` (test-day mode) · `RESEARCH <question>` (verified answer hunt) · `REVIEW` (end-of-day wrap, ~21:30) · `WEEKLY` / `MONTHLY` (when reminded) · `BUDGET` (money + credits) · `MEMORY` (system housekeeping) · `AUDIT` / `REDTEAM` (rare, guided). You can also just talk: "I keep making mistakes in quadratic equations" → it queues a drill cycle (detect → generate → validate → timed set → retest in 48h → gate check). "Mocks feel unstable lately" → it pulls the forecast band and proposes one intervention. "How are we doing against DU cutoffs?" → strategy pack + tagged numbers, not vibes.

## WHAT I ANSWER (all forms in your life, complete list)
Daily: 6-line check-in + 1-line block logs ("BLOCK: topic | 50min | 25Q | 18 correct | types | confusion | next"). Weekly: 7 short fields (06 §2). Monthly: 8 short fields (06 §3). That is everything. Everything else is computed from those lines.

## WHAT I STUDY
What yesterday's REVIEW seeded and today's check-in confirmed: the highest expected-score-gain item (07 §4), in 50/10 blocks. The OS tells you what and how long; you decide nothing before 07:00 and that is a feature.

## WHAT I REPORT AFTER EACH BLOCK
One line. If you forget, tomorrow's START asks once. No guilt loops, no forms.

## WHAT HAPPENS AUTOMATICALLY
Ledgers update from your lines. Mastery gates compute. Spaced retests schedule themselves. Question batches generate overnight on cheap off-peak APIs and get validated before you ever see them. Mock scores compute in 60 seconds with zero AI. The forecast band updates. Model health tracks. Budgets audit nightly. Improvement proposals queue for the weekly review.

## WHAT HAPPENS AT NIGHT (launchd jobs)
22:30 memory compaction → 23:00 off-peak question batch (DeepSeek/free tier — evenings and weekends are off-peak, your timezone is an advantage) → 23:20 credit + cash audit → 23:40 model health probe → 22:40 (Sun–Thu) improvement proposal draft. Nothing wakes you. Nothing posts anything anywhere.

## WHAT HAPPENS WEEKLY (Sunday ~19:00, 40 min)
You fill the 7-field form. Codex shows the computed week: minutes, accuracy trend, errors by type, AI use, burn. You choose exactly ONE change for next week. Done.

## WHAT HAPPENS MONTHLY (first Sunday, ≤90 min)
Bigger computed pack, 15 assessments, KEEP/CHANGE/REMOVE/ADD/RESEARCH/DEFER verdicts, credit reconciliation, red-team pass, restore drill. This is where the system evolves — not at 7 a.m. on a Tuesday.

## WHAT HAPPENS AFTER MOCKS
You sit the mock alone (AI off — integrity is the whole point). Photograph answers. Score appears in a minute. Evening is rest. Overnight the machines analyze. Next morning: patterns, one intervention, retests scheduled for 48h later. One bad mock changes nothing by design; two in a row triggers a panel, not a panic.

## WHAT HAPPENS WHEN THINGS BREAK
Say it in one line: "Codex is down" / "credits look weird" / "the drill questions are bad." The runbook ladder (13 §5) fires: fallbacks, deferrals, or fixes, and the day's studying continues regardless — the OS is designed so its own failure never cancels study time.

## WHAT I NEVER HAVE TO WORRY ABOUT
Choosing models (routed). Remembering anything (ledgers remember). Money surprises (gates + alerts + nightly audit). The 2027 exam pattern being wrong (frozen until NTA says otherwise; everything config-driven). The system silently changing its own rules (it can't — human-gated). Missing an update from NTA/DU (watchlist clocks). AI talking during study (silence law). Whether the system is secretly burning tokens (every call is tagged and visible in BUDGET).

## THE IDEAL DAY, HONESTLY
`07:00 codex → START → 6 answers → study → one-line logs → 21:30 REVIEW → sleep.` If the OS ever takes more than ~25 minutes of your day, that's a defect — complain in the weekly form.

## DEPLOYMENT CHECKLIST (one-time, ~2 h; commands in 02 + starter_scripts)
1. Install Codex CLI, sign in with ChatGPT · 2. `codex --version` → record in models/health.json · 3. Create `~/.codex/AGENTS.md` + `cuet/quiet/heavy.config.toml` profiles + rules files (copy from 02 §3–6) · 4. Create `~/cuet-os/` structure + project AGENTS.md (**pre-generated — copy `AGENTS.md` from this package's root, do not retype**) + `.codex/config.toml` with github+fetch MCP · 5. Set env keys (DeepSeek, Gemini free key, OpenRouter if used) — never in files · 6. Copy `starter_scripts/` into `scripts/`; run `python3 -m pytest tests/` (all green) · 7. Fill `config/{marking_scheme,subjects,budget}.json` (2026 baseline values pre-filled, tagged) · 8. Seed ledgers (baseline scores: Maths 0/10, GAT 0/10, English 6/10 self-reported) · 9. Record Google credit relay per 11 §2–3 — **already known [USER VERIFIED 2026-09-08]: A = $299, expires ~2026-12-07; B = $300, activates ~2026-12-07** — so just verify balances in the console, run the ₹1-scale SKU test on A, and set two calendar reminders: **Dec 1** (A spend-down finish line) and **Dec 7** (B activation day → record B's exact expiry) · 10. NotebookLM: load NB-NTA + NB-DU with official sources · 11. Install launchd plists (starter_scripts/launchd/) · 12. Git init + private remote + first `gov-approved` tag · 13. Run `/status`, note quota posture · 14. Run first START.

## 7-DAY PILOT (before trusting it)
Days 1–2: START/REVIEW only, measure OS-minutes/day. Day 3: first DRILL cycle end-to-end (inspect question quality critically). Day 5: first scored mini-mock via scorer.py (check the math by hand once). Day 6: deliberate failure test — kill internet mid-block, watch fallbacks behave. Day 7: weekly review; verdict KEEP/MODIFY/REMOVE per mechanism tried. Only then adopt the full cadence. Do not make 20 changes at once — the OS itself forbids it.
