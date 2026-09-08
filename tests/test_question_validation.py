import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "validate_questions.py"


def valid_question():
    return {
        "id": "math-algebra-001",
        "subject": "Mathematics",
        "topic": "Algebra",
        "subtopic": "Quadratics",
        "type": "mcq4",
        "stem": "Which value solves x² = 4?",
        "options": ["2", "3", "4", "5"],
        "correct_index": 0,
        "explanation": "Two squared equals four.",
        "recognition_cue": "square equation",
        "difficulty": 1,
        "trap_type": "E1",
        "source": {"generator": "test-fixture", "date": "2026-09-08", "batch": "test"},
        "validation": {"l1": "pass", "l2_engine": "human-test", "l3_by": None, "timestamps": ["2026-09-08T00:00:00+05:30"]},
        "usage_history": {"times_served": 0, "times_correct": 0},
        "status": "active",
    }


def run_validator(path):
    return subprocess.run([sys.executable, str(SCRIPT), str(path)], cwd=ROOT, text=True, capture_output=True)


def test_question_validator_accepts_a_validated_active_question(tmp_path):
    source = tmp_path / "questions.jsonl"
    source.write_text(json.dumps(valid_question()) + "\n", encoding="utf-8")
    result = run_validator(source)
    assert result.returncode == 0, result.stdout + result.stderr


def test_question_validator_rejects_active_question_without_l2(tmp_path):
    question = valid_question()
    question["validation"]["l2_engine"] = ""
    source = tmp_path / "questions.jsonl"
    source.write_text(json.dumps(question) + "\n", encoding="utf-8")
    result = run_validator(source)
    assert result.returncode == 1
    assert "l2_engine" in result.stdout


def test_question_validator_rejects_wrong_option_count(tmp_path):
    question = valid_question()
    question["options"] = ["2", "3", "4"]
    source = tmp_path / "questions.jsonl"
    source.write_text(json.dumps(question) + "\n", encoding="utf-8")
    result = run_validator(source)
    assert result.returncode == 1
    assert "options" in result.stdout


def test_question_validator_enforces_nested_schema_and_no_extra_fields(tmp_path):
    question = valid_question()
    question["unexpected"] = True
    question["options"] = ["2", "2", "4", "5"]
    question["source"] = {"generator": "test-fixture"}
    question["validation"] = {"l1": "pass", "l2_engine": "human-test"}
    question["usage_history"] = {"times_served": -1}
    source = tmp_path / "questions.jsonl"
    source.write_text(json.dumps(question) + "\n", encoding="utf-8")
    result = run_validator(source)
    assert result.returncode == 1
    assert "unexpected" in result.stdout
    assert "options" in result.stdout
    assert "source" in result.stdout
    assert "validation" in result.stdout
    assert "usage_history" in result.stdout


def test_question_validator_reports_bad_types_without_crashing(tmp_path):
    question = valid_question()
    question["options"] = None
    question["stem"] = 42
    source = tmp_path / "questions.jsonl"
    source.write_text(json.dumps(question) + "\n", encoding="utf-8")
    result = run_validator(source)
    assert result.returncode == 1
    assert "options" in result.stdout
    assert "stem" in result.stdout
    assert "Traceback" not in result.stderr
