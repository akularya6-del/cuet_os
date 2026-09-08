#!/usr/bin/env python3
"""scorer.py — deterministic mock scorer (T0; ZERO AI). +5/-1 baseline from config/marking_scheme.json.
Usage: python3 scripts/scorer.py mock_answers.csv
CSV columns: qno,subject,topic,correct_index (from official key),student_index (blank if unattempted),time_sec
Outputs: total, per-section, accuracy, attempt rate, error matrix proposal; appends mock_results.jsonl."""
import csv, json, os, sys, datetime as dt, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_scheme():
    p = os.path.join(ROOT, "config", "marking_scheme.json")
    if os.path.exists(p):
        cfg = json.load(open(p))
        return cfg.get("correct", 5), cfg.get("wrong", -1), cfg.get("unanswered", 0), cfg.get("status", "VERIFIED")
    raise FileNotFoundError("config/marking_scheme.json is required; scorer will not guess")

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    try:
        correct, wrong, unanswered, status = load_scheme()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FATAL: {exc}"); return 1
    try:
        with open(sys.argv[1], encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"qno", "subject", "topic", "correct_index", "student_index", "time_sec"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                print(f"FATAL: missing CSV columns: {', '.join(sorted(missing))}"); return 1
            rows = list(reader)
    except OSError as exc:
        print(f"FATAL: {exc}"); return 1
    if not rows:
        print("FATAL: answer CSV is empty"); return 1
    if len({r["qno"].strip() for r in rows}) != len(rows):
        print("FATAL: duplicate qno values"); return 1
    for r in rows:
        key, stu = r["correct_index"].strip(), r["student_index"].strip()
        if key not in {"0", "1", "2", "3", "4"} or (stu and stu not in {"0", "1", "2", "3", "4"}):
            print(f"FATAL: row {r['qno']} has invalid answer index"); return 1
        try:
            value = float(r["time_sec"])
            if not math.isfinite(value) or value < 0: raise ValueError
        except ValueError:
            print(f"FATAL: row {r['qno']} has invalid time_sec"); return 1
    sections = {}
    total = 0
    errors = {"unclassified_wrong": 0}
    for r in rows:
        sec = r.get("subject", "general").strip()
        s = sections.setdefault(sec, {"attempted": 0, "correct": 0, "wrong": 0, "skipped": 0, "marks": 0})
        key = r.get("correct_index", "").strip()
        stu = r.get("student_index", "").strip()
        if not key:  # malformed row = hard stop; scorer must never guess
            print(f"FATAL: row {r.get('qno')} missing correct key"); return 1
        if stu == "":
            s["skipped"] += 1; total += unanswered; s["marks"] += unanswered
        else:
            s["attempted"] += 1
            if stu == key:
                s["correct"] += 1; total += correct; s["marks"] += correct
            else:
                s["wrong"] += 1; total += wrong; s["marks"] += wrong
                errors["unclassified_wrong"] += 1
    acc = sum(s["correct"] for s in sections.values())
    att = sum(s["attempted"] for s in sections.values())
    out = {
        "id": f"M-{dt.date.today():%Y%m%d}", "ts": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "scheme_status": status, "total": total,
        "sections": sections, "attempted": att, "correct": acc,
        "accuracy_on_attempted": round(acc / att, 3) if att else None,
        "attempt_rate": round(att / len(rows), 3),
        "question_rate_per_minute": round(len(rows) / (sum(float(r["time_sec"]) for r in rows) / 60), 3) if sum(float(r["time_sec"]) for r in rows) else None,
        "tentative_errors": errors,
    }
    print(json.dumps(out, indent=2))
    led = os.path.join(ROOT, "memory", "ledgers", "mock_results.jsonl")
    os.makedirs(os.path.dirname(led), exist_ok=True)
    with open(led, "a", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
    print("appended to mock_results.jsonl")
    return 0

if __name__ == "__main__":
    sys.exit(main())
