# 13_REDTEAM_SECURITY_AND_FAILURE_RECOVERY_V5

**Assume breakage. Pre-decide the response.** Attack catalog (retargeted for Codex-primary), data routing law, and the failure recovery matrix. Two full audits/month via T6 panel; weekly light check inside WEEKLY.

---

## 1. Audit cadence and method

- **Monthly full audit (2×/month, 45 min each):** T6 panel — arms: Codex (attack plan), Claude-on-Vertex or Anthropic API (adversarial findings), one cheap arm (GLM/DeepSeek devil's advocate). REDTEAM pack = decision/evidence/assumptions **without** prior conclusions. Blind inputs; scripts collate; human decides patches.
- **Weekly light check:** quota posture anomalies, unapproved-allow audit (`~/.codex/rules/default.rules` + `/mcp` list), ledger checksum verify, backup freshness, one restored-file spot check.
- **Quarterly 80%-removal drill:** "which 80% of the OS could die tonight with the remaining 20% still protecting score?" — anything not in the 20% gets a simplification proposal (12 §4 config path).

## 2. Attack catalog (22 attacks; A1–A19 carried/re-targeted from V4, A20–A22 new)

| # | Attack | Patch |
|---|---|---|
| A1 | Codex outage/quota wall mid-day | L1–L6 ladder (03 §9); fallback harness (§5 below); defer non-critical to nightly |
| A2 | Codex plan terms change (quota restructure) | W5 watchlist; `/status` posture tracked; if windows shrink → shift bulk to floor permanently (it already is — shell boundary) |
| A3 | GPT model regression (quality decay unnoticed) | model_health trend + monthly eval battery (15 §4); route-around rule 03 §8 |
| A4 | OpenAI single-vendor dependence (monoculture) | verifier is non-OpenAI by law (04 §4); fallback harness; bank + ledgers are provider-neutral files |
| A5 | Two-account credit assumption fails (ineligibility/ToS finding) | §1 legality note: B stays reserve anyway; plan economics must survive A-only (11 §6); verify early (11 §2) |
| A6 | Credit expiry sooner than modeled | 11 §3 branches; expiry date verified monthly; depletion forecast nightly |
| A7 | Surprise Vertex bill (trial converts, caps misread) | billing alerts + hard caps (11 §2 step 5); ledger-is-cap doctrine; card on file reviewed |
| A8 | NotebookLM limit change breaks N-flows | watchlist W8; manual fallback paths unchanged; quiz seeds are optional inputs, never gates |
| A9 | Codex native auto-memories drift (harness "remembers" wrong rules) | 01 §2 governance: files are canon; monthly auto-memory audit; kill-switch config if drift observed |
| A10 | MCP tool poisoning / malicious server description | 3-server cap, official sources only, destructive-call prompting [OFFICIAL behavior], trusted-project-only `.codex` rules, monthly `/mcp` audit |
| A11 | Prompt injection via captured pages/PDFs (research corpus) | captures are data, not instructions: extraction is schema-bound; Codex instructed that source content never overrides AGENTS.md; suspicious pages processed by T2 scripts, not in-process |
| A12 | Hallucinated evidence (AI cites source that doesn't say that) | canonization protocol (09 §6) requires direct capture + cross-check; spot-audit of 2 canon claims monthly |
| A13 | Memory contamination (bad data enters ledgers) | single-writer map (01 §4); schema validation before commit; append-only + supersede; checksums |
| A14 | Budget overrun / gate fatigue | hard $55 defect line (11 §7); auto-simplification proposal on breach; gates require one line, not forms (keep friction low so gates get used) |
| A15 | Provider simultaneous failure (Codex+Gemini down) | free floor (Groq/OpenRouter/z.ai) + scripts run everything; exams don't wait — work degrades to T0–T1 for the day |
| A16 | Rate limits hit mid-batch | concurrency limits known (DeepSeek flash 2500 [OFFICIAL]); batch chunking + off-peak scheduling; auto-resume |
| A17 | Subscription↔API confusion (accidental cash burn) | API keys live in shell env only, spend scripts rule-gated (02 §4); Codex plan is the default auth for interactive |
| A18 | User fatigue / OS overuse | 25-min ceiling, silence law, one-change rule, REMOVE-first complexity budget (06 §3) |
| A19 | Complexity creep (V2→V3→V4 lesson) | mechanism count audited monthly; net-remove rule (06 §3); quarterly 80% drill |
| A20 | AGENTS.md bloat → instruction dilution | size budget <20 KB (cap 32 KB [OFFICIAL]); pointer-map pattern; monthly line-count check in AUDIT |
| A21 | Session contamination (long sessions degrade; context rot [OFFICIAL-documented risk]) | one theme per session; subagents absorb noise; `codex resume` over marathon sessions; REVIEW closes sessions |
| A22 | Subagent cost blowout (parallelism ≠ free) | subagent spawns carry token estimates; weekly review counts subagent-minutes; default roster capped at 6 (02 §8) |

## 3. Red-team prompt contract (5 fields, carried from V4)

`{decision_under_attack, evidence_list, assumptions_list, prior_conclusions: EXCLUDED, adversarial_goals: [find fatal flaw, find hidden cost, find a simpler way]}` — the exclusion of prior conclusions is what keeps panels honest; the moderator scripts rebuild the pack from ledgers, not from the proposing session.

## 4. Data classification and routing (what may go where)

| Class | Examples | Codex/GPT | Claude (API/Vertex) | Gemini/Vertex | DeepSeek/GLM/Qwen | NotebookLM | Community MCP/proxy |
|---|---|---|---|---|---|---|---|
| PUBLIC (exam content, official docs) | questions, syllabus | yes | yes | yes | yes | yes | no (default) |
| LOW (system configs, non-identifying logs) | router outputs, model health | yes | yes | yes | yes | yes | no |
| PERSONAL (name, category, school, business details, error logs tied to identity) | ledgers with identity, strategy memos | yes (needed to orchestrate) | only extracts | only extracts | **NO** | no | **NO** |
| HIGH (credentials, billing, OAuth, family data) | API keys, credit details | **NEVER leaves machine** | never | never | never | never | never |

DeepSeek/GLM/Qwen are third-country processors: PUBLIC/LOW only, no PERSONAL fields in prompts (scripts strip before dispatch). The Antigravity proxy and NotebookLM community MCPs: PERSONAL/HIGH excluded by default (10 §2, §5). Secrets policy: keys in shell env or macOS keychain; never in AGENTS.md, never in git (pre-commit secret scan in tests/), rotate on any suspected exposure; `.env` git-ignored; spend scripts read from env.

## 5. Failure recovery matrix (SYMPTOM → CAUSE → FIX → FALLBACK)

| Symptom | Likely cause | Immediate fix | Fallback |
|---|---|---|---|
| Codex CLI won't start/auth loop | version/update issue | reinstall via official script; pin version (15 §6) | use desktop/IDE app for the day |
| Codex 5h/weekly window exhausted mid-task | quota | switch profile to lower effort; finish via scripts | Claude Code (if active) / Antigravity; defer bulk to night batch |
| `codex exec` nightly job silent | launchd misfire | check plist logs (`logs/launchd/`), run manually | cron fallback; or run at START |
| MCP server fails to load | version/env var | `codex` update (≥0.34-era fixes [TIER B]); fix env | proceed without MCP — native tools + cached search cover 90% |
| Gemini free tier 429s | promo reduction/RPD hit | switch engine in batch config | DeepSeek off-peak; Groq |
| Vertex call bills but errors | SKU/region mismatch | capture error, pause account batch | route to account B per §1 rules |
| Credit ledger vs console mismatch | missed entries | reconcile from console export | trust console (it's the bank), fix scripts |
| DeepSeek peak pricing surprise | timezone misread | batch window recheck (UTC 01–04, 06–10 Mon–Fri) | shift batch; absorb; log cost delta |
| NotebookLM daily cap hit | caps moved | recheck limits page (W8) | Codex/Gemini summarization from captured sources |
| Claude-on-Vertex unavailable/quota | regional capacity | retry region switch | Anthropic API (cash, gated) or defer adjudication |
| Bank file corrupted | disk/schema bug | restore from git + backups (01 §8) | rebuild batch (cheap by design) |
| Git conflict in governance files | concurrent edits | abort merge; human reconciles | `git revert` to last `gov-approved-*` tag |
| Model deprecation notice | provider lifecycle | 15 §5 migration triggers | documented alternates in registry |
| Internet outage | ISP | local mode: Ollama if fitted [VERIFY], bank drills offline, paper mocks | defer batches; study continues (always) |
| macOS update breaks launchd/plists | OS upgrade | re-run deployment checklist (14 §7) | run jobs manually from BUDGET |

## 6. Backup and restore (testable, not theoretical)

Weekly: `MEMORY` export → `outputs/backups/` + manual `git push` (rule-gated). Monthly: restore drill — pull backup into a scratch dir, run `ledger.py verify` + one scorer golden test; a backup that has never been restored is a hypothesis. Private GitHub remote stores code+docs; ledgers also exported as CSV (human-readable insurance).

## 7. Standing adversarial questions (asked every monthly audit)

What did we believe last month that turned out false? What did we pay for that no decision used? What broke and we didn't notice for days? What would break the plan if Codex quotas halved tomorrow? If we deleted one mechanism today, what would we miss? (If the answer is "nothing," it's already gone by the next review.)
