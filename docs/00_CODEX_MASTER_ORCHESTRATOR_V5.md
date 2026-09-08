# 00_CODEX_MASTER_ORCHESTRATOR_V5

**CUET-UG 2027 Operating System — Version 5 (Codex-Native)**
Built: 2026-09-08 · Primary harness: **OpenAI Codex** · Currency of truth: `memory/` ledgers · Evidence tags mandatory.

---

## 1. Mission (unchanged, re-anchored)

One student, one goal: maximize the CUET-UG 2027 score and convert it into a Delhi University seat (BMS/BBE/B.Com Hons or fallback programs), while running an AI-receptionist side business and protecting 5–6 h/day of real study. This OS is a **personal academic operating system, not a chatbot**. Every mechanism exists to produce one of four outputs: more correct answers, fewer repeated errors, better time allocation, or a better strategic decision. Anything else is overhead and must justify itself monthly.

V5 changes the control plane. The previous assumption — Claude Code as primary harness — is dead. **Codex is now the primary harness.** All orchestration, verification, and interactive work starts inside Codex. Claude, Gemini, DeepSeek, GLM, and NotebookLM are *specialists the OS routes to*, not places where work begins.

## 2. The one architectural idea of V5

> **Codex tokens are the scarcest resource. Bulk work must leave the Codex process.**

Codex (ChatGPT Plus plan) runs on 5-hour + weekly usage windows with no public numeric quota [OFFICIAL VERIFIED: help.openai.com, 2026-09-08]. Therefore the OS enforces a **shell boundary**: whenever a task is shaped like "call an API, return JSON" — question generation, classification, tagging, mock scoring of raw answer keys, research capture — Codex must **run a script** (`python scripts/...`) that calls a cheap/free engine (DeepSeek off-peak, Gemini free tier, Groq, OpenRouter free), and then read the small JSON result. Codex spends its tokens deciding and verifying; scripts spend fractions of a cent producing volume. This single rule is why V5 fits inside a Plus plan plus ~$600 of finite Google credit and ~$55/month of *gated* cash.

## 3. Conceptual pipeline (Codex-native)

```
USER (types START / natural language)
  ↓  Codex interactive TUI (ChatGPT sign-in)
AGENTS.md BOOTSTRAP (rules load once per session)
  ↓
MASTER ORCHESTRATOR (Codex main thread — this file's policy)
  ↓
TASK CLASSIFIER  →  scripts/router.py precheck (deterministic: reads ledgers)
  ↓
CONTEXT RETRIEVER  →  context pack from prompts/ (see 01 §7)
  ↓
MODEL/TOOL ROUTER  →  tier decision (see 03)  — may be "NO MODEL / SCRIPT ONLY"
  ↓
SPECIALIST EXECUTION
   ├─ in-process: Codex (reasoning, coding, verification)
   ├─ subagents: Codex parallel agents, per-agent model configs [OFFICIAL VERIFIED]
   └─ out-of-process: scripts → DeepSeek / Gemini API / Vertex / NotebookLM / free tools
  ↓
VERIFICATION (structural validator always; second model only when 03 says so)
  ↓
DETERMINISTIC STATE UPDATE (scripts commit truth into memory/ ledgers)
  ↓
FUTURE-IMPACT UPDATE (1/3/7/14/30-day horizon notes, see 07 §9)
  ↓
END-OF-DAY SELF-REVIEW (REVIEW command)
  ↓
CONTROLLED SELF-IMPROVEMENT (nightly proposal via codex exec, see 12)
```

The pipeline is conceptual; its implementation is the file map in §7 plus AGENTS.md. If a cheaper architecture emerges (e.g., Codex scheduled tasks maturing), the weekly review may amend it through the governed process in 12.

## 4. V4 → V5 audit verdicts

The full audit was performed on all 16 V4 files, all V4 research digests, and the worklog. Verdicts:

