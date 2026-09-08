#!/usr/bin/env python3
"""Deterministic L1 validator for CUET question-bank JSONL files."""
import json
import sys


REQUIRED = {
    "id", "subject", "topic", "subtopic", "type", "stem", "options",
    "correct_index", "explanation", "recognition_cue", "difficulty",
    "trap_type", "source", "validation", "usage_history", "status",
}
TYPES = {"mcq4": {4}, "mcq5": {5}, "assertion": {4, 5}, "arithmetic": {4, 5}}
STATUSES = {"active", "quarantined", "retired"}


def errors(question):
    problems = []
    if not isinstance(question, dict):
        return ["question must be an object"]
    missing = sorted(REQUIRED - question.keys())
    if missing:
        return [f"missing fields: {', '.join(missing)}"]
    unexpected = sorted(question.keys() - REQUIRED)
    if unexpected:
        problems.append(f"unexpected fields: {', '.join(unexpected)}")
    allowed_counts = TYPES.get(question["type"]) if isinstance(question["type"], str) else None
    if allowed_counts is None:
        problems.append("type must be mcq4, mcq5, assertion, or arithmetic")
    options = question["options"] if isinstance(question["options"], list) else []
    if not isinstance(question["options"], list) or (allowed_counts and len(options) not in allowed_counts):
        problems.append("options must contain the required number of entries")
    elif any(not isinstance(option, str) or not option.strip() for option in options) or len(set(options)) != len(options):
        problems.append("options must be unique non-empty strings")
    if not isinstance(question["correct_index"], int) or isinstance(question["correct_index"], bool) or not options or not 0 <= question["correct_index"] < len(options):
        problems.append("correct_index must point to an option")
    for field in ["id", "subject", "topic", "subtopic", "stem", "recognition_cue"]:
        if not isinstance(question[field], str) or not question[field].strip():
            problems.append(f"{field} must be a non-empty string")
    if not isinstance(question["difficulty"], int) or isinstance(question["difficulty"], bool) or not 1 <= question["difficulty"] <= 5:
        problems.append("difficulty must be an integer from 1 to 5")
    if not isinstance(question["trap_type"], str) or question["trap_type"] not in {f"E{i}" for i in range(1, 11)}:
        problems.append("trap_type must be E1 through E10")
    if not isinstance(question["status"], str) or question["status"] not in STATUSES:
        problems.append("status must be active, quarantined, or retired")
    if not isinstance(question["explanation"], str) or not question["explanation"].strip() or len(question["explanation"].split()) > 80:
        problems.append("explanation is required and limited to 80 words")
    validation = question["validation"] if isinstance(question["validation"], dict) else {}
    timestamps = validation.get("timestamps")
    if set(validation) != {"l1", "l2_engine", "l3_by", "timestamps"} or not isinstance(timestamps, list) or not all(isinstance(value, str) and value for value in timestamps) or not isinstance(validation.get("l2_engine"), str) or not (validation.get("l3_by") is None or isinstance(validation.get("l3_by"), str)):
        problems.append("validation must contain l1, l2_engine, l3_by, and timestamps")
    if validation.get("l1") != "pass":
        problems.append("validation.l1 must be pass")
    if question["status"] == "active" and not validation.get("l2_engine"):
        problems.append("validation.l2_engine is required for active questions")
    source = question["source"] if isinstance(question["source"], dict) else {}
    if set(source) != {"generator", "date", "batch"} or not all(isinstance(value, str) and value for value in source.values()):
        problems.append("source must contain non-empty generator, date, and batch strings")
    usage = question["usage_history"] if isinstance(question["usage_history"], dict) else {}
    if set(usage) != {"times_served", "times_correct"} or not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in usage.values()) or usage.get("times_correct", 0) > usage.get("times_served", 0):
        problems.append("usage_history must contain valid non-negative times_served and times_correct")
    return problems


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/validate_questions.py FILE.jsonl")
        return 2
    failed = 0
    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    question = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(f"line {number}: invalid JSON ({exc.msg})")
                    failed += 1
                    continue
                for problem in errors(question):
                    print(f"line {number}: {problem}")
                    failed += 1
    except OSError as exc:
        print(f"FATAL: {exc}")
        return 2
    print("question validation:", "PASS" if failed == 0 else f"FAIL ({failed})")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
