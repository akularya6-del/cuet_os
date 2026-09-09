import contextlib
import csv
import importlib.util
import io
import json
import subprocess
import sys
import datetime as dt
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]


def load_script(name):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"cuet_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ledger_append_read_and_state_regeneration(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path / "memory" / "ledgers")
    ledger.STATE = str(tmp_path / "memory" / "STATE.md")
    ledger.append("study_log.jsonl", {"id": "B-test", "topic": "algebra", "minutes": 50, "questions": 10, "correct": 8, "confusion": "sign"})
    assert ledger.read("study_log.jsonl")[0]["topic"] == "algebra"
    assert ledger.cmd_state([]) == 0
    state = Path(ledger.STATE).read_text(encoding="utf-8")
    assert "study_minutes_14d: 50" in state
    assert "- sign" in state


def test_ledger_verify_rejects_invalid_jsonl(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    (tmp_path / "study_log.jsonl").write_text("{not-json}\n", encoding="utf-8")
    assert ledger.cmd_verify([]) == 1


def test_ledger_verify_rejects_bad_csv_header_and_model_health(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    (tmp_path / "token_ledger.csv").write_text("wrong,header\n", encoding="utf-8")
    (tmp_path / "model_health.json").write_text("{bad-json}\n", encoding="utf-8")
    assert ledger.cmd_verify([]) == 1


def test_ledger_rejects_structurally_invalid_rows(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    (tmp_path / "error_log.jsonl").write_text("[]\n", encoding="utf-8")
    assert ledger.cmd_verify([]) == 1
    with pytest.raises(ValueError):
        ledger.append("study_log.jsonl", {"id": "missing-fields"})


def test_ledger_rejects_invalid_semantics(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    bad = {"id": "B-bad", "ts": "not-a-date", "topic": "", "minutes": 1, "questions": 1, "correct": 1}
    (tmp_path / "study_log.jsonl").write_text(json.dumps(bad) + "\n", encoding="utf-8")
    assert ledger.cmd_verify([]) == 1


def test_ledger_error_command_rejects_missing_fields_without_crashing(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    assert ledger.cmd_error([]) == 2
    assert ledger.cmd_error(["E1"]) == 2


def test_ledger_block_rejects_impossible_score(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)
    assert ledger.cmd_block(["algebra", "|", "50min", "|", "10Q", "|", "11", "correct"]) == 2
    assert ledger.read("study_log.jsonl") == []


def test_state_uses_date_windows_not_record_counts(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path / "memory" / "ledgers")
    ledger.STATE = str(tmp_path / "memory" / "STATE.md")
    old = (dt.datetime.now().astimezone() - dt.timedelta(days=20)).isoformat(timespec="seconds")
    ledger.append("study_log.jsonl", {"id": "old", "ts": old, "topic": "old", "minutes": 999, "questions": 1, "correct": 1})
    ledger.append("study_log.jsonl", {"id": "new", "topic": "new", "minutes": 50, "questions": 1, "correct": 1})
    assert ledger.cmd_state([]) == 0
    state = Path(ledger.STATE).read_text(encoding="utf-8")
    assert "study_minutes_14d: 50" in state
    assert "blocks_logged_7: 1" in state


def test_state_labels_legacy_diagnostic_as_correct_count_not_exam_score(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path / "memory" / "ledgers")
    ledger.STATE = str(tmp_path / "memory" / "STATE.md")
    ledger.append("mock_results.jsonl", {
        "id": "legacy-mock", "ts": "2026-09-07T00:00:00+05:30",
        "scheme_status": "[UNKNOWN] legacy diagnostic", "total": 25,
        "total_kind": "correct_count_not_exam_marks", "attempted": 42, "correct": 25,
        "accuracy_on_attempted": 0.595,
        "sections": {"diagnostic": {"attempted": 42, "correct": 25, "wrong": 17,
                                      "skipped": 8, "marks": 25}},
        "tentative_errors": {"legacy_unmapped_wrong": 17},
    })
    assert ledger.cmd_state([]) == 0
    state = Path(ledger.STATE).read_text(encoding="utf-8")
    assert "last_assessment: 25 correct of 42 attempted" in state
    assert "last_mock: 25" not in state


def test_ledger_compact_archives_outside_active_ledgers(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path / "memory" / "ledgers")
    Path(ledger.LED).mkdir(parents=True)
    rows = "".join(json.dumps({"id": f"B-{i}", "ts": dt.datetime.now().astimezone().isoformat(), "topic": "x", "minutes": 1, "questions": 1, "correct": 1}) + "\n" for i in range(401))
    (Path(ledger.LED) / "study_log.jsonl").write_text(rows, encoding="utf-8")
    (Path(ledger.LED) / "error_log.jsonl").write_text("", encoding="utf-8")
    assert ledger.cmd_compact([]) == 0
    archives = list((tmp_path / "memory" / "archive").glob("study_log.jsonl.*"))
    assert len(archives) == 1
    assert len(ledger.read("study_log.jsonl")) == 200


def test_ledger_compaction_preserves_active_file_if_replace_fails(tmp_path, monkeypatch):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path / "memory" / "ledgers")
    Path(ledger.LED).mkdir(parents=True)
    rows = "".join(json.dumps({"id": f"B-{i}", "ts": dt.datetime.now().astimezone().isoformat(), "topic": "x", "minutes": 1, "questions": 1, "correct": 1}) + "\n" for i in range(401))
    active = Path(ledger.LED) / "study_log.jsonl"
    active.write_text(rows, encoding="utf-8")
    (Path(ledger.LED) / "error_log.jsonl").write_text("", encoding="utf-8")

    def fail_replace(*_args):
        raise OSError("simulated interruption")

    monkeypatch.setattr(ledger.os, "replace", fail_replace)
    with pytest.raises(OSError):
        ledger.cmd_compact([])
    assert len(active.read_text(encoding="utf-8").splitlines()) == 401


def test_ledger_unknown_command_exits_cleanly():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "ledger.py"), "unknown"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr


def test_bootstrap_rejects_unknown_flags(monkeypatch):
    bootstrap = load_script("bootstrap_check")
    monkeypatch.setattr(sys, "argv", ["bootstrap_check.py", "--typo"])
    assert bootstrap.main() == 2


def test_router_emits_deterministic_tier(tmp_path, monkeypatch):
    router = load_script("router")
    router.LED = str(tmp_path)
    monkeypatch.setattr(sys, "argv", ["router.py", "--task", "log block", "--value", "1", "--unc", "1", "--err", "1", "--imp", "1"])
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert router.main() == 0
    result = json.loads(output.getvalue())
    assert result["mcv"] == 0.5
    assert result["tier"] == "T0/T1 (script or free tool)"
    assert set(("engine", "profile", "est_cost_usd", "gate_required")) <= result.keys()


def test_router_credit_mode_excludes_dormant_reserve(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,status\n2026-09-08,A,USD,299,-299,0,active\n2026-09-08,B,USD,300,0,300,dormant\n",
        encoding="utf-8",
    )
    assert router.credit_mode()[0] == "EMERGENCY"


def test_router_credit_mode_retains_original_active_capacity(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status\n"
        "2026-09-01,A,USD,299,-248,51,2099-01-01,active\n"
        "2026-09-08,A,USD,51,-1,50,2099-01-01,active\n"
        "2026-09-08,B,USD,300,0,300,UNKNOWN,dormant\n",
        encoding="utf-8",
    )
    assert router.credit_mode()[0] == "PEAK"


def test_scorer_handles_correct_wrong_and_unanswered(tmp_path, monkeypatch):
    scorer = load_script("scorer")
    scorer.ROOT = str(tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 5, "wrong": -1, "unanswered": 0, "status": "REQUIRES-2027-CONFIRMATION"}),
        encoding="utf-8",
    )
    answers = tmp_path / "answers.csv"
    with answers.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["qno", "subject", "topic", "correct_index", "student_index", "time_sec"])
        writer.writerows([[1, "Maths", "algebra", 0, 0, 30], [2, "Maths", "algebra", 1, 2, 40], [3, "English", "grammar", 2, "", 0]])
    monkeypatch.setattr(sys, "argv", ["scorer.py", str(answers)])
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert scorer.main() == 0
    result = json.loads(output.getvalue().split("\nappended", 1)[0])
    assert result["total"] == 4
    assert result["sections"]["Maths"] == {"attempted": 2, "correct": 1, "wrong": 1, "skipped": 0, "marks": 4}
    assert result["sections"]["English"]["skipped"] == 1


