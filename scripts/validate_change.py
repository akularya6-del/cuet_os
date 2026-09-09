#!/usr/bin/env python3
"""validate_change.py — governance gate (T0). Run before any config/governance commit.
Checks: 1) no Chinese/CJK chars in docs (language rule), 2) no obvious secrets,
3) AGENTS.md size budget (<20480 bytes; hard cap 32768), 4) ledger JSONL still parse,
5) marking_scheme.json not edited without NTA tag change.
Usage: python3 scripts/validate_change.py [paths...]   (default: AGENTS.md config/ memory/)"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
SECRET = re.compile(r"(sk-(?:ant-|proj-)?[A-Za-z0-9_\-]{16,}|AIza[A-Za-z0-9_\-]{30,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})")

def fail(msg): print(f"FAIL: {msg}"); return 1
def ok(msg): print(f"ok: {msg}"); return 0

def main():
    paths = sys.argv[1:] or ["."]
    rc = 0
    for p in paths:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            rc |= fail(f"{p}: missing"); continue
        if os.path.isdir(full):
            for dp, dns, fns in os.walk(full):
                dns[:] = [name for name in dns if name not in {".git", ".pytest_cache", ".venv", "__pycache__"}]
                for fn in fns:
                    if fn.endswith((".md", ".json", ".jsonl", ".csv", ".toml", ".rules", ".py", ".html")):
                        rc |= check(os.path.join(dp, fn), os.path.relpath(os.path.join(dp, fn), ROOT))
        else:
            rc |= check(full, p)
    if os.path.exists(os.path.join(ROOT, "AGENTS.md")):
        size = os.path.getsize(os.path.join(ROOT, "AGENTS.md"))
        if size > 32768: rc |= fail(f"AGENTS.md {size}B exceeds 32KiB cap")
        elif size > 20480: rc |= fail(f"AGENTS.md {size}B exceeds 20KB budget (raise cap consciously or split)")
        else: rc |= ok(f"AGENTS.md {size}B within budget")
    marking = os.path.join(ROOT, "config", "marking_scheme.json")
    if os.path.exists(marking):
        try:
            cfg = json.load(open(marking, encoding="utf-8"))
            status, evidence = cfg.get("status"), cfg.get("evidence_tag", "")
            historical_values = (cfg.get("correct"), cfg.get("wrong"), cfg.get("unanswered"), cfg.get("baseline_cycle")) == (5, -1, 0, 2026)
            if status == "REQUIRES-2027-CONFIRMATION" and "2027" in evidence and historical_values:
                rc |= ok("marking_scheme: historical baseline remains gated")
            elif status == "OFFICIAL-VERIFIED-2027" and "OFFICIAL VERIFIED" in evidence and cfg.get("baseline_cycle") == 2027:
                rc |= ok("marking_scheme: 2027 verification tag present")
            else:
                rc |= fail("marking_scheme: invalid status/evidence gate")
        except (OSError, json.JSONDecodeError):
            rc |= fail("marking_scheme: invalid JSON")
    print("validate_change:", "PASS" if rc == 0 else "FAIL")
    return rc

def check(full, rel):
    rc = 0
    try:
        text = open(full, encoding="utf-8").read()
    except (UnicodeDecodeError, IsADirectoryError):
        return ok(f"{rel}: binary/skip")
    if CJK.search(text): rc |= fail(f"{rel}: CJK characters found (English-only rule)")
    if SECRET.search(text): rc |= fail(f"{rel}: apparent API secret committed")
    if rel.endswith(".jsonl"):
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                rc |= fail(f"{rel}:{number}: invalid JSONL ({exc.msg})")
    return rc

if __name__ == "__main__":
    sys.exit(main())
