#!/usr/bin/env python3
"""bootstrap_check.py — deterministic morning/system check (T0; zero AI).
Usage: python3 scripts/bootstrap_check.py --quick|--full
Exit codes: 0 ok, 1 warnings present. All output is human-readable lines for Codex to read."""
import json, os, sys, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")
LED = os.path.join(MEM, "ledgers")
STATE = os.path.join(MEM, "STATE.md")

def warn(msg): print(f"WARN: {msg}")
def info(msg): print(f"OK: {msg}")

def file_age_days(path):
    if not os.path.exists(path): return None
    mtime = os.path.getmtime(path)
    return (dt.datetime.now() - dt.datetime.fromtimestamp(mtime)).days

def main():
    if any(arg not in {"--quick", "--full"} for arg in sys.argv[1:]) or len(sys.argv) > 2:
        print("usage: python3 scripts/bootstrap_check.py --quick|--full")
        return 2
    quick = "--quick" in sys.argv
    warnings = 0
    # 1) STATE.md freshness
    age = file_age_days(STATE)
    if age is None:
        warn("memory/STATE.md missing — run: python3 scripts/ledger.py state"); warnings += 1
    elif age > 2:
        warn(f"STATE.md is {age}d old (stale=unknown) — regenerate with ledger.py state"); warnings += 1
    else:
        info(f"STATE.md fresh ({age}d)")
    # 2) ledger presence + integrity
    for name in ["study_log.jsonl", "error_log.jsonl", "token_ledger.csv", "credit_ledger.csv", "cash_ledger.csv"]:
        p = os.path.join(LED, name)
        if not os.path.exists(p):
            warn(f"ledger missing: ledgers/{name}"); warnings += 1
    for jl in ["study_log.jsonl", "error_log.jsonl", "mock_results.jsonl"]:
        p = os.path.join(LED, jl)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if line.strip(): json.loads(line)
                info(f"{jl} parses clean")
            except json.JSONDecodeError as e:
                warn(f"{jl} corrupted at line {i}: {e} — restore from backups/"); warnings += 1
    # 3) credit expiry warnings
    cl = os.path.join(LED, "credit_ledger.csv")
    if os.path.exists(cl):
        import csv
        balances = {}
        with open(cl) as f:
            for row in csv.DictReader(f):
                balances[row.get("account", "A")] = row
        for acct, row in balances.items():
            exp = row.get("expiry", "")
            if exp:
                try:
                    days = (dt.date.fromisoformat(exp) - dt.date.today()).days
                    bal = row.get("balance_after", row.get("balance", "?"))
                    if days < 45: warn(f"Account {acct}: credit expires in {days}d, balance ${bal} — check 11 §3 branch"); warnings += 1
                    else: info(f"Account {acct}: ${bal} left, expires in {days}d")
                except ValueError:
                    warn(f"Account {acct}: expiry '{exp}' unparseable — verify in console"); warnings += 1
    # 4) marking scheme confirmation state
    ms = os.path.join(ROOT, "config", "marking_scheme.json")
    if os.path.exists(ms):
        cfg = json.load(open(ms))
        if cfg.get("status") == "REQUIRES-2027-CONFIRMATION":
            info("marking_scheme: 2026 baseline active, 2027 confirmation still pending (expected Dec 2026-Feb 2027)")
    if quick:
        print(f"bootstrap quick done: {warnings} warning(s)"); return 1 if warnings else 0
    # full: model health flags
    mh = os.path.join(LED, "model_health.json")
    if os.path.exists(mh):
        for eng, st in json.load(open(mh)).items():
            if st.get("status") == "degraded":
                warn(f"engine degraded: {eng} — router will route around"); warnings += 1
    print(f"bootstrap full done: {warnings} warning(s)")
    return 1 if warnings else 0

if __name__ == "__main__":
    sys.exit(main())
