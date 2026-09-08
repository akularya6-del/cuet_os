# 10_MCP_FREE_TOOLS_ANTIGRAVITY_V5

**Small trusted surface, big free floor.** The OS deliberately runs on the minimum MCP set, the maximum free-tool floor, and a hard verdict on the Antigravity proxy.

---

## 1. MCP servers (final list — stdio only, Codex config format [OFFICIAL VERIFIED])

| Server | Purpose | Trust | Cost | Setup | Failure behavior | Verdict |
|---|---|---|---|---|---|---|
| `@modelcontextprotocol/server-github` | backup repo issues/PRs, registry sync | 1 (official reference impl) | free | `npx -y` + PAT env var (02 §6) | skip; git still local | **KEEP** |
| `mcp-server-fetch` | stable page capture into research/sources/ | 1 (official reference impl) | free | `uvx mcp-server-fetch` | Codex cached web search covers lookups | **KEEP** |
| NotebookLM community MCP (e.g., browser-cookie based) | scripted NotebookLM queries | **3–4** (unofficial, account-cookie mechanics) | free | none by default | N/A | **OPTIONAL, NOT INSTALLED** — trial rules §2 |

MCP bloat law: adding a 4th server requires the monthly review to REMOVE one first (cap: 3). Security: MCP tool descriptions are untrusted input — tool-poisoning attacks are a documented class [TIER B Invariant Labs 2025-04 / OWASP]; mitigations: only vetted servers, destructive tool calls always prompt (Codex behavior for annotated tools [OFFICIAL VERIFIED]), project `.codex/` layer only when trusted, monthly review of `/mcp` list and `~/.codex/rules/default.rules`. Filesystem MCP: **REJECTED** — Codex has native file tools; a second writer around the same files only widens the blast radius. Memory MCP: **REJECTED** — memory is file-based by design (01); a vector-store side-brain invites divergence. Remote/HTTP MCP servers: not used (earlier releases were stdio-only [TIER B community 2025-08]; re-verify before ever considering one).

## 2. NotebookLM-MCP trial rules (if ever exercised)

Burner Google profile only · read-only queries · no personal/strategy data through it · results treated as [SECONDARY] until cross-checked · never while primary account is signed into the same browser profile · removal triggers: any auth anomaly, any UI change that breaks it, any sign of automation blocking (account risk). Default state: **not installed** (the manual UI + export path in 09 §4-N3 covers all real needs at 20 items/day).

## 3. The free floor (what ₹0 buys every day)

| Tool | Role | Daily capacity (as-of tags) |
|---|---|---|
| NotebookLM Standard | grounded librarian, study guides, quiz seeds | 50 chats, 20 reports/flashcards, 6 video [TIER A V4; recheck after 2026-09-02 change] |
| Gemini API free tier (AI Studio key) | T2 volume overflow via scripts | free promo through 2026-12-31 [OFFICIAL]; Flash-class RPM/RPD per model — **[VERIFY exact numbers in AI Studio dashboard on setup]**; Pro-class free tier reduced/removed [TIER B] |
| Gemini CLI (free auth) | long-context quick tasks in terminal | ~1,000 req/day free [TIER B V4]; Pro allowance conflict unresolved [TIER C] — verify live |
| Groq free tier | fast small-model bursts (classification) | ~14,400 req/day, ~30 RPM [TIER B V4] |
| OpenRouter free models | family-diverse fallback after one-time $10 | 1,000 req/day [TIER A V4] |
| z.ai free Flash trio | GLM-Flash-class overflow | free [TIER B V4] |
| Codex cached web search | in-harness lookups (no live browsing) | within plan [OFFICIAL] |
| Ollama local (optional) | offline fallback; hardware UNKNOWN on user's Mac | unlimited if it fits — **[VERIFY RAM/model fit before relying on it]** |

The floor is the EMERGENCY tier of the reservoir (11 §4): if credits and cash both freeze, the OS still runs at T0–T2 quality. Weekly review includes a 60-second "floor check" (one free-tier call through the night-batch path) so the fallback is tested, not theoretical.

## 4. Antigravity (Google's agentic IDE) — role in V5

> **Plain English — start here if the name is unfamiliar.** Antigravity is Google's free AI coding app: an editor where AI agents write code and run multi-step tasks for you — the same job Codex does in this OS, just made by Google. **You do not need it.** The `antigravity-claude-proxy` GitHub repo is an unofficial hobbyist add-on that tries to funnel Claude models out of Antigravity into other tools; this system refuses it (§5) because it risks your Google account and hands your login credentials to third-party code. **Practical instruction: install neither. No setup step in this OS requires Antigravity — the system runs 100% on Codex + your Google credits + free tools.**

What it is (technical): Google's agent-first development platform (launched 2025-11-18 [OFFICIAL antigravity.google]), free public preview, agent manager + browser control; Pro tier meters agent work on 5-hour + weekly caps [TIER A V4 2026-09-08]; model slate includes Gemini 3.1 Pro, Gemini 3.8/3.7 Flash, Claude Sonnet/Opus 4.6 (thinking), GPT-OSS-120b [TIER A V4]. **V5 role: secondary/optional surface — good for visual agent runs and as a harness fallback (13 §5); never the control plane (Codex owns that), never load-bearing for ledgers.** Its Scheduled-Tasks-style sidecars may serve nightly jobs if Codex desktop scheduling proves insufficient [VERIFY feature maturity on first use].

## 5. antigravity-claude-proxy — audit verdict (repo re-audited 2026-09-08)

What it does: proxy exposing Antigravity-provisioned claude/gemini models to Claude Code and OpenClaw via OpenAI-style `/v1/*` endpoints; v2.0.3 adds API-key auth; `acc` CLI + web dashboard on :8080; authorization = **Google OAuth linking of your Antigravity/Google account** (README walkthrough verified by fetch).

Findings: (a) **reliability**: issue-thread evidence of constant 503 failures with an Ultra account while models worked in other surfaces [TIER B issue comment 2026-01]; (b) **policy**: credential-bridging proxies sit outside Google's supported use; V4 recorded prior ban evidence around similar tooling [TIER B R30]; (c) **security**: linking the primary account to a third-party proxy process exposes session credentials to that process and its network path; (d) **compat**: could technically plug into Codex as an openai-compatible provider — irrelevant given (a)–(c).

**Verdict (unchanged, now with fresh evidence): NOT INSTALLED. TRUST 4. FAILOVER-AT-MOST in a true emergency, on a burner account, never with the primary Google identity, never for exam-critical work.** The legitimate ways to reach Claude-family intelligence are: Anthropic API (cash), Claude-on-Vertex (credits) [OFFICIAL], Antigravity UI itself — all supported, all cheaper than the risk.

## 6. Tools formally retired or rejected (so they stop re-appearing)

OpenClaw/OpenClaw-style integrations [REJECTED V4 — risk profile] · Perplexity subscription [LIKELY EXPIRED + auto-renew trap ₹17,000 — do not resurrect without explicit check] · second Anthropic subscription [not needed; API-on-trigger + Vertex path covers Claude needs] · GLM subscription [REMOVED V4; re-subscribe triggers documented in 11 §7] · any "AI OS framework" npm package that would insert itself between Codex and the files (the OS *is* the framework; it's 16 markdown files + scripts).
