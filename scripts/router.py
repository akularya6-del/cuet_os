#!/usr/bin/env python3
"""router.py — deterministic routing precheck (T0). Codex consults this before spending tokens.
Usage: python3 scripts/router.py --task "generate 30 quadratic MCQs" --data --value 6 --unc 2 --err 2 --rev r --imp 6
       --task "switch PE strategy" --value 8 --unc 4 --err 5 --rev h --imp 8
Reads token_ledger.csv (cash this month) and credit_ledger.csv (mode hint) when present."""
import argparse, csv, json, os, sys, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LED = os.path.join(ROOT, "memory", "ledgers")

def cash_this_month():
    p = os.path.join(LED, "cash_ledger.csv")
    if not os.path.exists(p): return 0.0
    m = dt.date.today().strftime("%Y-%m")
    tot = 0.0
    with open(p) as f:
        for row in csv.DictReader(f):
            if str(row.get("date", "")).startswith(m):
                try: tot += float(row.get("usd", 0))
                except ValueError: pass
    return tot

def credit_mode(today=None):
    p = os.path.join(LED, "credit_ledger.csv")
    if not os.path.exists(p): return "NORMAL", None
    latest = {}
    epochs = {}
    with open(p) as f:
        for row in csv.DictReader(f):
            account = row.get("account", "A")
            latest[account] = row
            currency = row.get("currency", "").strip()
            prior = epochs.get(account)
            if not currency:
                epochs[account] = None
                continue
            try:
                before = float(row["balance_before"])
                delta = float(row["delta"])
                after = float(row["balance_after"])
            except (KeyError, TypeError, ValueError):
                epochs[account] = None
                continue
            if before < 0 or after < 0 or abs(before + delta - after) > 0.000001:
                epochs[account] = None
                continue
            if prior is None or prior["currency"] != currency:
                epochs[account] = {"currency": currency, "capacity": max(before, after), "balance": after}
            else:
                prior["capacity"] = max(prior["capacity"], before, after)
                prior["balance"] = after
    ratios = []
    days_left = []
    for account, row in latest.items():
        if row.get("status", "active").lower() != "active":
            continue
        epoch = epochs.get(account)
        if not epoch or epoch["capacity"] <= 0:
            return "EMERGENCY", latest
        try:
            days_left.append((dt.date.fromisoformat(row["expiry"]) - (today or dt.date.today())).days)
        except (KeyError, TypeError, ValueError):
            return "EMERGENCY", latest
        ratios.append(epoch["balance"] / epoch["capacity"])
    if not ratios:
        return "EMERGENCY", None
    ratio = min(ratios)
    if ratio <= 0 or min(days_left) < 0: return "EMERGENCY", latest
    if ratio < 0.30: return "PEAK", latest
    if min(days_left) <= 30: return "EXPIRING", latest
    if ratio < 0.60: return "HEAVY", latest
    return "NORMAL", latest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--data", action="store_true", help="output is data (JSON/CSV) → shell boundary applies")
    ap.add_argument("--value", type=float, default=5); ap.add_argument("--unc", type=float, default=3)
    ap.add_argument("--err", type=float, default=3); ap.add_argument("--rev", choices=["r", "h"], default="r")
    ap.add_argument("--imp", type=float, default=5); ap.add_argument("--sensitive", action="store_true")
    a = ap.parse_args()
    mcv = a.value * a.unc * a.err * (1.0 if a.rev == "h" else 0.5) * a.imp
    mode, _ = credit_mode()
    if mcv < 20: tier = "T0/T1 (script or free tool)"
    elif mcv < 48: tier = "T2/T3 (cheap or workhorse)"
    elif mcv < 100: tier = "T4 (strong, name the trigger)"
    elif mcv < 200: tier = "T4 default; T5 if disagreement material"
    else: tier = "T6 panel + human informed before spend"
    note = []
    if a.data and mcv >= 48: tier = "shell boundary overrides: run via scripts at T2, sample-check 5-10%"
    if a.sensitive: note.append("PERSONAL/HIGH data: DeepSeek/GLM/Qwen/NotebookLM/proxy FORBIDDEN (13 §4)")
    if mode in ("PEAK", "EMERGENCY"): note.append(f"reservoir mode {mode}: credits restricted (11 §4)")
    if mode == "EXPIRING": note.append("reservoir mode EXPIRING: front-load score-bearing durable assets before expiry (11 §4)")
    if cash_this_month() > 40: note.append(f"cash this month ${cash_this_month():.2f}: approaching cap, gates tighten")
    in_codex = not tier.startswith(("T0", "shell"))
    out = {"task": a.task, "mcv": round(mcv, 1), "tier": tier, "engine": None,
           "profile": "heavy" if mcv >= 48 and in_codex else ("cuet" if in_codex else None),
           "est_cost_usd": None, "gate_required": mcv >= 48,
           "mode": mode,
           "reason": f"MCV={mcv:.0f} (v{a.value} u{a.unc} e{a.err} rev:{a.rev} i{a.imp})",
           "notes": note, "est_cost": "see config/budget.json price table (tagged)"}
    print(json.dumps(out, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
