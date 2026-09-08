# CUET OS V5 — Codex-Native Build (2026-09-08)

Start here if you are human: `docs/14_USER_RUNBOOK_CODEX_V5.md`, then the PDF manual in `manual/`.
Codex reads: AGENTS.md (generate from 02 §5) + docs/ on demand.

## Implementation files (16)
| File | Role |
|---|---|
| 00_CODEX_MASTER_ORCHESTRATOR_V5 | Mission, V4-to-V5 audit, pipeline, command grammar |
| 01_MEMORY_AND_STATE_V5 | Ledgers, single-writer map, context packs, auto-memory governance |
| 02_CODEX_HARNESS_AND_BOOTSTRAP_V5 | Install, config.toml, profiles, rules, THE AGENTS.md text, subagents |
| 03_MODEL_ROUTER_AND_MODEL_HEALTH_V5 | 7 tiers, MCV governor, health ledger, failure ladder |
| 04_CLAUDE_GPT_GEMINI_COORDINATION_V5 | Harness-vs-model, access paths, panel law, task envelope |
| 05_DAILY_EXECUTION_AND_USER_LOOP_V5 | Check-in, silence law, day-in-the-life x4 |
| 06_WEEKLY_MONTHLY_PHASE_REVIEW_V5 | Cadence, forms, phases to May 2027 |
| 07_ACADEMIC_SCORE_MAX_ENGINE_V5 | Allocation, priority function, error taxonomy, R1/R2 gates |
| 08_QUESTION_MOCK_DIAGNOSTIC_ENGINE_V5 | Generation pipeline, validators, mock UX, forecast |
| 09_RESEARCH_EVIDENCE_AND_NOTEBOOKLM_V5 | Funnel, evidence tags, NotebookLM contract |
| 10_MCP_FREE_TOOLS_ANTIGRAVITY_V5 | MCP set (3 max), free floor, proxy verdict: NOT INSTALLED |
| 11_GOOGLE_CREDIT_RESERVOIR_AND_CASH_BUDGET_V5 | Two accounts, expiry branches, $55 gated reserve |
| 12_SELF_IMPROVEMENT_META_ENGINE_V5 | Governed loop, data-vs-governance wall, freezes |
| 13_REDTEAM_SECURITY_AND_FAILURE_RECOVERY_V5 | 22 attacks, data routing, recovery matrix |
| 14_USER_RUNBOOK_CODEX_V5 | Plain-language operating manual (source of the PDF) |
| 15_MODEL_REGISTRY_EVALUATION_AND_MIGRATION_V5 | Fleet registry, eval suite, migration triggers |

## Also in this folder
- **AGENTS.md** — ready-to-copy project bootstrap for Codex (generated from 02 §5). Place at `~/cuet-os/AGENTS.md` — do not retype it.
- `manual/CUET_2027_CODEX_MAXIMUM_PERFORMANCE_HUMAN_OPERATING_MANUAL.pdf` — the 15-page human manual
- `research/EVIDENCE_NOTES_2026-09-08.md` — research base with evidence tags and UNKNOWN list (updated 2026-09-08 with user-verified credit relay facts)
- `scripts/` — deterministic scripts + README
- assets/cover_source.html — editable cover source for the PDF manual

## First three commands after deployment
1. python3 scripts/bootstrap_check.py --quick
2. codex --profile cuet  ->  START
3. python3 scripts/ledger.py state
