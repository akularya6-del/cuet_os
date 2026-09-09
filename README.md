# CUET-OS 2027

> **A personal academic operating system** — deterministic scripts, AI orchestration, and evidence-tagged memory, purpose-built for one student targeting Delhi University through CUET-UG 2027.

---

## Table of Contents

1. [What Is This?](#1-what-is-this)
2. [Philosophy and Design Principles](#2-philosophy-and-design-principles)
3. [Repository Layout](#3-repository-layout)
4. [Quick Start](#4-quick-start)
5. [The Daily Loop](#5-the-daily-loop)
6. [Scripts Reference](#6-scripts-reference)
7. [Memory and Ledgers](#7-memory-and-ledgers)
8. [Configuration Reference](#8-configuration-reference)
9. [Model Router and AI Tiers](#9-model-router-and-ai-tiers)
10. [Question Bank and Validation Pipeline](#10-question-bank-and-validation-pipeline)
11. [Schemas](#11-schemas)
12. [Evidence Tagging System](#12-evidence-tagging-system)
13. [Google Cloud / Vertex Integration](#13-google-cloud--vertex-integration)
14. [Subjects and Marking Scheme](#14-subjects-and-marking-scheme)
15. [Tests](#15-tests)
16. [Governance and Git Safety](#16-governance-and-git-safety)
17. [Error Taxonomy](#17-error-taxonomy)
18. [Study-Time Protection Rules](#18-study-time-protection-rules)
19. [Authority Hierarchy](#19-authority-hierarchy)
20. [Roadmap and Open Unknowns](#20-roadmap-and-open-unknowns)

---

## 1. What Is This?

**CUET-OS** is not a study app. It is an operating system for one student's exam preparation — a tightly governed pipeline that connects:

- A **deterministic truth layer** (Python scripts that commit facts to ledger files — no AI allowed to touch them directly).
- An **AI orchestration layer** (the Codex agent, governed by `AGENTS.md`, which reads ledgers and proposes actions but never modifies ledgers itself).
- A **question bank** (JSONL files in `bank/`, each question passing a three-level validation gate before admission).
- A **memory and state system** (`memory/ledgers/`) tracking every study block, mock score, error pattern, credit spend, and strategic decision since the project started.
- A **credit reservoir manager** tracking two Google Cloud accounts and their Vertex AI spend in real time.

The goal is a single number: the student's CUET-UG 2027 score. Every design decision is evaluated against that metric. Technical elegance is explicitly deprioritized.

---

## 2. Philosophy and Design Principles

### 2.1 Scripts Are Truth, AI Proposes

The central axiom of CUET-OS: **deterministic scripts commit; AI proposes.** No AI model — not Codex, not Gemini, not any other — is permitted to write directly to `memory/ledgers/`. All ledger writes go through `scripts/ledger.py`, which validates every row against strict schemas before appending. The AI reads ledger state and emits structured proposals. Scripts decide what lands in the canonical record.

### 2.2 The Shell Boundary

Any "bulk or quantifiable" work — generating batches of MCQs, scoring mocks, classifying errors, computing token costs — is pushed to the shell via scripts that may call free or cheap APIs. The output is a small JSON file that is then read back. This keeps expensive AI reasoning for genuinely irreplaceable tasks: strategy adjudication, deep concept explanation, red-team passes.

### 2.3 MCV Governor (Model Cost Value)

Before any AI call, a **Model Cost Value** score is computed:

```
MCV = value × uncertainty × error_cost × reversibility × impact
```

| MCV Range | Tier | Action |
|---|---|---|
| < 20 | T0/T1 | Script or free tool only |
| 20–47 | T2/T3 | Cheap or workhorse model |
| 48–99 | T4 | Strong model; must name the trigger |
| 100–199 | T4/T5 | T4 default; T5 if disagreement is material |
| ≥ 200 | T6 | Panel + human informed before spend |

Run `scripts/router.py` to compute this before any AI call. The script reads `credit_ledger.csv` to determine the current **reservoir mode** (NORMAL → HEAVY → EXPIRING → PEAK → EMERGENCY), which tightens the tier gates in higher-pressure modes.

### 2.4 Evidence Tags

Every factual claim in deliverables carries exactly one evidence tag from a closed vocabulary:

| Tag | Meaning |
|---|---|
| `[OFFICIAL VERIFIED date]` | Primary source confirmed on that date |
| `[HISTORICAL OFFICIAL]` | Past official source; may be outdated |
| `[SECONDARY]` | Reputable secondary source |
| `[INFERENCE]` | Logical deduction from verified facts |
| `[ESTIMATE]` | Quantitative guess with stated basis |
| `[UNKNOWN]` | Not known; fabrication is prohibited |

`UNKNOWN` is always an acceptable answer. The system is explicitly designed to surface ignorance rather than paper over it.

### 2.5 Study-Time Is Sacred

The OS has hard rules about when AI is allowed to speak during study blocks. By default: silence. AI may speak only at four defined moments (see §18). The OS never interrupts timed practice, mock sections, or a student's unaided recall attempts. Minimum 10 minutes of unaided struggle before EXPLAIN is permitted.

---

## 3. Repository Layout

```
cuet_os/
├── AGENTS.md                   # Codex bootstrap — the AI reads this first on START
├── INDEX.md                    # Human-readable sitemap of the 16 doc files
├── README.md                   # ← you are here
├── requirements.txt            # Python dependencies (pinned)
│
├── config/                     # Static configuration (human-edited, human-approved)
│   ├── subjects.json           # Subject roster, baselines, priority classes
│   ├── marking_scheme.json     # +5/−1/0 scheme; REQUIRES-2027-CONFIRMATION
│   ├── vertex.json             # Vertex AI project, routes, token limits
│   ├── budget.json             # Monthly cash caps, per-engine price table
│   └── integrations.toml       # Integration flags (NotebookLM, MCP, etc.)
│
├── docs/                       # 16 governance documents (the law of the system)
│   ├── 00_CODEX_MASTER_ORCHESTRATOR_V5.md
│   ├── 01_MEMORY_AND_STATE_V5.md
│   ├── 02_CODEX_HARNESS_AND_BOOTSTRAP_V5.md
│   ├── 03_MODEL_ROUTER_AND_MODEL_HEALTH_V5.md
│   ├── 04_CLAUDE_GPT_GEMINI_COORDINATION_V5.md
│   ├── 05_DAILY_EXECUTION_AND_USER_LOOP_V5.md
│   ├── 06_WEEKLY_MONTHLY_PHASE_REVIEW_V5.md
│   ├── 07_ACADEMIC_SCORE_MAX_ENGINE_V5.md
│   ├── 08_QUESTION_MOCK_DIAGNOSTIC_ENGINE_V5.md
│   ├── 09_RESEARCH_EVIDENCE_AND_NOTEBOOKLM_V5.md
│   ├── 10_MCP_FREE_TOOLS_ANTIGRAVITY_V5.md
│   ├── 11_GOOGLE_CREDIT_RESERVOIR_AND_CASH_BUDGET_V5.md
│   ├── 12_SELF_IMPROVEMENT_META_ENGINE_V5.md
│   ├── 13_REDTEAM_SECURITY_AND_FAILURE_RECOVERY_V5.md
│   ├── 14_USER_RUNBOOK_CODEX_V5.md
│   └── 15_MODEL_REGISTRY_EVALUATION_AND_MIGRATION_V5.md
│
├── memory/                     # The canonical truth store
│   ├── STATE.md                # Auto-generated snapshot (never hand-edit)
│   ├── ledgers/                # Append-only ledger files
│   │   ├── study_log.jsonl
│   │   ├── error_log.jsonl
│   │   ├── mock_results.jsonl
│   │   ├── decision_log.jsonl
│   │   ├── experiment_log.jsonl
│   │   ├── credit_ledger.csv
│   │   ├── token_ledger.csv
│   │   ├── cash_ledger.csv
│   │   ├── mastery_map.json
│   │   └── model_health.json
│   └── archive/                # Compacted old ledger rows (>400 rows → archive)
│
├── bank/                       # Validated question bank (JSONL, schema-gated)
│   └── _quarantine/            # Questions that failed validation
│
├── schemas/                    # JSON schemas for validation
│   ├── question.schema.json
│   ├── research_extraction.schema.json
│   └── task_envelope.json
│
├── scripts/                    # All deterministic scripts (T0 truth layer)
│   ├── bootstrap_check.py      # Morning system health check
│   ├── ledger.py               # Single writer for all ledger files
│   ├── router.py               # MCV precheck — tier and engine recommendation
│   ├── dispatch.py             # Vertex AI dispatcher (dry-run by default)
│   ├── scorer.py               # Zero-AI mock exam scorer
│   ├── validate_questions.py   # L1 deterministic question validator
│   ├── validate_change.py      # Governance gate for repo changes
│   ├── import_legacy.py        # One-time legacy diagnostic importer
│   └── README.md               # Script usage reference
│
├── models/                     # Model registry and evaluation artifacts
│   ├── REGISTRY.md             # Locally verified model observations
│   └── evals/                  # Evaluation outputs
│
├── tests/                      # Pytest test suite
│   ├── test_core.py
│   ├── test_credit.py
│   ├── test_dispatch.py
│   ├── test_import_legacy.py
│   └── test_question_validation.py
│
├── prompts/                    # Reusable prompt packs for AI context loads
├── research/                   # Evidence notes and research artifacts
├── experiments/                # Experiment tracking
├── outputs/                    # AI-generated content awaiting review
├── logs/                       # Script and harness failure logs
├── assets/                     # Source files for manual/PDF generation
└── manual/                     # Human operating manual (PDF)
```

---

## 4. Quick Start

### Prerequisites

- Python 3.9+
- (Optional, for Vertex AI dispatch) A Google Cloud project with Vertex AI enabled and Application Default Credentials configured.

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/akularya6-del/cuet_os.git
cd cuet_os

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the morning health check
python3 scripts/bootstrap_check.py --quick

# 5. Regenerate STATE.md from ledgers (first run)
python3 scripts/ledger.py state

# 6. Verify all ledgers are clean
python3 scripts/ledger.py verify
```

### First Three Commands After Any Fresh Deployment

```bash
python3 scripts/bootstrap_check.py --quick
python3 scripts/ledger.py state
python3 scripts/ledger.py verify
```

The bootstrap check will warn you about: missing ledger files, stale `STATE.md`, credit expiry windows, and marking scheme confirmation status. Address `WARN:` lines before starting a study session.

---

## 5. The Daily Loop

The OS runs a deterministic state machine throughout each day. All timings are IST.

```
MORNING   →  START → check-in (≤5 questions) → bottleneck identified → today's #1 action proposed
WORK      →  study blocks (50 min study / 10 min break) → silence by default → 1-line block log
AFTER     →  REVIEW (≤10 min, ~21:30) → ledgers updated → tomorrow seeded
NIGHT     →  launchd jobs: memory compact, off-peak AI batches, credit audit, model-health probe
```

### 5.1 Morning START Sequence

When the user types **START** in a Codex session:

1. Codex runs `python3 scripts/bootstrap_check.py --quick` (deterministic, < 3 seconds). Reads only the warnings.
2. Codex reads `memory/STATE.md` (≤ 60 lines).
3. Codex presents the **check-in form** (see below). The student answers 5 fields.
4. Codex identifies today's bottleneck from ledgers (error clusters, mock gaps, mastery decay) and proposes **one highest-value action** with a one-line expected score-impact statement. The student approves or overrides.
5. First study block must start within 10 minutes of START. If it hasn't, the OS flags it and stops adding process.

### 5.2 The Check-In Form

```
DATE:              (auto-filled)
SLEEP:             /10
ENERGY:            /10
AVAILABLE HRS:     h
TODAY CONSTRAINT:  (one line, or "none")
TOP CONFUSION:     (one line, or "none")
```

Everything else (streak, pending retests, reservoir mode, quota posture, yesterday's result) is computed from ledgers — the student never fills those in.

### 5.3 Day Modes

| Mode | Total Study | Trigger |
|---|---|---|
| Minimum | 120 min | Sick/chaos day — 2 blocks, no system work |
| Normal | 270 min | Default: 3–4 blocks |
| Strong | 330 min | ENERGY ≥ 8 + no constraint |
| Recovery | 90 min | Post-mock evening or burnout signal |
| Deep | 360 min | Holiday with ENERGY ≥ 8 |
| Sprint | Phase-defined | March–April mock season (Phase 3) |
| Mock | Per docs/08 | Scheduled Saturdays |

The OS never pushes the student to upgrade a mode. Adherence beats heroics.

### 5.4 After Each Block — the 1-Line Log

```
BLOCK: topic | 50min | 25Q | 18 correct | silly-2,concept-3 | conf: discriminant | next: retest Thu
```

Codex passes this to `ledger.py block`, which validates and appends. Mastery, error taxonomy, and decay updates are **computed**, not asked. No forms beyond this single line.

### 5.5 End-of-Day REVIEW (≤ 10 minutes)

Codex + scripts produce a **DAILY META-REVIEW** inspecting:

- Planned vs actual study minutes
- Error counts by taxonomy (E1–E10)
- Repeated mistakes (same taxonomy + topic ≥ 3 days in 7)
- AI usage: calls, tiers, quota burn, premium-call justification
- Model failures
- OS overhead minutes (must stay ≤ 25 min/day)
- Memory updates applied
- Future-bottleneck flags (1/3/7/14/30-day horizons)

Output: 5 lines maximum, plus a `tomorrow_seed.md`. Mornings start with execution, not planning.

---

## 6. Scripts Reference

All scripts are zero-dependency except where noted. Python 3.9+, standard library only (except `dispatch.py` which needs `google-genai`).

---

### `scripts/bootstrap_check.py`

**The morning T0 health check.** Deterministic — zero AI, zero network calls. Run it first, every day.

```bash
python3 scripts/bootstrap_check.py --quick   # fast: STATE.md + ledgers + credit
python3 scripts/bootstrap_check.py --full    # full: adds model-health flag check
```

**Exit codes:** `0` = clean, `1` = warnings present.

**Checks performed:**

| Check | Detail |
|---|---|
| `STATE.md` freshness | Warns if > 2 days old |
| Ledger presence | Warns if any of the 5 core ledger files is missing |
| JSONL integrity | Parses every line of `study_log`, `error_log`, `mock_results` |
| Credit expiry | Warns if any active account expires in < 45 days |
| Marking scheme | Notes if `REQUIRES-2027-CONFIRMATION` status is active |
| Model health (full) | Flags any engine marked `degraded` in `model_health.json` |

---

### `scripts/ledger.py`

**The single writer for all canonical ledgers.** The AI never writes ledgers directly — it calls this script. All writes are append-only. `STATE.md` is regenerated, never hand-edited.

```bash
# Log a study block
python3 scripts/ledger.py block "topic | 50min | 25Q | 18 correct | [errors] | [confusion] | [next]"

# Log an error
python3 scripts/ledger.py error E3 "quadratic equations" "mixed up discriminant sign"

# Log a credit transaction
python3 scripts/ledger.py credit --account A --currency INR --balance-before 300 --delta -12.50 \
    --balance-after 287.50 --expiry 2026-10-02 --status active \
    --evidence-tag "[OFFICIAL VERIFIED 2026-09-09]"

# Log token usage
python3 scripts/ledger.py token --category volume --task "30 maths MCQs" \
    --engine gemini-3.8-flash --tokens 4200 --est-cost-usd 0.002 \
    --evidence-tag "[ESTIMATE]"

# Regenerate STATE.md
python3 scripts/ledger.py state

# Verify all ledgers
python3 scripts/ledger.py verify

# Compact old rows to archive
python3 scripts/ledger.py compact
```

**`block` format in detail:**

```
topic | minutes | questions | correct | [error_note] | [conf: confusion] | [next: next_action]
```

- `minutes` must be a positive integer (extracted from text like `"50min"`)
- `correct` must be ≤ `questions`
- `confusion` is logged to STATE.md's open-confusions section
- IDs are auto-generated as `B-YYYYMMDD-HHMMSS` with collision avoidance for same-second writes

**`error` taxonomy codes:** E1–E10 (see §17)

**`credit` validations:**
- `balance_before + delta == balance_after` (exact Decimal arithmetic)
- `currency` must be a three-letter uppercase ISO code
- `expiry` must be a valid ISO date
- `status` must be one of: `active`, `dormant`, `depleted`, `expired`

---

### `scripts/router.py`

**Deterministic MCV precheck.** Consults `token_ledger.csv` and `credit_ledger.csv` to add reservoir-mode context. Run this before any AI call to determine the appropriate tier.

```bash
python3 scripts/router.py \
  --task "generate 30 quadratic MCQs" \
  --data \              # output is data → shell boundary may apply
  --value 6 \           # score value (1–10)
  --unc 2 \             # uncertainty if wrong (1–5)
  --err 2 \             # error cost (1–5)
  --rev r \             # reversibility: r=reversible, h=hard
  --imp 6               # impact on score (1–10)
```

**Output (JSON):**

```json
{
  "task": "generate 30 quadratic MCQs",
  "mcv": 288.0,
  "tier": "T6 panel + human informed before spend",
  "engine": null,
  "profile": "heavy",
  "gate_required": true,
  "mode": "EXPIRING",
  "reason": "MCV=288 (v6 u2 e2 rev:r i6)",
  "notes": ["reservoir mode EXPIRING: front-load score-bearing durable assets before expiry (11 §4)"],
  "est_cost": "see config/budget.json price table (tagged)"
}
```

**MCV formula:**

```
MCV = value × uncertainty × error_cost × (1.0 if rev='h' else 0.5) × impact
```

**Shell boundary override:** if `--data` is set and `MCV ≥ 48`, the tier is overridden to `"shell boundary overrides: run via scripts at T2, sample-check 5–10%"` — keeping bulk generation out of expensive in-context AI calls.

---

### `scripts/dispatch.py`

**Vertex AI dispatcher.** Dry-run by default. Requires `google-genai` and a valid `credit_ledger.csv` with an active Account A row.

```bash
# Dry-run (no tokens spent, no API call)
python3 scripts/dispatch.py --task volume --prompt "Generate 20 GAT syllogism MCQs"

# Execution (spends real credits; requires explicit human-approved cap)
.venv/bin/python scripts/dispatch.py \
  --task volume \
  --prompt-file prompts/gat_syllogism.txt \
  --execute \
  --approved-cap-inr 15
```

**Task routes** (from `config/vertex.json`):

| Task | Model |
|---|---|
| `volume` | Gemini 3.8 Flash |
| `complex` | Gemini 2.5 Pro |
| `preview` | Gemini 3.1 Pro Preview (explicit gate: `--allow-preview` required) |

**Safety checks enforced before any execution:**

1. Prompt must be non-empty and < `max_prompt_chars` (100,000 chars)
2. Prompt is scanned for secrets (`sk-`, `AIza`, `ghp_`, `github_pat_`, `AKIA` patterns)
3. Account B is hard-blocked until its scheduled human review date
4. Vertex integration must be `enabled: true` in `vertex.json`
5. Account must be `active` in `credit_ledger.csv`
6. Credit balance must be > 0
7. Expiry date must be in the future
8. `approved_cap_inr` must be provided and ≤ `initial_cap_inr` for execution
9. Project and location must match the verified Account A values (no env-var override accepted)

**Output is never admitted directly into `bank/`.** All dispatcher output must pass `validate_questions.py` (L1) and the L2 engine check before bank admission.

---

### `scripts/scorer.py`

**Zero-AI mock exam scorer.** Reads a CSV of answers and the official key, applies the marking scheme from `config/marking_scheme.json` (`+5 correct / −1 wrong / 0 unanswered`), and appends a row to `memory/ledgers/mock_results.jsonl`.

```bash
python3 scripts/scorer.py mock_answers.csv
```

Used on mock Saturdays: the student photographs their OMR/answer sheet, enters responses into the CSV, and runs the scorer to get a deterministic, AI-free score before any analysis begins.

---

### `scripts/validate_questions.py`

**Deterministic L1 validator for question bank files.** Every question must pass this before any further processing.

```bash
python3 scripts/validate_questions.py bank/maths_quadratic.jsonl
```

**Validation rules enforced (per question):**

| Field | Rule |
|---|---|
| `type` | Must be `mcq4`, `mcq5`, `assertion`, or `arithmetic` |
| `options` | 4 options for mcq4; 4 or 5 for mcq5/assertion/arithmetic; all unique non-empty strings |
| `correct_index` | Integer, 0-indexed, must point to a valid option |
| `difficulty` | Integer 1–5 |
| `trap_type` | Must be E1–E10 |
| `status` | Must be `active`, `quarantined`, or `retired` |
| `explanation` | Required; ≤ 80 words |
| `validation.l1` | Must be `"pass"` |
| `validation.l2_engine` | Required for `active` questions |
| `source` | Must contain `generator`, `date`, `batch` (all non-empty strings) |
| `usage_history` | `times_correct ≤ times_served`; both non-negative integers |

Exit code `0` = all pass, `1` = failures found.

---

### `scripts/validate_change.py`

**Governance gate for repo changes.** Run before committing any governance-file change. Checks:

- English-only policy on core governance files
- Secret scan (same regex as `dispatch.py`)
- `AGENTS.md` size budget (must not exceed configured byte limit)

```bash
python3 scripts/validate_change.py
```

---

### `scripts/import_legacy.py`

**One-time legacy diagnostic importer.** Idempotently applies a one-day-shifted diagnostic import from a legacy CUET-OS folder. Used during the V4→V5 migration.

```bash
python3 scripts/import_legacy.py ~/Desktop/CUET_OS_2027
```

Safe to re-run (idempotent by design).

---

## 7. Memory and Ledgers

`memory/ledgers/` is the canonical store. **Nothing in this directory is ever hand-edited.** All writes go through `ledger.py`. All reads are done by scripts or by the AI reading `STATE.md` + on-demand ledger reads.

### Ledger Files

| File | Type | Purpose |
|---|---|---|
| `study_log.jsonl` | JSONL | One row per study block: topic, minutes, questions, correct, errors, confusion, next |
| `error_log.jsonl` | JSONL | One row per error logged: taxonomy code E1–E10, topic, detail, status (open/resolved) |
| `mock_results.jsonl` | JSONL | One row per mock exam: sections, attempted, correct, accuracy, tentative errors |
| `decision_log.jsonl` | JSONL | Strategic decisions: decision text, evidence tags, horizon notes |
| `experiment_log.jsonl` | JSONL | Improvement experiments: hypothesis, metric before/after, red-team verdict, decision |
| `credit_ledger.csv` | CSV | Every credit transaction on Account A: balance before/after, delta, expiry, evidence tag |
| `token_ledger.csv` | CSV | Token-level AI spend log: engine, tokens, estimated cost USD, evidence tag |
| `cash_ledger.csv` | CSV | Cash spend log (if any): USD amount, engine, approver |
| `mastery_map.json` | JSON | Per-topic mastery scores (computed from study blocks) |
| `model_health.json` | JSON | Per-engine health status (`ok` / `degraded`) |

### STATE.md

`memory/STATE.md` is the AI's compressed morning briefing. It is auto-generated by `ledger.py state` and contains:

- Study minutes in the last 14 days
- Number of open errors and the top taxonomy code
- Number of blocks logged in the last 7 days
- Latest mock result
- Open confusions from recent blocks
- A prompt to run `bootstrap_check.py` for live warnings

**The AI reads STATE.md first, before any ledger. It never edits STATE.md.**

### Compaction

When `study_log.jsonl` or `error_log.jsonl` exceeds 400 rows, `ledger.py compact` moves the oldest 200 rows to `memory/archive/LEDGERNAME.YYYYMM`, keeping the most recent 200 in the active file. Archive files are append-only and never deleted.

---

## 8. Configuration Reference

### `config/subjects.json`

Defines the five subjects the student is preparing, with baselines, priority classes, and known unknowns.

| Subject | Role | Priority Class | Baseline |
|---|---|---|---|
| English | Core | `protect` | 6/10 [USER SELF-REPORTED] |
| Mathematics | Weakest | `highest` | 0/10 [USER SELF-REPORTED] |
| Chemistry | Domain | `standard` | [UNKNOWN] |
| General Aptitude Test | Weakest | `highest` | 0/10 [USER SELF-REPORTED] |
| Physical Education | NIOS 5th subject | `thin-high-yield` | [UNKNOWN] |

> **Status:** `REQUIRES-2027-CONFIRMATION` — exam weights, targets, and chapter lists will be populated once the NTA 2027 notification is released.

### `config/marking_scheme.json`

```json
{
  "correct":    5,
  "wrong":     -1,
  "unanswered": 0,
  "status": "REQUIRES-2027-CONFIRMATION",
  "baseline_cycle": 2026
}
```

The 2026 baseline is `[HISTORICAL OFFICIAL]`. CUET-UG 2027 marking scheme is `[UNKNOWN]` until the NTA notification. `scorer.py` uses this file; reconfirm before any mock result is treated as exam-predictive.

### `config/vertex.json`

Controls all Vertex AI dispatch. The `dispatch.py` script reads this file on every run.

| Key | Value | Notes |
|---|---|---|
| `enabled` | `true` | Global kill-switch for all Vertex calls |
| `project` | `trim-hash-471406-t4` | Account A GCP project |
| `location` | `global` | Vertex global endpoint |
| `routes.volume` | `gemini-3.8-flash` | High-throughput question generation |
| `routes.complex` | `gemini-2.5-pro` | Long-context research reading |
| `routes.preview` | `gemini-3.1-pro-preview` | Explicit preview gate only |
| `max_prompt_chars` | 100,000 | Hard upper limit on prompt size |
| `default_output_tokens` | 512 | Default if not specified |
| `max_output_tokens` | 4,096 | Hard cap |
| `initial_cap_inr` | 100 | Maximum approved per-run cap in INR |

### `config/budget.json`

Monthly cash caps, per-engine price tables (all entries evidence-tagged). Used by `router.py` to flag when the monthly cash spend approaches the cap.

### `config/integrations.toml`

Flags for optional integrations: NotebookLM (source-grounded lookup only, never canonical), MCP tools, and any proxy services. Governs which tools are active at any given time.

---

## 9. Model Router and AI Tiers

The routing system has seven tiers. The tier is determined by MCV (see §2.3) and the current reservoir mode.

| Tier | Label | Use Case |
|---|---|---|
| T0 | Deterministic scripts | Any bulk/quantifiable task |
| T1 | Free tools | NotebookLM, free API endpoints |
| T2 | Cheap model | Gemini 3.8 Flash (Vertex volume route) |
| T3 | Workhorse model | Mid-range tasks |
| T4 | Strong model | Gemini 2.5 Pro (Vertex complex route); named trigger required |
| T5 | Multi-model verification | Strategy changes, mock post-mortems, research canonization, red-team passes |
| T6 | Panel + human | MCV ≥ 200; never run without explicit human awareness |

### Reservoir Modes

The credit reservoir mode is computed by `router.py` from `credit_ledger.csv`:

| Mode | Trigger | Effect |
|---|---|---|
| NORMAL | Balance ≥ 60% of capacity, expiry > 30 days | No restriction |
| HEAVY | Balance 30–60% of capacity | Prefer T2 over T4 |
| EXPIRING | Expiry ≤ 30 days | Front-load score-bearing durable assets |
| PEAK | Balance < 30% of capacity | Credits restricted; T4+ requires explicit justification |
| EMERGENCY | Zero balance or expired | All AI calls blocked; fallback ladder (docs/13 §5) |

### Multi-Model Verification (T5)

Two models are run together only for:
- Strategic decisions (changing study phase, reallocating subjects)
- Mock post-mortems
- Research canonization (upgrading a SECONDARY tag to OFFICIAL)
- Red-team security passes

**Never run two models for convenience.**

---

## 10. Question Bank and Validation Pipeline

Questions live in `bank/` as JSONL files (one question per line). No question enters the bank without passing all three validation levels.

### Validation Pipeline

```
AI generates question
        ↓
  L1: validate_questions.py   ← deterministic, 100% coverage
        ↓ pass
  L2: AI model review         ← engine recorded in validation.l2_engine
        ↓ pass
  L3: Human sample check      ← 5–10% premium sample, logged in validation.l3_by
        ↓ pass
  bank/ admission
```

Questions that fail L1 go to `bank/_quarantine/` with a reason logged to `bank/_quarantine.jsonl`.

### Question Object (all required fields)

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique identifier |
| `subject` | string | e.g., "Mathematics" |
| `topic` | string | e.g., "Quadratic Equations" |
| `subtopic` | string | e.g., "Discriminant" |
| `type` | enum | `mcq4`, `mcq5`, `assertion`, `arithmetic` |
| `stem` | string | The question text |
| `options` | string[] | 4 or 5 options; unique, non-empty |
| `correct_index` | int | 0-indexed pointer into `options` |
| `explanation` | string | ≤ 80 words |
| `recognition_cue` | string | The one-line pattern to recognize this question type |
| `difficulty` | int | 1 (easiest) to 5 (hardest) |
| `trap_type` | enum | E1–E10 (most likely error a student makes on this question) |
| `source` | object | `{generator, date, batch}` |
| `validation` | object | `{l1, l2_engine, l3_by, timestamps}` |
| `usage_history` | object | `{times_served, times_correct}` |
| `status` | enum | `active`, `quarantined`, `retired` |

---

## 11. Schemas

`schemas/` contains JSON Schema (Draft 2020-12) files used by validators and scripts.

| File | Validates |
|---|---|
| `question.schema.json` | Every question in `bank/` |
| `research_extraction.schema.json` | Research extractions from the docs/09 pipeline |
| `task_envelope.json` | Task envelopes passed to AI models via the coordination layer |

---

## 12. Evidence Tagging System

Every factual claim in every deliverable carries exactly one evidence tag.

| Tag | When to Use |
|---|---|
| `[OFFICIAL VERIFIED YYYY-MM-DD]` | You have checked the primary source yourself on that date |
| `[HISTORICAL OFFICIAL]` | This was official in a past cycle; may no longer apply |
| `[SECONDARY]` | Reputable secondary source (textbook, coaching notes); cite the source |
| `[INFERENCE]` | Logical deduction from two or more verified facts |
| `[ESTIMATE]` | A quantitative guess; state the basis |
| `[UNKNOWN]` | You do not know; fabrication is strictly prohibited |

**Canonization procedure:** Upgrading a tag from SECONDARY/INFERENCE/ESTIMATE to OFFICIAL VERIFIED requires the `docs/09` research funnel and a multi-model verification pass (T5).

---

## 13. Google Cloud / Vertex Integration

### Account A

- **Project:** `trim-hash-471406-t4`
- **Endpoint:** `global` (Vertex AI global endpoint)
- **Status:** `EXPIRING` — credits expire **2026-10-02** `[LOCAL VERIFIED 2026-09-09]`
- **Posture:** Front-load score-bearing durable assets. Do not displace study blocks or weaken validation.

### Account B

Deferred. Do not use or ask about Account B before **2026-12-07** unless the human explicitly states it is necessary.

### Authentication Setup

```bash
# Install gcloud CLI and authenticate
gcloud auth application-default login

# Verify the correct project is active
gcloud config set project trim-hash-471406-t4

# Test dispatch (dry-run, no credits spent)
.venv/bin/python scripts/dispatch.py --task volume --prompt "test"
```

### Environment Variables (optional overrides)

```bash
export CUET_GCP_PROJECT_A=trim-hash-471406-t4
export CUET_GCP_REGION_A=global
```

If the environment variables do not match the verified Account A values, `dispatch.py` raises an error and refuses to execute.

---

## 14. Subjects and Marking Scheme

### CUET-UG 2027 Subject Portfolio

| Subject | Code | Priority | Baseline | Notes |
|---|---|---|---|---|
| English | — | Protect | 6/10 | Confirmed |
| Mathematics | — | Highest | 0/10 | Confirmed |
| Chemistry | — | Standard | Unknown | To be assessed |
| General Aptitude Test (GAT) | — | Highest | 0/10 | Confirmed |
| Physical Education (NIOS) | 321 | Thin-high-yield | Unknown | `[HISTORICAL OFFICIAL 2026]` |

### Marking Scheme

Based on 2026 historical data `[HISTORICAL OFFICIAL]`:

- **Correct:** +5
- **Wrong:** −1  
- **Unanswered:** 0

This scheme **requires NTA 2027 confirmation** before any mock result is used for score prediction. Verification trigger: official CUET-UG 2027 notification (expected December 2026 – February 2027).

### Priority Logic

The academic score-max engine (`docs/07`) allocates study time using a priority function combining:

- Baseline score (lower → higher urgency)
- Exam weight (unknown for 2027; treated as equal until confirmed)
- Error cluster density from `error_log.jsonl`
- Mastery decay (time since last successful practice)
- R1/R2 gate status (readiness thresholds for topic graduation)

---

## 15. Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_core.py -v
```

| Test File | Covers |
|---|---|
| `test_core.py` | `ledger.py` — all subcommands, validation, ID collision, compaction |
| `test_credit.py` | `ledger.py credit` — Decimal arithmetic, balance checks, header migration |
| `test_dispatch.py` | `dispatch.py` — dry-run, execution, secret scan, account guards, route selection |
| `test_import_legacy.py` | `import_legacy.py` — idempotency, date-shift logic, legacy format handling |
| `test_question_validation.py` | `validate_questions.py` — all schema rules, edge cases |

Tests use temporary directories and do not touch `memory/ledgers/` or `bank/`. Safe to run at any time.

---

## 16. Governance and Git Safety

### Branch Policy

- `main` — stable, human-approved snapshots only
- `setup/vertex-account-a` — current working branch (Account A setup and verification)
- Feature work uses short-lived branches: `feature/`, `fix/`, `experiment/`

### What Requires Branch + Tests + Human Approval

Any change to:
- `AGENTS.md`
- Any file in `docs/`
- Any file in `schemas/`
- `config/marking_scheme.json`
- `config/subjects.json`

These are **governance files**. The AI may propose changes but may not merge them. `validate_change.py` must pass before any governance file PR is created.

### Hard Rules

1. **Never rewrite git history.** No force-push, no rebase of shared branches.
2. **Pushes are manual.** The AI proposes; the human pushes.
3. **Ledger files are append-only.** Never delete or rewrite a ledger row.
4. **Secrets never enter the repo.** Both `validate_change.py` and `dispatch.py` enforce a secret scan.

---

## 17. Error Taxonomy

Errors logged via `ledger.py error` use a 10-code taxonomy. The taxonomy encodes the *category of mistake*, not just the subject:

| Code | Error Category |
|---|---|
| E1 | Concept gap (did not know the rule) |
| E2 | Recall failure (knew it, couldn't retrieve it) |
| E3 | Procedural error (knew rule, made arithmetic mistake) |
| E4 | Misread question / trap answer |
| E5 | Time pressure / rushed |
| E6 | Overconfidence (skipped checking) |
| E7 | Transfer failure (knew rule in one form, failed in another context) |
| E8 | Negative marking miscalculation (wrong skip/attempt decision) |
| E9 | Missing prerequisite concept |
| E10 | Language/comprehension barrier |

Errors of the same code on the same topic on 3+ days in 7 trigger a **bottleneck flag** in the REVIEW, which becomes the next morning's highest-priority action.

---

## 18. Study-Time Protection Rules

These rules are non-negotiable and are encoded in `AGENTS.md` and `docs/05 §5`.

### When AI May Speak (the only four moments)

1. **After ≥ 10 minutes of unaided struggle on one blocker** — EXPLAIN is Socratic: one hint, then re-attempt required, full answer only on the second request.
2. **At block end** — to receive and commit the one-line log.
3. **During scheduled drill windows** — AI-delivered practice from the overnight question queue.
4. **When the student initiates error logging** — e.g., `ledger.py error E3 ...`

### When AI Must Stay Silent

- During any timed practice session
- During mock exam sections (AI fully silent 09:00–12:00 on mock Saturdays)
- During the student's recall attempts
- During the first 10 minutes of any struggle
- During revision sprints

### What AI Must Never Do

- Generate answers during timed work (exam integrity — `docs/08 §6`)
- Enable "studying by chatting" (retrieval practice is the point, not conversation)
- Run novelty tool tours during study hours
- Break silence for system administration tasks during study blocks

### OS Administration Cap

OS administration must not exceed **25 minutes per day**. If this cap is exceeded for 3 days in any 7-day window, the system must propose a simplification at the next REVIEW.

---

## 19. Authority Hierarchy

When there is a conflict between system components, this hierarchy resolves it (highest authority first):

1. **Deterministic scripts** — they commit truth; all other layers propose.
2. **`AGENTS.md` + `docs/00`** — governance documents, the law of the OS.
3. **Evidence-tagged memory in `memory/ledgers/`** — the factual record.
4. **Second-model adjudication** — only when `docs/03 §7` triggers it.
5. **AI judgment** — within the constraints set by levels 1–4.
6. **The human** — above everything. Human override is always available and always final.

---

## 20. Roadmap and Open Unknowns

### Known Unknowns (as of 2026-09-09)

| Item | Why Unknown | Resolution Trigger |
|---|---|---|
| CUET-UG 2027 exam date | NTA has not notified | NTA CUET-UG 2027 notification |
| 2027 marking scheme | Based on 2026 only | NTA 2027 notification (Dec 2026 – Feb 2027) |
| 2027 subject weights | NTA has not published | NTA 2027 notification |
| Chapter lists for all subjects | Syllabus pending 2027 confirmation | NTA 2027 notification |
| Chemistry baseline | Student has not self-assessed | First Chemistry mock or diagnostic |
| Physical Education baseline | Not yet assessed | First PE practice test |
| Physical Education 2027 paper code | 2026 code is 321; 2027 requires confirmation | NTA 2027 notification |
| Account A balance post-session | Requires console check | Manual credit ledger update after each session |

### Planned Milestones

| Date | Milestone |
|---|---|
| 2026-10-02 | Account A credit expiry — all durable assets generated before this date |
| 2026-12-07 | Earliest date to evaluate Account B |
| Dec 2026 – Feb 2027 | Expected NTA CUET-UG 2027 notification window |
| March 2027 | Phase 3 (Sprint) — mock season begins |
| May 2027 | CUET-UG 2027 exam (expected; `[UNKNOWN until NTA notification]`) |

### Immediate Next Actions (from ledgers, as of 2026-09-09)

1. Log a Chemistry baseline diagnostic block → `python3 scripts/ledger.py block "..."`
2. Front-load Maths and GAT question generation via Vertex before Account A expiry (2026-10-02)
3. Regenerate `STATE.md` after each session → `python3 scripts/ledger.py state`
4. Confirm Physical Education chapter list from NIOS 2027 materials once available

---

## Smoke Test (after fresh clone)

```bash
python3 scripts/ledger.py block "test | 50min | 25Q | 18 correct | concept-2 | conf: none | next: x"
python3 scripts/ledger.py state && python3 scripts/ledger.py verify
python3 scripts/validate_change.py
python3 scripts/bootstrap_check.py --quick
```

All four commands should exit with code `0` and no `WARN:` or `FAIL` lines.

---

## License

This repository contains personal academic preparation materials and is not licensed for redistribution or commercial use.

---

*README last updated: 2026-09-09. Evidence posture: current ledger state reflects V5 deployment on 2026-09-08. All open unknowns are explicitly declared in §20.*
