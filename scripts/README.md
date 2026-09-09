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
| `dispatch.py` | `.venv/bin/python scripts/dispatch.py --task volume --prompt "..."` | Dry-run-first Account-A Vertex Gemini router; execution requires the explicit approval cap |
| `import_legacy.py` | `python3 scripts/import_legacy.py ~/Desktop/CUET_OS_2027` | Review or idempotently apply the one-day-shifted legacy diagnostic import |

Smoke test (after copying into a repo with the memory/ tree):

```bash
python3 scripts/ledger.py block "test | 50min | 25Q | 18 correct | concept-2 | conf: none | next: x"
python3 scripts/ledger.py state && python3 scripts/ledger.py verify
python3 scripts/validate_change.py
python3 scripts/bootstrap_check.py --quick
```

Install the pinned Vertex SDK locally with
`python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Account B remains
rejected until its scheduled human review. Question generation remains gated by the bank schema
and validators; dispatcher output is never admitted directly into `bank/`.
