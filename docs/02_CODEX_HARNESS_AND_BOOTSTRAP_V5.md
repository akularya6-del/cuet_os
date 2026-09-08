# 02_CODEX_HARNESS_AND_BOOTSTRAP_V5

**The exact Codex-native harness.** Everything here is grounded in official Codex documentation fetched 2026-09-08 (learn.chatgpt.com: AGENTS.md, Configuration Reference, Advanced Config, Agent approvals & security, Rules, Subagents, Codex CLI, Developer commands; help.openai.com: Codex plan limits). Where a detail could not be verified, it is marked **[VERIFY]** with the exact check to run.

---

## 1. Install and sign-in (macOS)

```bash
# Official installer [OFFICIAL VERIFIED]
curl -fsSL https://chatgpt.com/codex/install.sh | sh
# Alternatives: npm install -g @openai/codex   |   brew install --cask codex

cd ~/cuet-os
codex                # first run → choose "Sign in with ChatGPT" (uses the Plus plan;
                     # do NOT paste API keys for the interactive harness — that path bills cash)
codex --version      # record into models/health.json (pin versions, see 15 §6)
```

Plan facts that shape this design [OFFICIAL VERIFIED]: Codex is included in ChatGPT plans; Plus = "a few focused coding sessions each week"; usage runs on **5-hour + weekly windows**, visible via `/status`; banked resets (e.g., referral rewards) refresh windows; switching to a lower-cost model stretches allowance; GPT-6 Astra is limited on Plus (credits purchasable). ChatGPT Plus India = ₹1,999/month [TIER B 2025-08]. Numeric per-plan token quotas are **UNKNOWN** — treat the windows as the real constraint (that is why §6 exists).

## 2. Directory layout the harness expects

```
~/cuet-os/
├── AGENTS.md                  ← project bootstrap (§5) — loaded every session
├── .codex/
│   ├── config.toml            ← project-scoped overrides (closest file wins [OFFICIAL VERIFIED])
│   ├── rules/cuet.rules       ← command gates (§4)
│   └── agents/                ← custom subagent definitions [VERIFY format]
~/.codex/
├── AGENTS.md                  ← global instructions (§3)
├── cuet.config.toml           ← the `--profile cuet` overlay [OFFICIAL VERIFIED format]
├── quiet.config.toml          ← low-noise profile
├── heavy.config.toml          ← long-review profile
└── rules/default.rules        ← user-layer command gates
```

## 3. Global instructions — `~/.codex/AGENTS.md` (exact text)

Keep it tiny; CUET logic lives in the project file.

```markdown
# Global working agreements
- You are the assistant inside the CUET-OS project when working in ~/cuet-os.
  Follow that project's AGENTS.md over these defaults when they differ.
- Never send API keys, tokens, or billing data anywhere; never print secrets.
- Prefer deterministic scripts over model reasoning for arithmetic and ledgers.
- Ask before any action that costs money (API calls, subscriptions, credits).
- Keep responses compact; do not restate files you were given.
```

## 4. Command gating — `~/.codex/rules/cuet.rules` (exact text)

Rules are an experimental Codex feature: `prefix_rule(pattern, decision, justification)` scanned at startup from every active config layer [OFFICIAL VERIFIED — mark experimental; re-verify behavior after Codex updates].

```python
# CUET-OS command gates. Decisions: "prompt" keeps a human in the loop.
prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "Pushes publish memory/governance; weekly backup pushes are manual.",
    match = ["git push origin main"], not_match = ["git push --dry-run origin main"],
)
prefix_rule(
    pattern = ["python", "scripts/spend.py"],
    decision = "prompt",
    justification = "Any cash-spending script needs explicit human approval.",
)
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "prompt",
    justification = "No recursive deletes without the human.",
)
```

The TUI's own "allow" choices persist into `~/.codex/rules/default.rules` [OFFICIAL VERIFIED] — audit that file monthly so accidental allows don't accumulate.

## 5. Project bootstrap — `~/cuet-os/AGENTS.md` (exact text, ~7 KB — the crown jewel)

