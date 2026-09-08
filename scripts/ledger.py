#!/usr/bin/env python3
"""ledger.py — single writer for memory ledgers (T0 truth layer).
Subcommands: block | error | state | verify | compact
All writes are append-only; STATE.md is regenerated, never hand-edited."""
import json, os, sys, csv, datetime as dt, tempfile, math
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LED = os.path.join(ROOT, "memory", "ledgers")
STATE = os.path.join(ROOT, "memory", "STATE.md")
TAX = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"]
ROW_REQUIRED = {
    "study_log.jsonl": {"id", "ts", "topic", "minutes", "questions", "correct"},
    "error_log.jsonl": {"id", "ts", "code", "topic", "status"},
    "mock_results.jsonl": {"id", "ts", "scheme_status", "total", "sections", "attempted", "correct", "accuracy_on_attempted", "tentative_errors"},
    "decision_log.jsonl": {"id", "ts", "decision", "evidence_tags", "horizon_notes"},
    "experiment_log.jsonl": {"id", "ts", "date", "hypothesis", "change_files", "branch", "test_window", "metric_before", "metric_after", "redteam_verdict", "decision", "evidence_refs"},
}


def validate_row(name, obj):
    if not isinstance(obj, dict):
        raise ValueError(f"{name}: row must be an object")
    missing = ROW_REQUIRED.get(name, set()) - obj.keys()
    if missing:
        raise ValueError(f"{name}: missing fields {sorted(missing)}")
    try:
        timestamp = dt.datetime.fromisoformat(obj["ts"])
        if timestamp.tzinfo is None:
            raise ValueError
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{name}: ts must be an ISO timestamp with timezone") from None
    if "id" in ROW_REQUIRED.get(name, set()) and (not isinstance(obj["id"], str) or not obj["id"].strip()):
        raise ValueError(f"{name}: id must be a non-empty string")
    if name == "study_log.jsonl":
        values = (obj["minutes"], obj["questions"], obj["correct"])
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in values):
            raise ValueError(f"{name}: minutes/questions/correct must be integers")
        if obj["minutes"] <= 0 or obj["questions"] < 0 or not 0 <= obj["correct"] <= obj["questions"]:
            raise ValueError(f"{name}: invalid study counts")
        if not isinstance(obj["topic"], str) or not obj["topic"].strip():
            raise ValueError(f"{name}: topic must be a non-empty string")
    if name == "error_log.jsonl":
        if obj["code"] not in TAX or obj["status"] not in {"open", "resolved"}:
            raise ValueError(f"{name}: invalid code or status")
        if not isinstance(obj["topic"], str) or not obj["topic"].strip():
            raise ValueError(f"{name}: topic must be a non-empty string")
    if name == "mock_results.jsonl":
        if not isinstance(obj["sections"], dict) or not isinstance(obj["tentative_errors"], dict):
            raise ValueError(f"{name}: sections and tentative_errors must be objects")
        if not isinstance(obj["total"], (int, float)) or isinstance(obj["total"], bool) or not math.isfinite(obj["total"]):
            raise ValueError(f"{name}: total must be numeric")
        if not all(isinstance(obj[key], int) and not isinstance(obj[key], bool) and obj[key] >= 0 for key in ("attempted", "correct")) or obj["correct"] > obj["attempted"]:
            raise ValueError(f"{name}: invalid attempted/correct counts")
        accuracy = obj["accuracy_on_attempted"]
        if accuracy is not None and (not isinstance(accuracy, (int, float)) or isinstance(accuracy, bool) or not math.isfinite(accuracy) or not 0 <= accuracy <= 1):
            raise ValueError(f"{name}: invalid accuracy")
        if not isinstance(obj["scheme_status"], str) or not obj["scheme_status"].strip():
            raise ValueError(f"{name}: scheme_status must be a non-empty string")
        for section in obj["sections"].values():
            counts = ("attempted", "correct", "wrong", "skipped")
            if not isinstance(section, dict) or not all(isinstance(section.get(key), int) and not isinstance(section.get(key), bool) and section[key] >= 0 for key in counts) or section["attempted"] != section["correct"] + section["wrong"] or not isinstance(section.get("marks"), (int, float)):
                raise ValueError(f"{name}: invalid section payload")
        if not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in obj["tentative_errors"].values()):
            raise ValueError(f"{name}: invalid tentative error counts")
    if name == "decision_log.jsonl":
        if not isinstance(obj["decision"], str) or not obj["decision"].strip() or not isinstance(obj["evidence_tags"], list) or not isinstance(obj["horizon_notes"], dict):
            raise ValueError(f"{name}: invalid decision payload")
    if name == "experiment_log.jsonl":
        list_fields = ("change_files", "evidence_refs")
        text_fields = ("date", "hypothesis", "branch", "test_window", "redteam_verdict", "decision")
        if not all(isinstance(obj[key], list) for key in list_fields) or not all(isinstance(obj[key], str) and obj[key].strip() for key in text_fields):
            raise ValueError(f"{name}: invalid experiment payload")
    return obj

