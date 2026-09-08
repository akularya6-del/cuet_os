# 12_SELF_IMPROVEMENT_META_ENGINE_V5

**The system may learn. It may never rewrite itself freely.** Controlled self-improvement with a hard wall between data updates (automatable) and governance changes (human-gated).

---

## 1. The loop

```
OBSERVATION (ledgers, run logs, review outputs)
→ PATTERN (≥ threshold evidence, §3 — never a single event)
→ HYPOTHESIS (written, falsifiable, with the metric it should move)
→ PROPOSED CHANGE (diff-shaped: file, section, before/after)
→ TEST (time-boxed: a week of routed work, or a shadow run on past data)
→ RED TEAM (13 §3 — adversarial pass on the proposal)
→ GIT BRANCH (proposal lives on branch; main is stable)
→ APPLY (human approves; merge)
→ MEASURE (metric vs hypothesis, 1–2 weeks)
→ RETAIN or ROLLBACK (both are successes; drift is the only failure)
```

## 2. What the system learns (evidence-backed, threshold-gated)

| Learning | Source | Threshold |
|---|---|---|
| Which engine serves which task best | token_ledger × validator results | ≥30 tasks per engine×task cell |
| Which generators produce bank-quality questions | L1/L2/L3 pass rates by generator | ≥200 questions per generator |
| Which explanation styles land (fewer follow-ups, faster gate passes) | EXPLAIN logs vs retest outcomes | ≥20 explained concepts per style |
| Which interventions move scores | mock delta after intervention weeks | ≥3 comparable mocks |
| Which scheduling patterns fail | adherence vs plan shape | ≥2 failed weeks of a pattern |
| Which predictions were accurate | horizons.py calibration report | monthly, all open horizons |
| Which AI workflows waste time | OS-overhead minutes + zero-decision outputs | ≥60 min/week wasted on one workflow |

## 3. What the system must NOT learn from (anti-overreaction law)

One bad day; one good day; one bad mock; one good mock; boredom; novelty; a model's one hallucination; one outage; one viral study-hack post; motivational spikes. Thresholds: **strategy-relevant changes require ≥3 independent occurrences or ≥7 sustained days of signal, and must survive a REDTEAM pass.** Daily anomalies are logged (they may become patterns) but cannot alter plans, weights, or budgets. The forecast band (08 §5) exists precisely so single events don't move the system.

## 4. Data vs governance — the wall

| Class | Examples | Who may change | Process |
|---|---|---|---|
| **DATA updates** | ledger appends, mastery map, health.json flags, STATE.md regen, claim registry, pack contents, health scores | scripts, automatically | schema-validated; checksummed; auditable |
| **CONFIG tuning** | allocator weights, router thresholds, scheduler intervals, budget.json prices (with tags) | propose→test→approve | weekly one-change slot or monthly review |
| **GOVERNANCE** | AGENTS.md, docs/00–15, rules file, schemas, reservoir gates, approval matrices | human-approved only | §1 full loop with branch + tests + REDTEAM; **Codex auto-memories and any AI session may never write these files directly** |

Litmus test: *if this change were wrong, would it corrupt truth or just produce a bad week?* Bad-week-only → config path. Truth-corrupting → governance path. When unclear → governance path.

## 5. Experiment registry (`memory/ledgers/experiment_log.jsonl`)

`id · date · hypothesis · change_files · branch · test_window · metric_before/after · redteam_verdict · decision (retain/rollback/extend) · evidence refs`. A change without a registry entry is, by definition, an unauthorized change — `AUDIT` (§7) checks for unregistered diffs between governance files and their last approved versions (git tags `gov-approved-*`).

## 6. Git protocol (safety for self-modification)

Branch naming `exp/<n>-<slug>`; governance changes require: diff ≤ 100 lines OR human explicitly waives; tests pass (`pytest tests/` — scorer golden files, ledger integrity, schema checks); REDTEAM verdict attached in the registry entry; merge by human; tag `gov-approved-<date>`; rollback = `git revert` + ledger note (drilled monthly, 13 §6). Codex's own sandbox rules (02 §4) prompt on `git push`, so nothing leaves the machine unattended.

## 7. Nightly improvement proposal (launchd + `codex exec`)

22:40 IST job: `codex exec "Read memory/ledgers/ + outputs/reviews; if any §2 threshold is met, draft a proposal diff for experiments/next.md; do not modify any tracked file."` Output: at most one proposal/night, stored unapplied. Weekly review triages the week's proposals: adopt (≤1/week via one-change rule), park, or reject with a one-line reason. The proposal prompt itself is governance — changing it goes through §4.

## 8. Improvement freezes

**Freeze windows:** mock day +1 day (diagnostics own the signal); exam-notification week (NTA 2027 — configs only, no mechanism changes); last 4 weeks before CUET (P4: system is frozen except ledgers and decay probes; complexity is the enemy in April). After each freeze, the backlog wakes up — nothing is lost, only queued.

## 9. The meta-rule

The OS improving itself is a means. The only success metric remains the student's score and time. If self-improvement activity ever exceeds ~5% of OS overhead minutes for a month, improvement pauses for a month — the system optimizing itself instead of the student is exactly the failure mode this file exists to prevent.
