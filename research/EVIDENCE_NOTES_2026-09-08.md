# V5 RESEARCH NOTES — evidence base (as-of 2026-09-08)

## CODEX (all [OFFICIAL VERIFIED 2026-09-08] unless noted — source learn.chatgpt.com, help.openai.com)
- Install: `curl -fsSL https://chatgpt.com/codex/install.sh | sh` / `npm i -g @openai/codex` / `brew install --cask codex`. Sign in with ChatGPT.
- AGENTS.md chain: global `~/.codex/AGENTS.md` (or AGENTS.override.md); project: Git root walked down to CWD, first non-empty file per level wins; `project_doc_max_bytes` default 32 KiB (raise or split into nested dirs). `.md` versions of docs pages exist (append .md).
- Rules (experimental): `~/.codex/rules/*.rules` + project `.codex/rules/` (trusted projects only). `prefix_rule(pattern=[...], decision="prompt"|"allow"|"deny"?)`, scanned at startup. TUI allow-writes go to user layer.
- Config: `~/.codex/config.toml`; project overrides `.codex/config.toml` (closest wins); `-c key=value` CLI override. Profiles: `--profile name` overlays `~/.codex/<name>.config.toml` (top-level keys, separate file per profile).
- Sandbox modes: read-only / workspace-write / danger-full-access; approval_policy incl. untrusted / on-request / never + granular policy object; network gated; `/permissions`; `--sandbox workspace-write --ask-for-approval on-request` recommended for low-friction local work; `--search` = live web (default cached web search); destructive MCP tool calls always prompt unless read-annotated.
- MCP: stdio servers in config `[mcp_servers.<id>]` command/args/env/env_vars; startup_timeout_sec; tool-catalog timeout default 1000.
- Subagents [OFFICIAL VERIFIED]: Codex runs subagent workflows, parallel, results collected into one response; local Codex clients can define CUSTOM agents with different model configurations + instructions; `/agent` inspects/switches threads; AGENTS.md/skill instructions can request delegation; subagent work consumes more tokens; context-pollution rationale official.
- Native memories: config keys `memories.*` (e.g., no_memories_if_mcp_or_web_search, max_raw_memories_for_consolidation=256, max_unused_days=30) — auto-memory exists; keep file-based memory canonical, govern auto-memories.
- Sessions: `codex resume` / `resume --last`; `codex exec` for scripts/CI (headless); `codex --image` attachments; app-server + --remote ws:// possible; slash: /init /status /mcp /plan /review /goal (desktop) + /permissions /model (TUI); `/init` generates AGENTS.md scaffold.
- Plans/limits: Codex included in Free/Go/Plus/Pro/Business/Enterprise; Plus = "a few focused coding sessions each week"; 5-hour + weekly usage windows; `/status` shows usage; banked resets (referral) refresh windows; higher tiers 5x/20x; GPT-6 Astra included (full on $100/$200 Pro + $100 Business; LIMITED on Plus + $20 Business, credits purchasable); switching to lower-cost model stretches allowance. ChatGPT Plus India ₹1,999/mo [TIER B 2025-08]. Codex models seen: gpt-5.5, gpt-5.3-codex, GPT-5.1-Codex-Max (compaction, multi-window); Codex caps context ~400k/~258k usable [TIER B 2026-07].
- Codex desktop app has Scheduled Tasks [VERIFIED existence]; CLI path = launchd/cron + `codex exec` (documented pattern).

## GOOGLE
- Vertex AI now "Gemini Enterprise Agent Platform"; Model Garden carries Gemini + partner models incl. Claude on Google Cloud (docs updated 2026-09-03, Agent Platform request-response supported) [OFFICIAL VERIFIED].
- Gemini 3 Pro API $2/$12 (≤200K) → $4/$18 (>200K) [TIER B apidog]; Gemini 3.1 Pro $4/$18 >200K, 2M ctx, 3.1 Flash-Lite $0.25 [TIER B metacto]; Gemini Developer API free promos END 2026-12-31 [OFFICIAL ai.google.dev: $0.075→$0.15 Jan 1 2027; free tier through Dec 31 2026]; Gemini 3.8 Flash intro $0.75/$3.75 ends 2026-12-31 [TIER A V4]. Free tier for Pro-class reduced/removed [TIER B Reddit + Google statement] — VERIFY live.
- Gemini API rate limits: RPM/TPM/RPD per project; Free→Tier1 via billing [OFFICIAL structure; numeric Free-tier table VERIFY in AI Studio].
- GCP Free Trial: $300 Welcome credit, 90 days, ends when exhausted OR upgraded OR account closed; not pausable/extensible [OFFICIAL]. Two accounts = two separate trials/billing accounts; practical precedent exists [TIER B Reddit]; ToS nuance: one trial per person per Google account — second account must be legitimately separate (different identity/eligibility); legality risk flagged; never pool credits; balances UNKNOWN → verify via Billing console each account.
- Antigravity: Google's agentic development platform, launched 2025-11-18, free preview; Pro tier w/ 5h+weekly caps metered by agent work [TIER A V4]; model slate incl. Gemini 3.1 Pro, 3.8 Flash, Claude Sonnet/Opus 4.6, GPT-OSS-120b [TIER A V4 2026-09-08].