def test_scorer_fails_closed_without_marking_config(tmp_path, monkeypatch):
    scorer = load_script("scorer")
    scorer.ROOT = str(tmp_path)
    answers = tmp_path / "answers.csv"
    answers.write_text("qno,subject,topic,correct_index,student_index,time_sec\n1,Maths,a,0,0,10\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["scorer.py", str(answers)])
    assert scorer.main() == 1


def test_scorer_rejects_missing_columns_before_append(tmp_path, monkeypatch):
    scorer = load_script("scorer")
    scorer.ROOT = str(tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 5, "wrong": -1, "unanswered": 0, "status": "REQUIRES-2027-CONFIRMATION"}),
        encoding="utf-8",
    )
    answers = tmp_path / "answers.csv"
    answers.write_text("qno,subject,correct_index\n1,Maths,0\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["scorer.py", str(answers)])
    assert scorer.main() == 1
    assert not (tmp_path / "memory" / "ledgers" / "mock_results.jsonl").exists()


def test_scorer_rejects_non_finite_time_and_does_not_invent_error_class(tmp_path, monkeypatch):
    scorer = load_script("scorer")
    scorer.ROOT = str(tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 5, "wrong": -1, "unanswered": 0, "status": "REQUIRES-2027-CONFIRMATION"}),
        encoding="utf-8",
    )
    answers = tmp_path / "answers.csv"
    answers.write_text("qno,subject,topic,correct_index,student_index,time_sec\n1,Maths,a,0,1,NaN\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["scorer.py", str(answers)])
    assert scorer.main() == 1
    answers.write_text("qno,subject,topic,correct_index,student_index,time_sec\n1,Maths,a,0,1,10\n", encoding="utf-8")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert scorer.main() == 0
    result = json.loads(output.getvalue().split("\nappended", 1)[0])
    assert result["tentative_errors"] == {"unclassified_wrong": 1}


def test_validate_change_rejects_secret_cjk_and_invalid_jsonl(tmp_path):
    validator = load_script("validate_change")
    validator.ROOT = str(tmp_path)
    (tmp_path / "AGENTS.md").write_text("safe\n", encoding="utf-8")
    fake_secret = "sk-" + "A" * 16
    cjk = chr(0x6F22) + chr(0x5B57)
    (tmp_path / "bad.md").write_text(f"secret {fake_secret} and {cjk}\n", encoding="utf-8")
    ledgers = tmp_path / "memory" / "ledgers"
    ledgers.mkdir(parents=True)
    (ledgers / "study_log.jsonl").write_text("{bad-json}\n", encoding="utf-8")
    old_argv = sys.argv
    sys.argv = ["validate_change.py", "bad.md", "memory"]
    try:
        assert validator.main() == 1
    finally:
        sys.argv = old_argv


def test_validate_change_rejects_invalid_jsonl_even_when_text_is_safe(tmp_path):
    validator = load_script("validate_change")
    validator.ROOT = str(tmp_path)
    (tmp_path / "AGENTS.md").write_text("safe\n", encoding="utf-8")
    ledgers = tmp_path / "memory" / "ledgers"
    ledgers.mkdir(parents=True)
    (ledgers / "study_log.jsonl").write_text("{bad-json}\n", encoding="utf-8")
    old_argv = sys.argv
    sys.argv = ["validate_change.py", "memory"]
    try:
        assert validator.main() == 1
    finally:
        sys.argv = old_argv


def test_validate_change_default_scans_project_and_marking_invariants(tmp_path):
    validator = load_script("validate_change")
    validator.ROOT = str(tmp_path)
    (tmp_path / "AGENTS.md").write_text("safe\n", encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 5, "wrong": -1, "unanswered": 0, "status": "UNVERIFIED", "evidence_tag": "none"}),
        encoding="utf-8",
    )
    (tmp_path / "memory").mkdir()
    (tmp_path / ".codex").mkdir()
    fake_secret = "sk-ant-" + "A" * 20
    (tmp_path / ".codex" / "config.toml").write_text(f'token = "{fake_secret}"\n', encoding="utf-8")
    old_argv = sys.argv
    sys.argv = ["validate_change.py"]
    try:
        assert validator.main() == 1
    finally:
        sys.argv = old_argv


