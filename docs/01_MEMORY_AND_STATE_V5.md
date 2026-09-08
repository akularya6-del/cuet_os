# 01_MEMORY_AND_STATE_V5

**Memory architecture for the Codex harness.** Carries forward the V4 invariants (they were harness-neutral and correct), replaces the Claude Code memory mechanics (CLAUDE.md, @imports, auto-memory caps) with verified Codex mechanisms.

---

## 1. The four invariants (unchanged from V4 — KEEP)

1. **Logs are truth.** Everything that happened goes to `logs/` and `memory/ledgers/` first, as append-only records.
2. **State is a derived cache.** `memory/STATE.md` is regenerated from ledgers by `scripts/ledger.py state`; if it disagrees with ledgers, ledgers win.
3. **Stale equals unknown.** Any fact older than its refresh clock is treated as unknown, not as false and not as true (see §5 clocks).
4. **Single writer per file.** Exactly one writer owns each file (§4). Anyone else must go through that writer's interface. No exceptions, including Codex auto-memories.

Why these survive: they cost nothing, they prevent the two classic failures (state drift and double-write corruption), and they are independent of which AI harness runs the day. V4 ran them under Claude Code; V5 runs them under Codex; a future V6 could run them under anything.

## 2. Codex memory surface — what the harness gives us [OFFICIAL VERIFIED 2026-09-08]

Codex has **three** instruction/memory layers the OS uses:

| Layer | Path | Loaded when | OS use |
|---|---|---|---|
| Global instructions | `~/.codex/AGENTS.md` | Every session, always | Cross-project personal rules only (~90 lines max). CUET-specific rules do NOT live here. |
| Project instructions | `~/cuet-os/AGENTS.md` | Every session in repo | THE bootstrap: identity, boot sequence, routing policy, evidence rules, pointer map to docs/ (full text in 02 §5). Default cap 32 KiB — our target < 20 KB. |
| Rules (experimental) | `~/.codex/rules/*.rules`, `.codex/rules/` | Startup, command gating | Hard command-level guardrails (deny/allow/prompt on `git push`, spend scripts, destructive rm). See 02 §4. |

Codex also has a **native auto-memories feature** (config keys under `memories.*`, consolidation controls) [OFFICIAL VERIFIED]. Governance decision:

- Auto-memories are treated as **session scratch**, never as canonical state.
- `AGENTS.md` instructs Codex: canonical memory = files in `memory/`; anything important must be appended there via scripts before session end.
- Monthly audit compares auto-memory content against ledgers; contradictions are resolved in favor of ledgers. If auto-memories ever cause instruction drift (Codex "remembering" rules that contradict AGENTS.md), the fallback is disabling native memories via config and relying purely on files — this is a one-line config change plus Red Team note 13 §2-A9.
- Context compaction: Codex compacts long sessions itself (GPT-5.1-Codex-Max introduced native compaction [TIER B 2025-11]); the OS still prefers short sessions + `codex resume` over one marathon session, because compaction is lossy and the OS needs precision on ledgers.

## 3. The memory tree (what each file is for)

```
memory/
├── STATE.md                  ← derived cache: phase, today's focus, warnings, reservoir mode
├── ledgers/
│   ├── study_log.jsonl       ← one line per study block (topic, minutes, Qs, accuracy, error refs)
│   ├── error_log.jsonl       ← every wrong answer, taxonomy code (07 §5), status open/resolved
│   ├── mastery_map.json      ← topic → {accuracy_30d, attempts, last_seen, gate_status}
│   ├── mock_results.jsonl    ← mock scores + section splits + timing
│   ├── token_ledger.csv      ← FREE|SUBSCRIPTION|CREDIT|CASH rows: date, task, engine, tokens, est_cost
│   ├── credit_ledger.csv     ← per-account balance snapshots + burn entries
│   ├── cash_ledger.csv       ← every real-money spend, gated approvals
│   ├── decision_log.jsonl    ← strategy decisions with evidence tags + horizon notes
│   ├── model_health.json     ← per-engine availability/latency/failure counters (03 §8)
│   └── experiment_log.jsonl  ← self-improvement experiments (12 §5)
└── archive/                  ← compacted months (never deleted)
```

All ledger writes go through `scripts/ledger.py` (or dedicated scripts) which validate JSON shape against `schemas/` before appending. Models NEVER write ledgers directly — they emit structured proposals that scripts commit.

