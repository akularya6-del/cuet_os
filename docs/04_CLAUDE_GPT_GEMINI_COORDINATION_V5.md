# 04_CLAUDE_GPT_GEMINI_COORDINATION_V5

**How the model families cooperate now that GPT/Codex is the control plane.** This file re-runs the V4 coordination verdict with the harness inverted.

---

## 1. Harness vs model — the distinction that was missing before V4's end

| Concept | V4 assumption | V5 reality |
|---|---|---|
| **Harness** (the place work starts: instructions, tools, permissions, sessions) | Claude Code | **Codex** (CLI/TUI + desktop app + `codex exec`) [OFFICIAL VERIFIED] |
| **Model** (the intelligence a harness or API call invokes) | Claude (interactive), GPT (verifier) | GPT-class via Codex plan; Claude/Gemini/others via APIs and Google surfaces |

Consequence: Claude **models** remain fully usable; **Claude Code as harness is demoted to fallback** (13 §5). The reverse also holds: Codex models can be called via OpenAI API with cash if ever needed — but the plan-included path is preferred (that's what the subscription is for).

## 2. Access paths (all verified 2026-09-08 unless tagged)

| Family | Path | Cost surface | Notes |
|---|---|---|---|
| GPT / Codex models | Codex CLI/app with ChatGPT sign-in | **subscription** (Plus ₹1,999 [TIER B]) | 5h+weekly windows; GPT-6 Astra limited on Plus [OFFICIAL] |
| OpenAI API (rare) | developers.openai.com key | cash | only if plan path is exhausted and task is critical |
| Claude | Anthropic API (console key) | cash (Sonnet 5 $2/$10, Opus 5 $5/$25 [TIER A 2026-09-06]) | elite triggers only |
| Claude **on Vertex** | Model Garden via Google Cloud | **Google credits** [OFFICIAL: Claude on Google Cloud docs, 2026-09-03] | the V5 unlock: credits can buy cross-family verification |
| Gemini | Gemini API free tier (promo through 2026-12-31 [OFFICIAL ai.google.dev]), then paid; Vertex (credits); Gemini CLI free tier; Antigravity | free → credits | volume + long context |
| DeepSeek | api.deepseek.com — **OpenAI-format AND Anthropic-format endpoints** [OFFICIAL 2026-09-08] | cash, tiny | off-peak half price; peak hours UTC 01–04, 06–10 Mon–Fri |
| GLM / MiniMax / Qwen | official APIs or OpenRouter | cash, tiny | overflow pool |
| OpenRouter | one-time $10 → 1,000 free req/day + paid routing [TIER A V4] | one-time cash | family-agnostic fallback |

## 3. Role assignment (the 17-row V4 table, re-decided for Codex-primary)

| Role | Owner | Why |
|---|---|---|
| Control plane, orchestration, tool use | **Codex (GPT)** | verified subagents, rules, profiles, exec; strongest harness fit |
| Quantitative reasoning, structured analysis | Codex | native to control plane; scripts check arithmetic anyway |
| Independent second opinion / verification of Codex output | **Claude (Sonnet 5) via Vertex credits or Anthropic API** | different family — anti-echo-chamber requirement; credits make it nearly free now |
| Complex code + automation | Codex first; Claude on 2 failures | keep one escalation rung |
| Long-form reasoning/writing (essays, strategy memos) | Codex; Gemini 3.x Pro for long-context synthesis | length fits Gemini's 1–2M context [TIER B] |
| Volume generation (questions, tagging, classification) | **DeepSeek V4 Flash / Gemini Flash / GLM Flash** | cheapest competent; validators catch defects |
| Long documents, PDFs, multimodal (images of problems) | **Gemini** (API/Vertex); Codex `--image` for quick visual context | context + vision economics |
| Google-ecosystem research | Gemini + Codex cached/live web search | complementary retrieval |
| Source-grounded lookup, study guides, flashcards | **NotebookLM** | citation-bound librarian (09 contract) |
| Arithmetic, ledgers, scoring, scheduling | **Scripts, always** | zero hallucination, zero cost |
| Bulk repetitive analysis | T2 engines via scripts | shell boundary |

## 4. Coordination patterns (the only four legal ones)

1. **Solo** — one engine end-to-end (the default; covers ~90% of days).
2. **Generate→Verify** — T2/T3 produces data; validators + a different-family check when 03 §7 fires (e.g., DeepSeek generates questions; Claude-on-Vertex audits the 5–10% sample on credits).
3. **Panel (T6)** — three arms from ≥2 families, blind inputs, moderator = scripts collect, human decides. Composition law: **≥1 non-OpenAI arm AND ≥1 non-Google arm; Codex excluded from panels judging its own output** (anti-echo-chamber; V4's law preserved and sharpened).
4. **Handoff** — async file exchange via `schemas/task_envelope.json` (§6) so no engine needs another's raw session context.

Forbidden: running the same task on multiple engines "for confidence" without §03 gates; letting any engine append to ledgers directly; letting the same family verify its own output on load-bearing items.

## 5. Why this division beats the alternatives (verdict re-run)

V4 rejected "GPT primary" partly because Claude Code was the stronger harness in evidence. That evidence changed: Codex now has verified subagents, rules gating, profiles, native memories, exec/CI use, and live/cached web search [OFFICIAL 2026-09-08] — the harness gap closed. Re-evaluated candidates: (A) Codex-primary + Claude-as-verifier + Gemini-volume **wins** on harness fit, cost (credits cover cross-family checks), and continuity with existing subscriptions; (B) Claude-primary fails the user's constraint (can no longer rely on Claude Code); (C) Gemini-primary would burn finite credits on orchestration, the one thing scripts+subscription already do free. Risk carried: OpenAI plan dependence — mitigated by fallback ladder (13 §5) and the family-diverse verifier path.

## 6. Task envelope (the handoff format, `schemas/task_envelope.json`)

```json
{
  "task_id": "T-2026-0910-A3",
  "type": "question_validation | research_extraction | adjudication | writing",
  "engine_hint": {"family": "claude", "via": "vertex", "min_ctx": 200000},
  "context_pack": "prompts/RESEARCH_2026-09-10.md",
  "input_files": ["research/sources/nta_2026_notice.pdf"],
  "instruction": "Extract every date, fee, and eligibility clause with quotes + page refs.",
  "output_schema": "schemas/research_extraction.schema.json",
  "evidence_tags_required": true,
  "budget_usd_max": 0.05,
  "deadline": "2026-09-10T21:00:00+05:30",
  "requester": "codex-main", "created": "2026-09-10T07:12:00+05:30"
}
```

Scripts dispatch envelopes (`scripts/dispatch.py`), engines respond with schema-validated JSON, `ledger.py` logs cost and validator result. Human-readable record lands in `logs/`.

## 7. Family-failure handoffs

GPT/quota failure → orchestration degrades to scripts + Claude Code (if active) or Antigravity for the day (13 §5). Claude unavailable → verification arm becomes Gemini Pro (non-Google rule relaxes to "different vendor" with a logged exception — still never same-family). Gemini failure → DeepSeek handles volume, NotebookLM holds grounded lookups. Every handoff is one line in the daily log; weekly review counts handoffs as a health metric.