| V4 component | Verdict | Why |
|---|---|---|
| 00 Master orchestrator (Claude Code boot, 13-step 7:00 AM) | **REPLACE** | Boot assumed `claude` CLI, CLAUDE.md, hooks. Codex boot is AGENTS.md-driven. |
| 01 Memory & state (ledgers, single-writer, append-only) | **KEEP** | Harness-neutral discipline. Rewrite only the CLAUDE.md/@imports sections → AGENTS.md + Codex memory config. |
| 02 Claude Code harness (10 subagents, hooks, skills, permissions) | **REPLACE** | 100% Claude Code-native. V5 equivalent: 02 file (AGENTS.md, profiles, rules, stdio MCP, subagents). Roster cut 10 → 6. |
| 03 Model router (tiers, MCV, failure ladder) | **MODIFY** | Tier scale and MCV survive. Tier-3a re-pointed to Codex; routing mechanism changes from subagent `model:` field to profile switch + script shell-out + subagent configs. |
| 04 Coordination (verifier pattern, no-duplication law) | **MODIFY** | Verdict logic re-run: "GPT-primary rejected" is void — GPT now primary. Anti-echo-chamber rule strengthened (Codex excluded from panels judging Codex output). |
| 05 Daily execution (day modes, 25-min ceiling, check-in) | **KEEP** | Harness-neutral. Launch command and headless jobs re-bound to Codex. |
| 06 Weekly/monthly cadence | **KEEP** | Clock and authority law stand; prep jobs move to launchd + `codex exec`. |
| 07 Academic score engine (865 h, priority function, taxonomy) | **KEEP** | Engine-agnostic. Bindings re-pointed only. |
| 08 Question/mock engine | **KEEP** | Pipeline, validators, bank layout, forecast formula stand. Overnight runner re-bound (off-peak DeepSeek). |
| 09 Research/evidence/NotebookLM | **KEEP** | Funnel, VOI gate, NotebookLM contract stand; capture re-bound to Codex web search + fetch MCP. |
| 10 MCP/free tools/Antigravity | **MERGE+MODIFY** | Proxy verdict (NOT INSTALLED, TRUST 4) re-confirmed with fresh repo fetch + 503 evidence. MCP list trimmed to ≤3 stdio servers, Codex format. OpenClaw rejection stands. |
| 11 Google credit reservoir | **KEEP + EXTEND** | Fully harness-neutral economics. V5 adds Claude-on-Vertex (credits can now buy Claude) and two-account A/B policy. |
| 12 Red team / failure recovery | **MODIFY** | HARNESS-FAILURE fallback inverts: fallback is now Claude Code/Antigravity, primary is Codex. Monoculture attack re-targets Codex. |
| 13 User runbook | **REWRITE** | Every command re-bound to `codex`; Codex-first phase-0. |
| 14 Model registry & migration | **MODIFY** | Registry E (harness registry) flips PRIMARY to Codex; prices re-verified 2026-09-08; Codex limits become load-bearing open items. |
| $55 budget | **UPHOLD + CLARIFY** | $55 stays a **gated reserve ceiling**, not a spending target. Typical cash: $0–9/month (see 11 §7). |

**Removed outright in V5:** OpenClaw integration (was already rejected), Claude Pro as an assumed subscription (do not renew unless Claude becomes primary again), the 10-agent roster (overkill under a stronger harness), any mechanism that assumed `claude -p` headless runs.

## 5. Authority hierarchy (dispute resolution order)

1. **Deterministic scripts** — arithmetic, ledgers, scoring, validation. Scripts commit truth; models only propose.
2. **This file + AGENTS.md** — governing policy. Changeable only via the governed loop (12).
3. **Evidence-tagged memory** (`memory/` files with [OFFICIAL VERIFIED] / [INFERENCE] / [UNKNOWN] labels).
4. **Second-model adjudication** (only when 03 §7 triggers it).
5. **Codex main-thread judgment** — everything else.
6. **Human owner** — always above all of this; can veto anything with one sentence.

## 6. Boot sequence (what happens when the user opens Codex)

1. `cd ~/cuet-os && codex` — Codex TUI starts, signs in via ChatGPT.
2. Codex builds the instruction chain once per session: `~/.codex/AGENTS.md` (global, ~90 lines) + project `AGENTS.md` (≤32 KiB default cap [OFFICIAL VERIFIED]) + `.codex/rules/*.rules` command gates.
3. Profile: `codex --profile cuet` loads `~/.codex/cuet.config.toml` (sandbox `workspace-write`, approval `on-request`, cuet model settings).
4. User types `START`. Codex runs `python scripts/bootstrap_check.py --quick` (deterministic: STATE.md freshness, ledger integrity, credit warnings) and the check-in (05 §3).
5. Work happens under the shell-boundary rule (§2). Everything lands in ledgers via scripts.

**Session recovery:** `codex resume` / `codex resume --last` [OFFICIAL VERIFIED]. Long task interrupted → resume; do not re-plan from scratch.

## 7. File map (what lives where)

