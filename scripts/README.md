# Starter Scripts — CUET OS V5 (the "commit truth" layer)

Deterministic, zero-AI helpers referenced by the 16 implementation files. Copy into
`~/cuet-os/scripts/` and run the test smoke below. Python 3.9+, stdlib only.

| Script | Command | Purpose (doc reference) |
|---|---|---|
| `bootstrap_check.py` | `python3 scripts/bootstrap_check.py --quick` | Morning T0 check: STATE freshness, ledger integrity, credit-expiry warnings (00 §6, 05 §2) |
| `ledger.py` | `python3 scripts/ledger.py block "quadratic | 50min | 25Q | 18 correct | concept-3 | conf: discriminant | next: retest Thu"` | Single-writer append to ledgers; `state` regenerates STATE.md; `verify`; `compact` (01 §3–4) |
| `router.py` | `python3 scripts/router.py --task "generate 30 MCQs" --data --value 6 --unc 2 --err 2 --rev r --imp 6` | Deterministic MCV precheck → tier recommendation JSON (03 §2, §5) |
| `scorer.py` | `python3 scripts/scorer.py mock_answers.csv` | Zero-AI mock scoring from official key (+5/−1 from config), appends mock_results.jsonl (08 §5) |
| `validate_change.py` | `python3 scripts/validate_change.py` | Governance gate: English-only check, secret scan, AGENTS.md size budget (12 §6, 13 §2-A20) |

Smoke test (after copying into a repo with the memory/ tree):

```bash
python3 scripts/ledger.py block "test | 50min | 25Q | 18 correct | concept-2 | conf: none | next: x"
python3 scripts/ledger.py state && python3 scripts/ledger.py verify
python3 scripts/validate_change.py
python3 scripts/bootstrap_check.py --quick
```

**Not included by design:** API-calling batch scripts (question generation, DeepSeek/Gemini
dispatch, credit probes). They require your keys and engine choices at deployment time
(02 §6 env setup, 11 §2 verification). Codex will scaffold them against the schemas on
first run of the DRILL workflow — the shell boundary (00 §2) is the contract they implement.