## ANTIGRAVITY-CLAUDE-PROXY (repo fetched 2026-09-08)
- Purpose: expose Antigravity-provisioned claude/gemini models to Claude Code + OpenClaw via /v1/* endpoints; v2.0.3 added API-key auth; `acc` CLI (acc ui dashboard :8080, acc start --log); Google OAuth "Link Account(s)".
- Reliability: issue comments report constant 503s (Ultra account) Jan 2026 [TIER B]. V4 verdict stands: DEFAULT NOT INSTALLED, TRUST 4, failover-at-most. Codex-compat: theoretically usable as openai-compatible model_provider; NOT recommended.

## NOTEBOOKLM
- 2026 limits: Standard/free 100 notebooks, 50 sources each, 500k words/source, 200MB upload; 50 chats/day free; plan changes from 2026-09-02 (support.google.com); Plus 100 sources, Pro 300, Ultra 600 + 5000 chats/day [TIER B mixed]; Video/Reports/Flashcards/Quizzes daily caps [TIER A V4: 6/day video, 20/day reports]. NO official API [VERIFIED via ongoing user complaints 2026]; community MCP servers exist (TRUST 3, non-load-bearing).

## PRICES (per 1M tokens)
- DeepSeek OFFICIAL (api-docs.deepseek.com, fetched 2026-09-08): deepseek-v4-flash $0.22 in (cache-hit $0.007) / $0.66 out off-peak; deepseek-v4-pro $0.66 in ($0.022 hit) / $1.98 out off-peak; PEAK = 2× (peak hours UTC 01:00–04:00, 06:00–10:00 Mon–Fri → IST 06:30–09:30, 11:30–15:30 Mon–Fri; IST evenings/weekends off-peak). OpenAI-format base https://api.deepseek.com AND Anthropic-format https://api.deepseek.com/anthropic. Thinking default on; concurrency flash 2500/pro 500.
- Claude (Track B 2026-09-06 [TIER A]): Sonnet 5 $2/$10; Opus 5 $5/$25; Fable 5.1 $10/$50.
- OpenAI API: GPT-5 $1.25/M in [TIER B]; slate $0.20–$50/1M: GPT-6 Astra, Sol ($4/$20 promo 2026-07-30), Terra, Luna ($0.20/$1.20) [TIER B cloudzero/stob 2026-09-04].
- GLM-5.3 $1.40/$4.40; GLM Flash $0.15/$0.50; MiniMax M3 $0.30/$1.20; Qwen3.7 Flash $0.03/$0.13 [TIER A/B V4 2026-09-06].
- FX ₹94.5/USD [VERIFIED 2026-09-06]; ChatGPT Plus India ₹1,999.
- Batch APIs ~50% discount [TIER A V4, re-verify per provider].

## CUET (baseline)
- CUET-UG 2026 marking: +5 correct, −1 wrong, 0 unanswered; sections Language (IA/IB), Domain, GT [TIER B multiple 2026]; per-paper max 250 marks (50Q) [TIER B]. 2027 pattern UNKNOWN → scripts/config-driven marking_scheme.json; NTA notification expected ~Dec 2026 syllabus/Jan 2027 [REQUIRES 2027 CONFIRMATION].
- Student: SC category female, NIOS PE 5th subject (locked), targets DU BMS/BBE/B.Com(Hons) etc., 5–6h/day max, Maths 0/10, GAT 0/10, English 6/10 self-baseline; SC composite band 630–670 [HISTORICAL OFFICIAL 2026].

## V4 ECONOMICS (worklog — carried into V5)
- Architecture C: raw burst $0.56/mo NORMAL; credit burn ≈$2.83/mo; new cash $5–9/mo typical, $12 hard cap; $55 = PARKED GATED RESERVE (peak phase, credit expiry, provider failure); one-time $10 OpenRouter; sprint $40–60/8wk from CREDITS not cash; GLM sub removed; cash ≥$10 non-one-time needs buy-nothing gate.
- V5 update: reservoir now includes Claude-on-Vertex (credits can buy Claude!) → verifier/adjudication can run on credits, cash reserve lasts longer. Codex Plus absorbs orchestration/interactive (was Claude Pro in V4).

## USER-VERIFIED CREDIT FACTS (2026-09-08, in-chat) — supersedes estimates
- [USER VERIFIED 2026-09-08] Google Account A: **$299** credit, expires **~90 days from 2026-09-08 → ~2026-12-07**.
- [USER VERIFIED 2026-09-08] Google Account B: **$300** credit, **activates ~90 days from 2026-09-08 → ~2026-12-07**. B's own expiry: [UNKNOWN → record on activation day]; if it runs a second 90-day clock it would end ~2027-03-07 (still before the ~May 2027 exam window).
- Architecture consequence: two-account policy moves from balance-trigger reserve to a **time-based relay** (11 §1, §3): A front-loads durable assets Sep→Dec; B carries mock-season premium Dec→Mar; final stretch runs free floor + subscription + gated cash.
- Downloaded manual updated with the exact dates; ledger seeds: A balance 299, B balance 300 (inactive).
- [USER REPORT 2026-09-08] Antigravity not recognized by the user → plain-English explainer added at 10 §4; verdicts unchanged (Antigravity optional; antigravity-claude-proxy NOT INSTALLED, TRUST 4). System runs 100% without either.
