# 06_WEEKLY_MONTHLY_PHASE_REVIEW_V5

**Cadence law.** Weekly = one change. Monthly = keep/change/remove/add/research/defer. Phases = exit gates to May 2027. All forms are copy-paste short; all metrics are computed by scripts before the human sits down.

---

## 1. Cadence table

| Ritual | When | Duration | Engine | Input | Output |
|---|---|---|---|---|---|
| Daily REVIEW | 21:30 | ≤10 min | Codex T3 + scripts | auto | 5-line meta (05 §7) |
| Weekly review | Sunday 19:00 | ≤40 min | Codex heavy profile (1× T4 gated) + scripts | weekly form + computed pack | 1 change + next-week targets |
| Monthly review | 1st Sunday | ≤90 min | Codex heavy + T6 optional | monthly form + 20-point audit | KEEP/CHANGE/REMOVE/ADD/RESEARCH/DEFER |
| Red team pass | 2× / month (with monthly) | 45 min | T6 panel | REDTEAM pack | attack notes + patches |
| Credit reconciliation | monthly, with review | 15 min | credit_audit.py + console check | credit_ledger | updated balances + forecast |
| Registry re-check | monthly | 15 min | scripts + web spot-check | models/REGISTRY.md | price/quota updates (15) |
| Backup + restore drill | monthly | 15 min | ledger.py export + git push (manual) | memory/ | verified backup |

## 2. Weekly review — exact procedure

1. Scripts pre-compute (before human sits): study minutes vs plan by day and subject; accuracy trend; error taxonomy counts; retest pass-rate; mock delta; AI usage by tier (Codex windows used, T2 items, premium calls); OS-overhead minutes; reservoir mode and burn; adherence streak; open loops (unresolved confusions, stale claims).
2. Codex (STRATEGY pack) reads the computed pack and answers 12 standing questions (carried from V4): score trajectory, weakest section by expected-gain, strongest to protect, retention risk (decay checks due), error pattern of the week, one intervention to run, AI over/under-use, quota posture, credit burn vs forecast, single biggest system friction, next week's top-3 actions, what to stop doing.
3. **One-change rule:** the review may adopt exactly ONE system change for the coming week (12 §3 threshold applies to data-driven changes; this slot is for workflow changes). Everything else goes to the parking list.
4. Output: `outputs/weekly/2026-Wnn.md` (≤1 page) + updated STATE.md + tomorrow seeded.

### Weekly form (copy-paste)
```
WEEK:            (auto)
ADHERENCE:       x/7 days ≥ target
AVG STUDY:       x h/day
BEST MOMENT:     (one line)
WORST MOMENT:    (one line)
ONE COMPLAINT:   about the OS (one line)
ONE REQUEST:     (one line)
```

## 3. Monthly review — exact procedure

Run the weekly script at month grain, then Codex assesses 15 dimensions and issues verdicts: performance vs phase gate; score forecast band vs target band (SC anchor 630–670 [HISTORICAL OFFICIAL 2026] — re-verify each cycle); subject balance vs 865-h plan (07 §3); syllabus coverage; retention (decay probe pass-rate); mock trend + stability (σ); time accounting; adherence; business hours protected or not; AI spend (cash + credits vs budget.json); provider health (model_health.json); system complexity (LOC, active mechanisms, MCP count); future phase readiness; rule changes due; open research items.

Verdict vocabulary (mandatory, per item): **KEEP / CHANGE / REMOVE / ADD / RESEARCH / DEFER.** REMOVE is a first-class outcome — any mechanism that produced zero referenced decisions or zero score-relevant actions in a month is a REMOVE candidate. Complexity budget: if active mechanisms grew >2 net items, the next month must net-remove.

### Monthly form (copy-paste)
```
MONTH:           (auto)
SCORE TREND:     (auto, band)
BIGGEST WIN:     (one line)
BIGGEST LEAK:    (time or marks) (one line)
CASH SPENT:      $      CREDITS BURNED:  $
HEALTH:          sleep/energy/illness (one line)
BUSINESS HOURS:  kept? (yes/no)
```

## 4. Phase map to CUET 2027 (dates tagged; exam window [UNKNOWN until NTA notification, expected ~Dec 2026–Feb 2027 announcement, May–Jun 2027 test] [REQUIRES 2027 CONFIRMATION])

| Phase | Window | Focus | Exit gate (all required) |
|---|---|---|---|
| P0 Foundation of the OS | Sep 2026 | deploy V5, baseline mocks, ledger hygiene | 7-day pilot done; 2 baseline mocks scored; all ledgers live |
| P1 Syllabus ramp | Oct–Dec 2026 | full syllabus first pass; **heavy question-bank generation on credits before expiry**; Maths/GAT fundamentals | 100% topics touched; mastery R1 on ≥60% topics; bank ≥3,000 validated Qs |
| P2 Consolidation | Jan–Feb 2027 | weak-zone second pass; speed work; NTA 2027 pattern verified + configs updated | R2 on P1 topics; timed accuracy ≥70% target sections |
| P3 Mock intensive | Mar–Apr 2027 | 2 mocks/week, full post-mortem cycle, stability training | mock σ ≤ 15; forecast band inside target |
| P4 Final | Apr–May 2027 | retention only, error-log shrink, PE + GT polish, taper | decay probes ≥90%; no new content last 10 days |

Google-credit alignment: activate both accounts' heaviest use in P1 (P2's compounding assets: bank, study guides, extracted sources). If credits expire late (12-month variant), P2 premium usage may draw the remainder — see 11 §3 branch logic.

## 5. Decision authority (who may decide what — unchanged from V4, reworded)

| Decision | Authority |
|---|---|
| Ledger math, scoring, validation | Scripts (final) |
| Daily tactics, drill selection | Codex proposes, user picks |
| Weekly one-change | User approves (Codex recommends) |
| Strategy shifts, subject reweighting | Monthly review + user, evidence-tagged, T6 if contested |
| Cash spend > $5 non-recurring | Buy-nothing gate + explicit user approval (11 §7) |
| Governance file edits | Governed loop only (12 §4) — user approval mandatory |
| Exam-pattern config | NTA notification only; nothing else may touch marking_scheme.json |

## 6. Review hygiene

Reviews never run on mock days. A skipped weekly review rolls into the next one (never "double" the one-change rule). Monthly review that exceeds 90 minutes is stopped at the clock and continued next morning — cadence must protect study hours as strictly as the daily loop does. All review outputs are git-committed (diffable history of the system's own evolution, feeding 12 §6).
