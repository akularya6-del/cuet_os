#!/usr/bin/env python3
"""Build a reviewable V4 academic-data proposal; never write V5 ledgers."""

import datetime as dt
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import ledger


SHIFT = dt.timedelta(days=1)
IST = "+05:30"


def shift_date(value):
    if not value or value == "—":
        return None
    return (dt.date.fromisoformat(value) + SHIFT).isoformat()


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def mock_rows(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| mock-"):
            continue
        item = cells(line)
        attempted_match = re.fullmatch(r"(\d+) of (\d+) issued", item[5])
        accuracy_match = re.search(r"(\d+(?:\.\d+)?)%", item[8])
        if not attempted_match or not accuracy_match:
            raise ValueError(f"unsupported mock row: {item[0]}")
        attempted, issued = map(int, attempted_match.groups())
        correct, wrong = int(item[6]), int(item[7])
        if attempted != correct + wrong:
            raise ValueError(f"inconsistent mock counts: {item[0]}")
        shifted = shift_date(item[1])
        row = {
            "id": f"legacy-{item[0]}",
            "ts": f"{shifted}T00:00:00{IST}",
            "scheme_status": "[UNKNOWN] legacy diagnostic; composite score not computable",
            "total": correct,
            "total_kind": "correct_count_not_exam_marks",
            "issued": issued,
            "sections": {
                "diagnostic_total": {
                    "attempted": attempted,
                    "correct": correct,
                    "wrong": wrong,
                    "skipped": issued - attempted,
                    "marks": correct,
                }
            },
            "attempted": attempted,
            "correct": correct,
            "accuracy_on_attempted": round(float(accuracy_match.group(1)) / 100, 3),
            "tentative_errors": {"legacy_unmapped_wrong": wrong},
            "source": "legacy memory/logs/mocks.log",
            "source_date_precision": "day",
            "evidence_tag": "[LEGACY ARTIFACT]",
        }
        ledger.validate_row("mock_results.jsonl", row)
        rows.append(row)
    if [row["id"] for row in rows] != ["legacy-mock-001a", "legacy-mock-001b"]:
        raise ValueError("expected exactly legacy mock-001a and mock-001b")
    return rows


def mastery_proposal(path):
    proposal = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| [A-Z]+-[A-Z0-9]+ ", line):
            continue
        item = cells(line)
        if len(item) != 7:
            continue
        topic, subject, raw_state, accuracy, evidence, recall_due, state_since = item
        state = "LEARNING" if "LEARNING" in raw_state else "UNSEEN"
        fraction = re.search(r"(\d+)\s*/\s*(\d+)", accuracy)
        attempts_match = re.search(r"n=(\d+)", accuracy)
        attempts = int(attempts_match.group(1)) if attempts_match else (int(fraction.group(2)) if fraction else None)
        proposal[topic] = {
            "subject": subject,
            "state": state,
            "accuracy_30d": round(int(fraction.group(1)) / int(fraction.group(2)), 3) if fraction else None,
            "attempts": attempts,
            "last_seen": shift_date(state_since),
            "recall_due": shift_date(recall_due),
            "evidence_ref": evidence,
            "gate_status": "PROPOSED_IMPORT",
        }
    if not proposal:
        raise ValueError("no mastery rows found")
    return proposal


def profile_proposal(path):
    text = path.read_text(encoding="utf-8")
    date_match = re.search(r"as_of:\s*(\d{4}-\d{2}-\d{2})", text)
    hours_match = re.search(r"\*\*(\d+) h/wk\*\*", text)
    target_match = re.search(r"^- target:\s*(.*?)\s{2,}\[", text, re.MULTILINE)
    if not date_match or not hours_match or not target_match:
        raise ValueError("legacy profile lacks target, date, or weekly hours")
    return {
        "as_of": shift_date(date_match.group(1)),
        "target": target_match.group(1),
        "scheduled_study_hours_per_week": int(hours_match.group(1)),
        "attention_constraints": [
            "external: calls/reels and random tabs",
            "internal: focus can lapse without external distraction",
        ],
        "calibration_rule": "self-report requires artifact-backed measurement",
        "evidence_tag": "[USER STATEMENT; LEGACY ARTIFACT]",
    }


def planned_exclusion(source):
    week = source / "WEEK_01_2026-09-07.md"
    if not week.exists():
        return []
    match = re.search(r"(\d{4}-\d{2}-\d{2})\s*[→-]+\s*(\d{4}-\d{2}-\d{2})", week.read_text(encoding="utf-8"))
    if not match:
        raise ValueError("legacy Week 1 window not found")
    return [{"path": week.name, "shifted_window": f"{shift_date(match.group(1))} to {shift_date(match.group(2))}"}]


def build_proposal(source):
    return {
        "schema_version": 1,
        "date_shift_days": 1,
        "ledger_appends": {"mock_results.jsonl": mock_rows(source / "memory" / "logs" / "mocks.log")},
        "mastery_proposal": mastery_proposal(source / "memory" / "academic_state.md"),
        "profile_proposal": profile_proposal(source / "memory" / "profile.md"),
        "excluded": {
            "planned_not_completed": planned_exclusion(source),
            "v4_system_files": [".claude/", ".claude-flow/", ".codex/", ".mcp.json", "*_V4.md", "scripts/"],
        },
        "writes_canonical_ledgers": False,
    }


def apply_proposal(proposal, ledgers):
    ledgers = Path(ledgers)
    ledgers.mkdir(parents=True, exist_ok=True)
    ledger.LED = str(ledgers)

    mastery_path = ledgers / "mastery_map.json"
    if mastery_path.exists():
        mastery = json.loads(mastery_path.read_text(encoding="utf-8"))
        if not isinstance(mastery, dict):
            raise ValueError("mastery_map.json must contain an object")
    else:
        mastery = {}
    mastery_imported = 0
    for topic, proposed in proposal["mastery_proposal"].items():
        existing = mastery.get(topic)
        if existing and (existing.get("last_seen") or "9999-12-31") >= (proposed.get("last_seen") or "0001-01-01"):
            continue
        mastery[topic] = {**proposed, "gate_status": "IMPORTED_DIAGNOSTIC"}
        mastery_imported += 1
    if mastery_imported:
        with tempfile.NamedTemporaryFile("w", dir=ledgers, encoding="utf-8", delete=False) as handle:
            json.dump(mastery, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            replacement = handle.name
        os.replace(replacement, mastery_path)

    existing_mock_ids = {row["id"] for row in ledger.read("mock_results.jsonl")}
    mocks_appended = 0
    for row in proposal["ledger_appends"]["mock_results.jsonl"]:
        if row["id"] not in existing_mock_ids:
            ledger.append("mock_results.jsonl", row.copy())
            existing_mock_ids.add(row["id"])
            mocks_appended += 1

    profile = proposal["profile_proposal"]
    decision = {
        "id": "legacy-profile-context-20260907",
        "ts": f"{profile['as_of']}T00:00:00{IST}",
        "decision": (
            f"Imported legacy profile context for {profile['target']}: "
            f"{profile['scheduled_study_hours_per_week']} h/week was planned capacity, not executed study; "
            f"attention constraints: {', '.join(profile['attention_constraints'])}; "
            f"calibration: {profile['calibration_rule']}."
        ),
        "evidence_tags": [profile["evidence_tag"]],
        "horizon_notes": {"source": "legacy memory/profile.md", "date_shift_days": 1},
    }
    existing_decision_ids = {row["id"] for row in ledger.read("decision_log.jsonl")}
    decision_appended = 0
    if decision["id"] not in existing_decision_ids:
        ledger.append("decision_log.jsonl", decision)
        decision_appended = 1

    return {
        "mocks_appended": mocks_appended,
        "mastery_imported": mastery_imported,
        "decision_appended": decision_appended,
    }


def main(argv):
    apply = len(argv) == 3 and argv[1] == "--apply"
    if len(argv) != (3 if apply else 2):
        print("usage: import_legacy.py [--apply] LEGACY_ROOT", file=sys.stderr)
        return 2
    try:
        proposal = build_proposal(Path(argv[-1]).expanduser().resolve())
        result = apply_proposal(proposal, ledger.LED) if apply else proposal
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"legacy import refused: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