```markdown
# CUET-OS 2027 — Codex bootstrap

## Identity and purpose
You are the orchestrator of a personal academic operating system for one student
preparing for CUET-UG 2027 (Delhi University target, May 2027 expected window,
[UNKNOWN until NTA notification]). Your success metric: the student's score and
time efficiency — not technical elegance. Studying always outranks system work.

## Authority hierarchy
1. Deterministic scripts (they commit truth; you propose).
2. AGENTS.md + docs/00 (governance).
3. Evidence-tagged memory in memory/ledgers/.
4. Second-model adjudication (only when docs/03 §7 triggers it).
5. Your own judgment. 6. The human above everything.

## Boot sequence (on "START")
1. Run: python scripts/bootstrap_check.py --quick  → read its warnings only.
2. Read memory/STATE.md (≤ 60 lines).
3. Ask the check-in (docs/05 §3): at most 5 questions you ask; yesterday's result is auto-filled from ledgers.
4. Propose today's highest-value action from ledgers; wait for choice.

## Routing policy (summary; full law in docs/03)
- Default tier: NO MODEL or CHEAP. Escalate only on documented triggers.
- Shell boundary: any bulk/quantifiable work (questions, classification, scoring,
  capture) → run scripts that call free/cheap APIs; read back small JSON.
- Premium (in-process heavy reasoning) requires MCV ≥ 48 or a named trigger
  (docs/03 §6–7). Before premium calls, say the tier and why in one line.
- Multi-model verification ONLY for: strategy changes, mock post-mortems,
  research canonization, red-team passes. Never run two models for convenience.

## Evidence rules
- Every factual claim in deliverables carries a tag: [OFFICIAL VERIFIED date],
  [HISTORICAL OFFICIAL], [SECONDARY], [INFERENCE], [ESTIMATE], [UNKNOWN].
- UNKNOWN is an acceptable answer. Never fabricate quotas, prices, dates, or
  catalog contents. Verify via docs/09 procedures before canonizing.

## Memory rules
- memory/ledgers/ is canonical. You never edit ledgers directly; you emit
  structured proposals that scripts validate and commit.
- Native auto-memories are session scratch. Anything durable must land in
  ledgers via scripts before the session ends.
- Read only what the task needs (docs/01 §6 context economy; use prompts/ packs).

## Model/tool routing defaults
- Interactive reasoning, coding, verification: yourself (Codex).
- Volume generation: scripts → DeepSeek V4 Flash (off-peak) or Gemini free tier.
- Long-context research reading: Gemini via API/Vertex (credits) or NotebookLM.
- Source-grounded lookup: NotebookLM (never canonical; docs/09 contract).
- Claude-class second opinion: scripts → Anthropic API or Vertex Claude
  (credits) — GATED by docs/11 §7 cash/reserve rules.
- Parallel work: use subagents for noisy independent tasks (docs/02 §8).

## Verification requirements
- Deterministic validators run 100% of the time on generated questions and
  scores (docs/08 §3–5). You personally check a 5–10% premium sample.
- No content enters bank/ without passing schemas/ validation.

## Study-time protection
- During study blocks: silence by default. Interrupt only for the defined
  moments in docs/05 §5. Minimum 10 minutes of unaided struggle before EXPLAIN.
- OS administration ≤ 25 min/day. If exceeded 3 days in 7, propose simplification.

## Git safety
- Governance files change only via branch + tests + human approval (docs/12).
- Never rewrite git history. Pushes are manual (rule-gated).

## Escalation and failure
- If a tool/script fails twice, stop and report with a one-line diagnosis.
- Harness problems (quota, outage) → docs/13 §5 fallback ladder; never fake
  completion; write failure to logs/.

## Where things live (pointer map — read only what you need)
docs/00 orchestrator · 01 memory · 02 harness · 03 router · 04 coordination ·
05 daily loop · 06 weekly/monthly · 07 academic engine · 08 question/mock ·
09 research/NotebookLM · 10 MCP/free tools · 11 credits · 12 self-improvement ·
13 red team · 14 runbook · 15 model registry.
```

## 6. Profiles — `~/.codex/{cuet,quiet,heavy}.config.toml` (exact files)

Profile mechanics [OFFICIAL VERIFIED]: `codex --profile cuet` loads `~/.codex/config.toml`, then overlays `~/.codex/cuet.config.toml` (top-level keys, one file per profile).