def append(name, obj):
    os.makedirs(LED, exist_ok=True)
    obj["ts"] = obj.get("ts") or dt.datetime.now().astimezone().isoformat(timespec="seconds")
    validate_row(name, obj)
    with open(os.path.join(LED, name), "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"appended to {name}: {obj.get('id', '')}")

def read(name):
    p = os.path.join(LED, name)
    if not os.path.exists(p): return []
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.strip(): out.append(validate_row(name, json.loads(line)))
    return out

def cmd_block(args):
    # BLOCK: topic | 50min | 25Q | 18 correct | silly-2,concept-3 | conf: x | next: y
    text = " ".join(args)
    parts = [p.strip() for p in text.split("|")]
    if len(parts) < 4:
        print("format: topic | minutes | questions | correct | [errors] | [confusion] | [next]"); return 2
    try:
        mins = int("".join(c for c in parts[1] if c.isdigit()))
        qs, corr = (int("".join(c for c in parts[i] if c.isdigit())) for i in (2, 3))
    except ValueError:
        print("minutes/questions/correct must contain numbers"); return 2
    if mins <= 0 or qs < 0 or corr < 0 or corr > qs:
        print("minutes must be positive and correct must be between 0 and questions"); return 2
    append("study_log.jsonl", {"id": f"B-{dt.date.today():%Y%m%d-%H%M%S}", "topic": parts[0],
        "minutes": mins, "questions": qs, "correct": corr, "accuracy": round(corr / qs, 3) if qs else None,
        "error_note": parts[4] if len(parts) > 4 else "", "confusion": parts[5].replace("conf:", "").strip() if len(parts) > 5 else "",
        "next": parts[6].replace("next:", "").strip() if len(parts) > 6 else ""})
    return 0

def cmd_error(args):
    # error CODE topic detail...
    if len(args) < 2:
        print("format: error CODE topic [detail]"); return 2
    code, topic = args[0], args[1]
    if code not in TAX:
        print(f"code must be one of {TAX}"); return 2
    append("error_log.jsonl", {"id": f"E-{dt.date.today():%Y%m%d-%H%M%S}", "code": code,
        "topic": topic, "detail": " ".join(args[2:]), "status": "open"})
    return 0

def recent_blocks(days):
    cutoff = dt.datetime.now().astimezone() - dt.timedelta(days=days)
    recent = []
    for block in read("study_log.jsonl"):
        try:
            when = dt.datetime.fromisoformat(block["ts"])
            if when.tzinfo is None:
                when = when.astimezone()
            if when >= cutoff:
                recent.append(block)
        except (KeyError, TypeError, ValueError):
            continue
    return recent

def cmd_state(_args):
    blocks = recent_blocks(14)
    mins = sum(b.get("minutes", 0) for b in blocks)
    errs = read("error_log.jsonl")
    open_errs = [e for e in errs if e.get("status") == "open"]
    mocks = read("mock_results.jsonl")[-5:]
    lines = [
        "# STATE.md (auto-generated — ledgers are truth)", "",
        f"updated: {dt.datetime.now().astimezone():%Y-%m-%d %H:%M}",
        f"study_minutes_14d: {mins}  (target ~14d of day-mode totals)",
        f"open_errors: {len(open_errs)}  top: {Counter(e.get('code') for e in open_errs).most_common(1)[0][0] if open_errs else '-'}",
        f"blocks_logged_7: {len(recent_blocks(7))}",
    ]
    if mocks:
        lines.append(f"last_mock: {mocks[-1].get('total')}  band: see mock_results.jsonl")
    lines += ["", "## warnings", "run bootstrap_check.py for live warnings", "",
              "## open confusions", *[f"- {b['confusion']}" for b in blocks if b.get("confusion")][:5]]
    with open(STATE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"STATE.md regenerated ({len(lines)} lines)")
    return 0

def cmd_verify(_args):
    ok = True
    for name in ["study_log.jsonl", "error_log.jsonl", "mock_results.jsonl", "decision_log.jsonl", "experiment_log.jsonl"]:
        try: n = len(read(name)); print(f"{name}: {n} rows OK")
        except (json.JSONDecodeError, ValueError, TypeError) as e: print(f"{name}: CORRUPT {e}"); ok = False
    headers = {
        "token_ledger.csv": {"date", "category", "task", "engine", "tokens", "est_cost_usd", "evidence_tag", "notes"},
        "credit_ledger.csv": {"date", "account", "balance_before", "delta", "balance_after", "expiry", "status", "engine", "task_ref", "evidence_tag", "notes"},
        "cash_ledger.csv": {"date", "usd", "engine", "task_ref", "approved_by", "evidence_tag", "notes"},
    }
    for name, required in headers.items():
        path = os.path.join(LED, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", newline="") as handle:
            actual = set(csv.DictReader(handle).fieldnames or [])
        if not required <= actual:
            print(f"{name}: INVALID HEADER missing {sorted(required - actual)}"); ok = False
        else:
            print(f"{name}: header OK")
    for name in ["mastery_map.json", "model_health.json"]:
        path = os.path.join(LED, name)
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as handle: json.load(handle)
            print(f"{name}: JSON OK")
        except json.JSONDecodeError as e:
            print(f"{name}: CORRUPT {e}"); ok = False
    return 0 if ok else 1

def cmd_compact(_args):
    archive = os.path.join(os.path.dirname(LED), "archive")
    os.makedirs(archive, exist_ok=True)
    for name in ["study_log.jsonl", "error_log.jsonl"]:
        rows = read(name)
        if len(rows) > 400:
            keep = rows[-200:]; old = rows[:-200]
            with open(os.path.join(archive, f"{name}.{dt.date.today():%Y%m}"), "a", encoding="utf-8") as f:
                f.writelines(json.dumps(r) + "\n" for r in old)
                f.flush(); os.fsync(f.fileno())
            with tempfile.NamedTemporaryFile("w", dir=LED, encoding="utf-8", delete=False) as f:
                f.writelines(json.dumps(r) + "\n" for r in keep)
                f.flush(); os.fsync(f.fileno())
                replacement = f.name
            os.replace(replacement, os.path.join(LED, name))
            print(f"compacted {name}: archived {len(old)}, kept {len(keep)}")
        else:
            print(f"{name}: {len(rows)} rows, no compaction needed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    cmds = {"block": cmd_block, "error": cmd_error, "state": cmd_state, "verify": cmd_verify, "compact": cmd_compact}
    if sys.argv[1] not in cmds:
        print(__doc__); sys.exit(2)
    sys.exit(cmds[sys.argv[1]](sys.argv[2:]))