def test_validate_change_ignores_local_virtual_environment(tmp_path):
    validator = load_script("validate_change")
    validator.ROOT = str(tmp_path)
    (tmp_path / "AGENTS.md").write_text("safe\n", encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 5, "wrong": -1, "unanswered": 0,
                    "status": "REQUIRES-2027-CONFIRMATION", "baseline_cycle": 2026,
                    "evidence_tag": "[HISTORICAL OFFICIAL — CUET-UG 2027 UNKNOWN]"}),
        encoding="utf-8",
    )
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "third_party.py").write_text("sk-" + "A" * 16, encoding="utf-8")
    old_argv = sys.argv
    sys.argv = ["validate_change.py"]
    try:
        assert validator.main() == 0
    finally:
        sys.argv = old_argv


def test_validate_change_rejects_mutated_historical_marking_values(tmp_path):
    validator = load_script("validate_change")
    validator.ROOT = str(tmp_path)
    (tmp_path / "AGENTS.md").write_text("safe\n", encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "marking_scheme.json").write_text(
        json.dumps({"correct": 500, "wrong": 0, "unanswered": 99, "status": "REQUIRES-2027-CONFIRMATION", "baseline_cycle": 2026, "evidence_tag": "[HISTORICAL OFFICIAL — CUET-UG 2027 UNKNOWN]"}),
        encoding="utf-8",
    )
    old_argv = sys.argv
    sys.argv = ["validate_change.py"]
    try:
        assert validator.main() == 1
    finally:
        sys.argv = old_argv