```toml
# ~/.codex/cuet.config.toml — daily profile
model = "gpt-5.5"                    # [VERIFY: /model in TUI for current default; pick the
                                     #  standard-cot default, NOT the premium Astra-class model]
model_reasoning_effort = "medium"    # daily work; see heavy profile for xhigh
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

```toml
# ~/.codex/quiet.config.toml — log entry, quick checks (minimize tokens)
model_reasoning_effort = "low"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

```toml
# ~/.codex/heavy.config.toml — mock post-mortems, weekly review, red team
model_reasoning_effort = "xhigh"     # explicit trigger: docs/03 §6 MCV ≥ 48
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

```toml
# ~/cuet-os/.codex/config.toml — project overrides
sandbox_mode = "workspace-write"

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
# PAT: export GITHUB_PERSONAL_ACCESS_TOKEN in your shell profile, or paste it below
# at deployment and NEVER commit this file. [VERIFY: whether Codex forwards parent
# process env to stdio MCP servers on your installed version; if it does, keep the
# token out of this file entirely.]
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "PASTE-AT-DEPLOYMENT-OR-LEAVE-EMPTY-IF-ENV-INHERITED" }

[mcp_servers.fetch]
command = "uvx"
args = ["mcp-server-fetch"]
```

MCP notes: Codex MCP servers are **stdio** `[mcp_servers.<id>]` entries [OFFICIAL VERIFIED]; older releases required ≥0.34.0 for config.toml MCP [TIER B issue #3441 — one more reason to pin/update]. Allowlist discipline: **≤3 servers**. Remote MCP servers were not supported in earlier releases [TIER B community 2025-08] — re-verify if needed.

## 7. Daily driving commands (verified)

| Need | Command |
|---|---|
| Start | `codex --profile cuet` (TUI) |
| Quick status | `/status` (usage windows), `/permissions` (mode) |
| Resume interrupted work | `codex resume` / `codex resume --last` |
| Headless job (nightly) | `codex exec "..."` in launchd/cron wrappers (docs/12 §7) |
| Attach screenshot/image | `codex --image <file>` or paste |
| Web research | TUI web search (cached default; `--search` live) [OFFICIAL VERIFIED]; project `.codex` network gates apply |
| Generate AGENTS.md scaffold | `/init` (desktop app) |
| Inspect subagent threads | `/agent` |

## 8. Subagents (parallelism) — verified usage

Official: Codex runs subagent workflows — specialized agents spawned **in parallel**, results collected into one response; local clients can define **custom agents with different model configurations and instructions**; `/agent` inspects threads; AGENTS.md/skill instructions can request delegation; subagents consume more tokens and exist to prevent context pollution [OFFICIAL VERIFIED 2026-09-08].

CUET-OS roster (6, cut from V4's 10 — the stronger harness needs fewer):

| Agent | Config | Use |
|---|---|---|
| explorer | low effort | log/file sweeps, bank audits |
| verifier-second | **different family** (see 04 §4) | independent check of high-stakes outputs |
| question-validator | medium | Layer-2 validation runs (08 §4) |
| red-team-first | medium/xhigh | adversarial first pass (13 §3) |
| research-scout | medium | search + capture proposals (09 §2) |
| memory-hygiene | low | ledger consistency proposals |

**[VERIFY] definition format:** create agents under `.codex/agents/` following the current docs page "Agent configuration → subagents" (fetched page confirms capability; exact file schema was not captured — run `codex` docs `/docs/agent-configuration/subagents.md` and copy the reference example on first setup). Fallback that works today with zero config: ask in-session — "spawn subagents to A, B, C in parallel, then collect" — documented behavior.

## 9. Anti-goals of this harness file

No CLAUDE.md, no Claude hooks, no Claude permissions JSON, no `.claude/` directory, no `/compact`-specific advice, no ANTHROPIC_* env plumbing in the harness path. Those were V4's mechanisms; carrying them forward would create silent half-workings. The equivalent surfaces are: AGENTS.md (done), rules (done), profiles (done), sandbox modes (done), scripts (outside harness), launchd (outside harness).
