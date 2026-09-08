# 15_MODEL_REGISTRY_EVALUATION_AND_MIGRATION_V5

**The fleet manifest.** Every engine with its access path, price (tagged with as-of date), health, and role. The CUET-specific evaluation suite. Migration triggers. The V4→V5 migration map and evidence appendix.

---

## 1. Registry schema

`model · family · access_path · price_in/out per 1M (tag+date) · context · tool_use · batch/peak terms · quota posture · health flags · role (03 tier) · status [VERIFIED/CONFLICT/UNKNOWN]`

## 2. Registry — harness & plan layer

| Entry | Facts | Status |
|---|---|---|
| **Codex CLI (PRIMARY HARNESS)** | official installer/npm/brew; ChatGPT sign-in; AGENTS.md chain (global→project, 32 KiB cap); sandbox+approval policies; stdio MCP; subagents w/ per-agent model configs; rules gating; profiles; exec/resume; cached web search default, `--search` live; /status usage windows (5h+weekly) | [OFFICIAL VERIFIED 2026-09-08] |
| Codex desktop app | /init scaffold, /status, scheduled tasks feature exists | [VERIFIED existence; mechanics VERIFY on setup] |
| ChatGPT Plus (India) | ₹1,999/mo [TIER B 2025-08]; Codex included; GPT-6 Astra LIMITED on Plus (credits purchasable) [OFFICIAL 2026-09-08]; numeric token quota UNKNOWN by design | [VERIFIED unless tagged] |
| Fallback harnesses | Claude Code (if subscription exists), Antigravity UI | [POLICY] |

## 3. Registry — model layer (prices per 1M in/out, USD)

| Model | Path | Price | Context | Role | Status |
|---|---|---|---|---|---|
| GPT-5.5 / gpt-5.3-codex / GPT-5.1-Codex-Max | Codex plan | included | ~258k usable in Codex [TIER B 2026-07]; Codex-Max: compaction, multi-window [TIER B 2025-11] | T3/T4 control plane | [VERIFIED models exist; current default VERIFY via /model] |
| GPT-6 Astra | Codex plan (limited on Plus) | credits purchasable | UNKNOWN | T5 premium in-harness, sparingly | [VERIFIED product; limits PARTIAL] |
| OpenAI API slate (Terra/Luna/Sol) | cash | Luna $0.20/$1.20; Sol $4/$20 promo [TIER B 2026-07/09] | varies | rare overflow | [SECONDARY] |
| Claude Sonnet 5 | Anthropic API or **Vertex** | $2/$10 [TIER A 2026-09-06] | large | T5 verifier/adjudication | [VERIFIED] |
| Claude Opus 5 | Anthropic API or Vertex | $5/$25 [TIER A 2026-09-06] | large | T5/T6 finals, gated | [VERIFIED] |
| Claude (latest on Vertex) | Model Garden | Vertex pricing [VERIFY on console] | — | verifier on credits | [VERIFIED availability 2026-09-03] |
| Gemini 3.1 Pro | Gemini API / Vertex | $4/$18 >200K ctx [TIER B 2026]; ≤200K tier [CONFLICT — verify on bill] | 2M [TIER B] | T4 long-context synthesis | [CONFLICT→VERIFY] |
| Gemini 3.8 Flash | API/Vertex/Antigravity | $0.75/$3.75 intro ends 2026-12-31 [TIER A V4] | large | T2/T3 volume | [VERIFIED] |
| Gemini 3.1 Flash-Lite | API | $0.25-class [TIER B 2026-05] | large | T2 cheap volume | [SECONDARY] |
| Gemini API free tier | AI Studio key | free promo through 2026-12-31 [OFFICIAL]; Flash-class limits VERIFY in dashboard | — | T1/T2 floor | [VERIFIED promo; limits UNKNOWN→VERIFY] |
| DeepSeek V4 Flash | api.deepseek.com (OpenAI+Anthropic formats) | $0.22/$0.66 off-peak; cache-hit $0.007; peak 2× (UTC 01–04, 06–10 Mon–Fri) | 1M-class | T2 bulk generator | [OFFICIAL VERIFIED 2026-09-08] |
| DeepSeek V4 Pro | same | $0.66/$1.98 off-peak | 1M-class | T2/T3 heavy cheap | [OFFICIAL VERIFIED] |
| GLM-5.3 / GLM Flash | official/OpenRouter | $1.40/$4.40 · $0.15/$0.50 [TIER A/B V4 2026-09-06] | — | overflow, panel arm | [VERIFIED] |
| MiniMax M3 / Qwen3.7 Flash | OpenRouter/official | $0.30/$1.20 · $0.03/$0.13 [TIER A/B V4] | — | overflow | [SECONDARY] |
| NotebookLM Standard | UI only | free; 100 NB/50 sources/50 chats [TIER B 2026-08]; changed 2026-09-02 | 500k words/source | grounded librarian | [VERIFIED; no official API] |
| Groq / OpenRouter free / z.ai Flash | free tiers | free quotas (03/10) | — | emergency floor | [TIER A/B V4] |