```
cuet-os/
├── AGENTS.md                  ← THE bootstrap (generated from 02 §5; keep < 20 KB)
├── .codex/
│   ├── config.toml            ← project config (sandbox, MCP servers)
│   ├── rules/cuet.rules       ← command gating (git push, rm -rf, credit spend)
│   └── agents/                ← custom subagent definitions [VERIFY exact format on first use]
├── memory/                    ← canonical state (scripts own it)
│   ├── STATE.md               ← current phase, focus, warnings (human-readable cache)
│   ├── ledgers/*.json|csv     ← append-only truth: mastery, errors, tokens, credits, cash
│   └── archive/               ← compacted history (never auto-deleted)
├── logs/                      ← daily logs, run logs (append-only)
├── research/                  ← sources/, claims/, watchlist (09)
├── models/                    ← REGISTRY.md, health.json, evals/ (03, 15)
├── scripts/                   ← deterministic Python + shell (the "commit truth" layer)
├── schemas/                   ← JSON schemas for every ledger and task envelope
├── prompts/                   ← context packs (ACADEMIC, RESEARCH, STRATEGY, REDTEAM, MEMORY)
├── bank/                      ← question bank {subject}/{topic}.jsonl + _quarantine.jsonl
├── outputs/                   ← generated deliverables (drills, mock reports, weekly reviews)
├── tests/                     ← pytest for scripts; golden files for scoring math
├── config/                    ← marking_scheme.json, subjects.json, budget.json
└── docs/                      ← these 16 V5 files (read on demand, not per session)
```

`AGENTS.md` deliberately does **not** contain the architecture. It contains behavior rules and a pointer map to `docs/` so Codex reads only what a task requires (context economy, see 01 §6).

## 8. Command grammar (smallest useful set)

| Command | Meaning | Executor |
|---|---|---|
| `START` | Morning check-in + today's highest-value action | Codex + bootstrap_check.py |
| `STATUS` | State, ledgers, quota/credit posture, warnings | bootstrap_check.py --full |
| `PLAN` | Build/adjust today's or this week's plan | Codex (STRATEGY pack) |
| `DRILL <topic>` | Weakness → generate questions → validate → deliver | 08 pipeline |
| `EXPLAIN <concept>` | One concept, Socratic, logged as confusion | Codex or Gemini |
| `MOCK` | Mock-day protocol (before/during/after) | 08 §6 |
| `RESEARCH <question>` | Evidence-tagged research funnel | 09 |
| `REVIEW` | End-of-day meta-review | Codex + scripts |
| `WEEKLY` / `MONTHLY` | Cadence reviews with forms | 06 |
| `BUDGET` | Credit + cash position, burn forecast | credit_audit.py |
| `AUDIT` | System self-audit (20-point) | 12 §7 |
| `REDTEAM <decision>` | Adversarial pass before big decisions | 13 |
| `MEMORY <cmd>` | compact / verify / archive ledgers | ledger.py |

Natural language always works: *"I keep making mistakes in quadratic equations"* routes to the DRILL/RETEST workflow (see 14 §6). Unrecognized inputs default to: classify → propose → confirm with user before any premium call.

## 9. Escalation and failure rules (summary; full versions in 03 §9 and 13 §5)

- **Escalate up** (cheap → premium) only when: structural validation fails twice, disagreement is material, stakes are high (mock interpretation, strategy changes), or MCV ≥ 48 (03 §6).
- **De-escalate or refuse** when: memory is sufficient, a script can compute it, NotebookLM covers it, or expected score impact ≈ 0. The router must be allowed to answer "no model needed."
- **Harness failure** (Codex down/quota-out): fall back to Claude Code (if subscription active) or Antigravity, or plain CLI + scripts; nothing blocks ledgers and scripts (13 §5).
- **Never** let any failure mode write garbage into `memory/`; scripts validate before commit.

## 10. Study-time protection (non-negotiable)

The OS exists for the exam, not for itself. Hard rules: (1) 25-minute/day OS administration ceiling with automatic simplification after 3 heavy days in 7 (carried from V4); (2) during a study block the default is silence — AI speaks only at defined moments (05 §5); (3) productive struggle: minimum 10 minutes of unaided attempt before any EXPLAIN; (4) no AI content-chain generation during exam-sim hours; (5) if OS overhead exceeds 30 min/day for a week, the weekly review must cut features (one-change rule, 06 §3).

## 11. What V5 does NOT promise

No guaranteed score. No parallelism claims beyond what Codex subagents + scripts actually do (parallel subagents verified available [OFFICIAL VERIFIED 2026-09-08]; anything else is sequential). No fabricated quotas: every number in this OS carries a tag and a date; unknowns are marked UNKNOWN and verified at the listed procedure. No self-rewriting governance (12). No $55 routine spending — the envelope is a reserve with a gate (11 §7).

## 12. Reading order for Codex (and the human)

Per-session (small): `AGENTS.md` only. On demand by task type: academic work → 07/08; routing → 03/15; strategy → 05/06; money → 11; failure → 13; research → 09. Human: read 14 (runbook) and the PDF manual; never required to read the rest.