## 4. Single-writer map (condensed; full 18-row table in V4 remains valid)

| Data | Writer | Everyone else |
|---|---|---|
| study/error/mock ledgers | `scripts/ledger.py` (from user input + mock scorer output) | propose only |
| mastery_map.json | `scripts/mastery.py` (R1/R2 gate math, 07 §6) | propose only |
| token/credit/cash ledgers | `scripts/ledger.py` + `scripts/credit_audit.py` | propose only |
| STATE.md | `scripts/ledger.py state` (regeneration) | never hand-edit |
| AGENTS.md | Human approval via governed loop (12 §4) | never |
| docs/ | Governed loop with git branch + tests | never |
| Codex auto-memories | Codex native | treat as scratch, audit monthly |

## 5. Refresh clocks (stale = unknown)

| Fact class | Clock | Renewal action |
|---|---|---|
| CUET 2027 pattern/markings | until NTA 2027 notification | set `config/marking_scheme.json` source tag REQUIRES-2027-CONFIRMATION; check at notification (expected Dec 2026–Feb 2027) [UNKNOWN] |
| DU CSAS rules | each admission cycle | re-verify at CSAS 2027 bulletin release |
| Model prices | 30 days | weekly BUDGET run flags entries older than clock (15) |
| Credit balances | 7 days | manual console check → credit_ledger.csv |
| Codex/plan quotas | 30 days | `/status` screenshot note into token_ledger notes |
| NotebookLM limits | 30 days | quick UI check (12-notebook limits page) |
| Mastery estimates | 14 days without attempt | mastery_map marks `decay_check` (07 §7) |

## 6. Context economy — what Codex loads and when

The 32 KiB project-instructions cap is not a problem (AGENTS.md < 20 KB), but **context pollution** is: Codex docs themselves warn that flooding the main thread with intermediate output degrades reliability [OFFICIAL VERIFIED: subagents page]. Rules:

1. Per-session baseline = AGENTS.md + STATE.md only (≤ ~4 K tokens combined).
2. Everything else comes via **context packs** (§7), chosen by task type.
3. Large artifacts (bank files, research PDFs, long logs) are read by **scripts** and reduced to summaries before Codex sees them. Codex summarizes JSON, never raw 500-question banks.
4. Subagents absorb noisy work (exploration, log analysis, validation sweeps) and return summaries [OFFICIAL VERIFIED capability].
5. Session hygiene: one work theme per session; end sessions with REVIEW; use `codex resume` to continue rather than re-priming; `MEMORY compact` weekly.

## 7. Context packs (task-specific, stored in `prompts/`)

| Pack | Files included | Approx budget | Used by |
|---|---|---|---|
| ACADEMIC | mastery slice for topic (script-filtered), last 10 errors on topic, subject config | ≤ 2 K tokens | DRILL, EXPLAIN, RETEST |
| RESEARCH | claim registry slice, source registry index, watchlist W-items | ≤ 3 K | RESEARCH |
| STRATEGY | STATE.md, mock trend (script summary), capacity window, open decisions | ≤ 3 K | PLAN, WEEKLY |
| REDTEAM | decision + evidence list + assumptions **without** prior conclusion | ≤ 3 K | REDTEAM |
| MOCK-DAY | today's mock config, timing protocol, scoring sheet template | ≤ 2 K | MOCK |

Packs are assembled by `scripts/pack.py <name> <topic>` which reads ledgers and emits a single markdown file. Codex requests packs; scripts build them; this keeps "load only what the task requires" enforceable and measurable (pack line counts land in token_ledger as FREE rows).

## 8. Contamination guards

- **Append-only**: corrections are new entries with `supersedes` refs; nothing is edited in place. Ledger verification (`ledger.py verify`) recomputes counts and checks JSONL integrity (checksums in `memory/ledger_manifest.json`).
- **No unverified claims as canon**: research outputs carry evidence tags; only [OFFICIAL VERIFIED]/[HISTORICAL OFFICIAL] entries may be referenced by strategy logic; [INFERENCE] requires 2 independent supports to be promoted (09 §6).
- **One bad day writes nothing**: ledger-triggered strategy changes require the evidence thresholds in 12 §3 (≥3 occurrences or ≥7 days). Daily anomalies are logged, not acted on.
- **Backup**: ledgers are git-tracked (private remote) and exported weekly by `MEMORY` to `outputs/backups/`; restore drill runs monthly (13 §6).