## 4. CUET evaluation suite (how the OS tests its own fleet)

12 practical tests, run quarterly or on a migration candidate (results in `models/evals/`, tagged with engine+date):

1. **Orchestration** (Codex only): execute a 5-step routing scenario from a cold session; score = correct tier choices without prompts.
2. **Reasoning**: 10 fresh GAT-style logic items; accuracy + explanation validity (expert key).
3. **Maths**: 10 Class-12-level items across calculus/algebra/probability; accuracy + error type.
4. **GAT**: 10 mixed quantitative + GK items (2026-pattern style).
5. **English**: 10 CUET-style reading/grammar items.
6. **Chemistry**: 10 NCERT-aligned items.
7. **Question generation**: 10 items from a fixed blueprint → L1+L2 pipeline; score = pass rate.
8. **Question validation**: 10 seeded-defective items; score = defects caught.
9. **Mock analysis**: same mock report to each candidate; score = insight quality vs expert rubric (1–5).
10. **Evidence discipline**: research task with a planted false premise; score = refusal/correction behavior.
11. **Long context**: 200k-word source + 5 extraction questions (Gemini-class test).
12. **Structured output + failure recovery**: schema-validated JSON under one injected malformed input; score = validity + recovery.

Routing updates from evals follow 03 §10 (per-rupee decision rules) — eval results alone never promote an engine; cost-adjusted results do.

## 5. Migration triggers (any fires → monthly review action)

T1 deprecation/retirement notice (official) · T2 price change >20% · T3 health decay (2 flags/7 days) · T4 quota restructure (plan terms) · T5 better per-rupee cell in router report (≥30-task basis) · T6 eval leader change ≥2 consecutive quarters · T7 harness regression (Codex update breaks AGENTS.md/rules/MCP behavior — pin versions, read release notes before updating) · T8 credit regime change (expiry branch shifts) · T9 NotebookLM policy shift. Migration procedure (carried from V4): registry update → shadow test (1 week dual-run) → router default flip → old engine demoted (not deleted) → rollback point tagged.

## 6. Version pinning policy

Codex CLI + Node + Python versions recorded in `models/health.json`; updates applied **deliberately** (weekly slot), never auto, never mid-sprint; post-update: run `tests/` + one smoke DRILL + `/status` note. Same for MCP server packages (pin via lockfile-style versioned npx/uvx arguments).

## 7. V4→V5 migration map (for continuity with existing V4 files)

| V4 artifact | V5 destination |
|---|---|
| CLAUDE.md bootstrap + .claude/ tree | replaced by AGENTS.md + .codex/ (02) |
| 10-subagent roster + skills folders | 6-agent Codex roster + command grammar (02 §8, 00 §8) |
| hooks JSON (SessionStart/PreToolUse/…) | rules file + scripts + launchd (02 §4, 12 §7) |
| `claude -p` headless jobs | `codex exec` jobs (02 §7) |
| Tier-3a Claude-interactive rows | Tier-3 Codex rows (03 §1) |
| Registry E harness rows | flipped PRIMARY (this file §2) |
| All ledgers/schemas/bank/research | **copied forward unchanged** (git mv; checksums re-verified) |
| V4 15-file docs | archived under docs/v4/ (read-only reference) |

## 8. Evidence appendix (this build)

Research basis: 24 web searches + 12 page fetches on 2026-09-08 (Codex official docs ×10 incl. AGENTS.md/config-reference/approvals/rules/subagents/CLI/plan-limits; DeepSeek official pricing; Gemini rate-limit docs; GCP free-trial FAQ; Antigravity site; antigravity-claude-proxy repo), plus V4's 38 searches and 5 doc captures (Claude Code docs — now demoted to fallback reference), plus the Track B model landscape of 2026-09-06. Full raw notes: `research/EVIDENCE_NOTES_2026-09-08.md` (shipped alongside this build). Items still UNKNOWN and deliberately not guessed: numeric Codex quota per plan; exact Gemini free-tier RPM/RPD numbers; user's actual credit balances/expiry/SKU coverage; Gemini ≤200K pricing tier resolution; NotebookLM post-2026-09-02 exact caps; subagent config file schema; local RAM fit for Ollama. Each has a named verification procedure in 01 §5 / 11 §2 / 02 §8.
