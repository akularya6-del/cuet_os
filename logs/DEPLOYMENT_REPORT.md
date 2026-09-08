# CUET-OS V5 deployment record — 2026-09-08

## Inventory

| Class | Result |
|---|---|
| PRESENT | `AGENTS.md`, `INDEX.md`, sixteen V5 docs, evidence notes, PDF manual, five starter scripts, cover asset [LOCAL VERIFIED 2026-09-08] |
| PRESENT BUT MISPLACED | Docs, manual, evidence notes, and starter scripts arrived in package/staging locations and were moved to their V5 runtime paths without duplicate canonical copies. [LOCAL VERIFIED 2026-09-08] |
| MISSING BUT REQUIRED | Config, ledgers, schemas, tests, Codex project config/rules, derived state, and Git metadata were absent and have been created. [LOCAL VERIFIED 2026-09-08] |
| OPTIONAL / SPEC-ONLY | Custom subagent definitions, allocator/mastery/scheduler/pack/bank-audit/credit-audit/dispatch/router-report scripts, API batch runners, and launchd plists were not supplied. [LOCAL VERIFIED 2026-09-08] |
| REQUIRES HUMAN/AUTH | Google credit console verification, optional provider keys/projects, optional GitHub auth/private remote, and any paid SKU test. [UNKNOWN until human verification] |

## Normalization

- The canonical V5 documents are `docs/00_...` through `docs/15_...`; all sixteen are present once. [LOCAL VERIFIED 2026-09-08]
- The manual is under `manual/`, evidence notes under `research/`, and deterministic scripts under `scripts/`. [LOCAL VERIFIED 2026-09-08]
- `AGENTS.md` was preserved from the supplied package; it matches the V5 bootstrap intent and was not regenerated. [LOCAL VERIFIED 2026-09-08]
- `INDEX.md` and docs/15 were updated only to correct moved-file paths. [LOCAL VERIFIED 2026-09-08]

## Supplied-script defects repaired

- `ledger.py error` crashed on missing arguments; it now fails with usage status. [LOCAL VERIFIED 2026-09-08]
- Impossible or structurally invalid ledger rows were accepted; append and verify now enforce the minimum per-ledger structure, and correct answers must be between zero and question count. [LOCAL VERIFIED 2026-09-08]
- STATE's “14d/7” figures counted records rather than dates and its top error was lexical; date windows and frequency counting are now deterministic. [LOCAL VERIFIED 2026-09-08]
- Compaction targeted an uncreated `memory/ledgers/archive` and rewrote active truth non-atomically; it now creates governed `memory/archive`, flushes the archive, and atomically replaces the active file. [LOCAL VERIFIED 2026-09-08]
- Ledger verification ignored CSV headers and JSON ledgers; it now checks required headers plus mastery/model-health JSON. [LOCAL VERIFIED 2026-09-08]
- `scorer.py` silently guessed the marking scheme and accepted malformed/non-finite answer CSV; it now fails closed, validates inputs before append, and records wrong answers as unclassified instead of inventing E7. [LOCAL VERIFIED 2026-09-08]
- `router.py` made reservoir mode depend on CSV order, pooled dormant credit, and omitted contract fields; it now evaluates active balance against its active capacity and emits nullable engine/cost fields rather than inventing provider availability or prices. [LOCAL VERIFIED 2026-09-08]
- `validate_change.py` advertised JSONL verification but skipped JSONL and most of the project; it now scans the project, recognizes additional common secret forms, parses JSONL, and enforces the marking-scheme evidence gate. [LOCAL VERIFIED 2026-09-08]
- No L1 question validator was supplied; `validate_questions.py` now enforces the documented top-level and nested structure and blocks L2-unvalidated active questions. [LOCAL VERIFIED 2026-09-08]

## Harness and MCP state

- Codex CLI 0.153.4 is installed and ChatGPT login is active. [LOCAL VERIFIED 2026-09-08]
- `cuet`, `quiet`, and `heavy` overlays load under the installed CLI; no model is pinned, so current/base model selection remains authoritative. [LOCAL VERIFIED 2026-09-08]
- Project sandbox/approval baseline is workspace-write/on-request; push, recursive deletion, and future spend-script prefixes are prompt-gated. [LOCAL VERIFIED 2026-09-08]
- Inherited NotebookLM, memory-sidecar, unrelated security, node tool, and Ruflo MCP entries are disabled only inside CUET-OS. Ruflo was disabled after an observed 30-second handshake timeout and because this CLI reports ToolSearch removed. [LOCAL VERIFIED 2026-09-08]
- GitHub and fetch MCP are not enabled. The unofficial NotebookLM MCP is not active in this project. [LOCAL VERIFIED 2026-09-08]

## Night-job classification

| Function | Status | Decision |
|---|---|---|
| Memory/state maintenance | READY manually (`ledger.py compact/state`) | No launchd job during Days 1–2 pilot. |
| Off-peak question batches | BLOCKED BY API/AUTH + MISSING IMPLEMENTATION | Disabled; bank validator remains closed. |
| Credit/budget audit | SPEC-ONLY / MISSING IMPLEMENTATION | Manual ledger/console verification only. |
| Model-health probe | SPEC-ONLY / MISSING IMPLEMENTATION | Only locally observed Codex health is recorded. |
| Improvement proposal | SPEC-ONLY / MISSING IMPLEMENTATION | No unattended `codex exec` job during pilot. |

No launchd jobs were installed. [LOCAL VERIFIED 2026-09-08]

## First-boot evidence

`codex --profile cuet exec START` loaded the project instructions, ran `python scripts/bootstrap_check.py --quick`, read `memory/STATE.md` and docs/05, derived “no study entry logged” from the empty ledger, and presented exactly the five asked check-in fields. [LOCAL VERIFIED 2026-09-08]

Bootstrap currently returns its documented warning status because both exact Google credit expiry fields are `UNKNOWN`; ledger parsing and marking config checks pass. [LOCAL VERIFIED 2026-09-08]

## Remaining human actions

1. In Google Cloud Billing, verify account A current balance/exact expiry and account B activation/current balance/exact expiry; record covered SKUs, project IDs, regions, and billing alerts. Do not run a billable test until explicitly approved. [VERIFY]
2. If optional DRILL generation or external verification is wanted after the pilot, provide the chosen provider credentials through environment/keychain storage and approve any billable smoke separately. [VERIFY]
3. Review the pre-existing user-level `~/.codex/config.toml`: secret-named Anthropic values are stored directly there and should be migrated to a safer local secret mechanism without printing them. This deployment did not alter those unrelated values. [LOCAL OBSERVED 2026-09-08]
4. A private Git remote is optional and remains unconfigured; authenticate and authorize it only when backup pushes are desired. [UNKNOWN]

First use: `cd /Users/racoon/Desktop/wow/cuet_os && codex --profile cuet`, then type `START`.
