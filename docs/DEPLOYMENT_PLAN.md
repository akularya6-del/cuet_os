# CUET-OS V5 Deployment Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task.

**Goal:** Turn the supplied V5 package into a clean, local, first-boot-ready CUET-OS installation without paid calls or fabricated external state.

**Architecture:** Preserve the supplied documents and scripts as the governing design. Normalize files into the documented tree, add only the deterministic schemas/configuration/tests required for safe first use, and leave credentialed or billable integrations disabled with explicit human actions.

**Tech Stack:** Python 3 stdlib, JSON/JSONL/CSV, Codex CLI configuration, Git.

**Spec:** `AGENTS.md`, `docs/00_CODEX_MASTER_ORCHESTRATOR_V5.md`, and V5 docs 01–15.

## Global Constraints

- Deterministic scripts commit truth; models only propose.
- Preserve supplied V5 content and uncertainty tags.
- No secrets, paid calls, browser authorization, public remote, or history rewriting.
- Governance remains human-gated; this deployment is the owner-requested initial installation.
- Optional integrations stay disabled unless locally verifiable and credential-free.

---

### Task 1: Normalize the package

**Files:** Move the sixteen numbered V5 documents to `docs/`; move evidence notes to `research/`; move the PDF to `manual/`; copy starter scripts to `scripts/`; retain canonical `AGENTS.md` and `INDEX.md`.

**Produces:** Exactly one canonical copy of each supplied artifact at its documented path.

- [ ] Record present, misnamed, missing-required, optional, and auth-required inventory.
- [ ] Normalize supplied filenames without changing contents.
- [ ] Create only V5-referenced directories.
- [ ] Verify all 00–15 docs and five scripts exist exactly once.

### Task 2: Establish deterministic behavior with tests

**Files:** `tests/test_core.py`; minimally patch supplied scripts only for demonstrated defects.

**Produces:** Runnable checks for ledger append/read/state/verify, bootstrap, routing, scoring, and governance validation.

- [ ] Write tests against isolated temporary project roots and run them to expose missing or broken behavior.
- [ ] Apply the smallest fixes required by observed failures.
- [ ] Run Python compilation and the complete test suite.

### Task 3: Seed state, configuration, and bank validation

**Files:** `memory/ledgers/*`, `memory/STATE.md`, `config/marking_scheme.json`, `config/subjects.json`, `config/budget.json`, `schemas/question.schema.json`, and a minimal structural validator only if the supplied scripts do not provide one.

**Produces:** Valid empty ledgers with explicit CSV headers, derived STATE.md, uncertainty-tagged config, and a closed question-bank gate.

- [ ] Derive exact headers and values from docs and script readers.
- [ ] Initialize empty JSONL/JSON ledgers without invented observations.
- [ ] Add a JSON Schema matching docs/08 and keep API generation disabled.
- [ ] Run ledger verify/state and bootstrap quick; resolve actionable errors.

### Task 4: Configure the local Codex harness safely

**Files:** `.codex/config.toml`, `.codex/rules/cuet.rules`, `~/.codex/AGENTS.md`, and supported profile configuration in `~/.codex/config.toml` or version-supported equivalents.

**Produces:** Workspace-write project baseline, daily/quiet/heavy profiles, and prompt gates for push/destructive/spend commands.

- [ ] Record installed Codex version and inspect local help/current config behavior.
- [ ] Preserve unrelated existing global Codex configuration and never print secrets.
- [ ] Use current supported profile/rules syntax; do not pin an unverified model.
- [ ] Leave GitHub/fetch/NotebookLM and provider APIs disabled when auth/runtime is absent.

### Task 5: Git safety and acceptance verification

**Files:** `.gitignore`, `logs/DEPLOYMENT_REPORT.md`, Git repository metadata.

**Produces:** A local initial commit and evidence-backed deployment report.

- [ ] Initialize Git if absent and exclude secrets/caches/temp outputs without excluding canonical memory.
- [ ] Run full syntax, tests, ledger, bootstrap, governance, secret, and status checks.
- [ ] Classify every night function; install no launchd job whose implementation is absent.
- [ ] Commit locally only after green checks; create `gov-approved-<date>` only when governance validation is green.
- [ ] Report exact remaining human/auth actions and first-use command.
