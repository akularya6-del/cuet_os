import json
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_importer():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("import_legacy_under_test", ROOT / "scripts" / "import_legacy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_legacy_import_shifts_actuals_and_never_completes_plans(tmp_path):
    source = tmp_path / "legacy"
    logs = source / "memory" / "logs"
    logs.mkdir(parents=True)
    (logs / "mocks.log").write_text(
        "\n".join(
            [
                "| mock-001a | 2026-09-06 | diag | Maths + GAT | no composite | 33 of 48 issued | 29 | 4 | 87.9% on attempted | 2 | 0 | 0 | 0 | 900s | FORMULA-UNKNOWN | NOT COMPUTABLE |",
                "| mock-001b | 2026-09-06 | diag | Chemistry + English + PE | no composite | 42 of 50 issued | 25 | 17 | 59.5% on attempted | 4 | 0 | 0 | 0 | 3600s | RETENTION-DECAY | NOT COMPUTABLE |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (source / "memory" / "academic_state.md").write_text(
        """## MASTERY TABLE
| topic_id | subject | state | acc20 | evidence_ref | recall_due | state_since |
|---|---|---|---|---|---|---|
| M-F0 | Maths | **LEARNING** | 5/5 (n=5) | mock-001a rung D | 2026-09-13 | 2026-09-06 |
| C-INORG | Chemistry | **LEARNING — forgotten** | 0/5 (n=5) | mock-001b 2A | 2026-09-13 | 2026-09-06 |
""",
        encoding="utf-8",
    )
    (source / "memory" / "profile.md").write_text(
        """# profile
- target: CUET-UG 2027 → Delhi University primary  [USER STATEMENT]  (as_of: 2026-09-06)
- claimed capacity: 5–6h/day, and as of 2026-09-06 the candidate asserts **35 h/wk**
## ATTENTION PROFILE  [USER STATEMENT]  (as_of: 2026-09-06)
- **EXTERNAL / mechanical:** calls and reels sent by friends · opening random tabs.
- **INTERNAL:** difficult to focus even when there are no external distractions.
""",
        encoding="utf-8",
    )
    (source / "WEEK_01_2026-09-07.md").write_text(
        "# WEEK 01 — 2026-09-07 → 2026-09-13\nBLOCK 1: planned only\n",
        encoding="utf-8",
    )
    (source / ".mcp.json").write_text('{"legacy": true}\n', encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "import_legacy.py"), str(source)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    proposal = json.loads(result.stdout)

    rows = proposal["ledger_appends"]["mock_results.jsonl"]
    assert [(row["id"], row["ts"][:10]) for row in rows] == [
        ("legacy-mock-001a", "2026-09-07"),
        ("legacy-mock-001b", "2026-09-07"),
    ]
    assert [(row["attempted"], row["correct"], row["issued"]) for row in rows] == [
        (33, 29, 48),
        (42, 25, 50),
    ]
    assert proposal["ledger_appends"].keys() == {"mock_results.jsonl"}
    assert proposal["mastery_proposal"]["M-F0"] == {
        "subject": "Maths",
        "state": "LEARNING",
        "accuracy_30d": 1.0,
        "attempts": 5,
        "last_seen": "2026-09-07",
        "recall_due": "2026-09-14",
        "evidence_ref": "mock-001a rung D",
        "gate_status": "PROPOSED_IMPORT",
    }
    assert proposal["profile_proposal"]["as_of"] == "2026-09-07"
    assert proposal["profile_proposal"]["scheduled_study_hours_per_week"] == 35
    assert proposal["excluded"]["planned_not_completed"] == [
        {"path": "WEEK_01_2026-09-07.md", "shifted_window": "2026-09-08 to 2026-09-14"}
    ]
    assert ".mcp.json" in proposal["excluded"]["v4_system_files"]
    assert proposal["writes_canonical_ledgers"] is False

    sys.path.insert(0, str(ROOT / "scripts"))
    import ledger

    for row in rows:
        ledger.validate_row("mock_results.jsonl", row)


def test_apply_is_idempotent_and_preserves_newer_mastery(tmp_path):
    importer = load_importer()
    ledgers = tmp_path / "memory" / "ledgers"
    ledgers.mkdir(parents=True)
    importer.ledger.LED = str(ledgers)
    newer = {
        "subject": "Maths",
        "state": "PRACTICED",
        "accuracy_30d": 0.9,
        "attempts": 20,
        "last_seen": "2026-09-08",
        "gate_status": "CURRENT",
    }
    (ledgers / "mastery_map.json").write_text(json.dumps({"M-F0": newer}), encoding="utf-8")
    base_mock = {
        "scheme_status": "[UNKNOWN] legacy diagnostic; composite score not computable",
        "total": 1,
        "sections": {"diagnostic_total": {"attempted": 1, "correct": 1, "wrong": 0, "skipped": 0, "marks": 1}},
        "attempted": 1,
        "correct": 1,
        "accuracy_on_attempted": 1.0,
        "tentative_errors": {},
    }
    proposal = {
        "ledger_appends": {
            "mock_results.jsonl": [
                {**base_mock, "id": "legacy-mock-001a", "ts": "2026-09-07T00:00:00+05:30"},
                {**base_mock, "id": "legacy-mock-001b", "ts": "2026-09-07T00:00:00+05:30"},
            ]
        },
        "mastery_proposal": {
            "M-F0": {**newer, "state": "LEARNING", "last_seen": "2026-09-07", "gate_status": "PROPOSED_IMPORT"},
            "C-INORG": {
                "subject": "Chemistry",
                "state": "LEARNING",
                "accuracy_30d": 0.0,
                "attempts": 5,
                "last_seen": "2026-09-07",
                "recall_due": "2026-09-14",
                "evidence_ref": "mock-001b 2A",
                "gate_status": "PROPOSED_IMPORT",
            },
        },
        "profile_proposal": {
            "as_of": "2026-09-07",
            "target": "CUET-UG 2027",
            "scheduled_study_hours_per_week": 35,
            "attention_constraints": ["external", "internal"],
            "calibration_rule": "measure self-report",
            "evidence_tag": "[LEGACY ARTIFACT]",
        },
    }

    apply = getattr(importer, "apply_proposal", lambda *_: None)
    first = apply(proposal, ledgers)
    assert first == {"mocks_appended": 2, "mastery_imported": 1, "decision_appended": 1}
    second = apply(proposal, ledgers)
    assert second == {"mocks_appended": 0, "mastery_imported": 0, "decision_appended": 0}

    assert len(importer.ledger.read("mock_results.jsonl")) == 2
    decisions = importer.ledger.read("decision_log.jsonl")
    assert len(decisions) == 1
    assert "35 h/week was planned capacity, not executed study" in decisions[0]["decision"]
    mastery = json.loads((ledgers / "mastery_map.json").read_text(encoding="utf-8"))
    assert mastery["M-F0"] == newer
    assert mastery["C-INORG"]["gate_status"] == "IMPORTED_DIAGNOSTIC"
    assert not (ledgers / "study_log.jsonl").exists()


def test_apply_cli_commits_the_proposal_to_the_configured_ledgers(tmp_path, capsys):
    importer = load_importer()
    source = tmp_path / "legacy"
    (source / "memory" / "logs").mkdir(parents=True)
    (source / "memory" / "logs" / "mocks.log").write_text(
        "| mock-001a | 2026-09-06 | diag | Maths | none | 1 of 1 issued | 1 | 0 | 100% | 0 | 0 | 0 | 0 | n/a | none | n/a |\n"
        "| mock-001b | 2026-09-06 | diag | English | none | 1 of 1 issued | 1 | 0 | 100% | 0 | 0 | 0 | 0 | n/a | none | n/a |\n",
        encoding="utf-8",
    )
    (source / "memory" / "academic_state.md").write_text(
        "| M-F0 | Maths | LEARNING | 1/1 (n=1) | mock-001a | 2026-09-13 | 2026-09-06 |\n",
        encoding="utf-8",
    )
    (source / "memory" / "profile.md").write_text(
        "- target: CUET-UG 2027  [USER STATEMENT]  (as_of: 2026-09-06)\n"
        "- planned **35 h/wk**\n",
        encoding="utf-8",
    )
    (source / "WEEK_01_2026-09-07.md").write_text(
        "# 2026-09-07 → 2026-09-13\n", encoding="utf-8"
    )
    ledgers = tmp_path / "v5-ledgers"
    importer.ledger.LED = str(ledgers)

    assert importer.main(["import_legacy.py", "--apply", str(source)]) == 0
    output = capsys.readouterr().out
    assert '"mocks_appended": 2' in output
    assert len(importer.ledger.read("mock_results.jsonl")) == 2
