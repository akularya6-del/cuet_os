import csv
import datetime as dt
import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_script(name):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"cuet_{name}_credit_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_credit_command_appends_native_currency_snapshot(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)

    result = ledger.cmd_credit([
        "--account", "A",
        "--balance-before", "28320.75",
        "--delta", "-9433.05",
        "--balance-after", "18887.70",
        "--currency", "INR",
        "--expiry", "2026-10-02",
        "--status", "active",
        "--engine", "google-cloud",
        "--task-ref", "console-reconciliation",
        "--evidence-tag", "[USER-PROVIDED SCREENSHOT VERIFIED 2026-09-09]",
        "--notes", "Free Trial; original INR 28320.75; 67% displayed; net pricing; exact SKU scope [UNKNOWN]",
    ])

    assert result == 0
    with (tmp_path / "credit_ledger.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert b"\r\n" not in (tmp_path / "credit_ledger.csv").read_bytes()
    assert rows == [{
        "date": "2026-09-09",
        "account": "A",
        "currency": "INR",
        "balance_before": "28320.75",
        "delta": "-9433.05",
        "balance_after": "18887.70",
        "expiry": "2026-10-02",
        "status": "active",
        "engine": "google-cloud",
        "task_ref": "console-reconciliation",
        "evidence_tag": "[USER-PROVIDED SCREENSHOT VERIFIED 2026-09-09]",
        "notes": "Free Trial; original INR 28320.75; 67% displayed; net pricing; exact SKU scope [UNKNOWN]",
    }]


def test_credit_command_rejects_inconsistent_arithmetic_without_writing(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)

    result = ledger.cmd_credit([
        "--account", "A", "--balance-before", "100", "--delta", "-1",
        "--balance-after", "50", "--currency", "INR", "--expiry", "2026-10-02",
        "--status", "active", "--evidence-tag", "[VERIFIED]",
    ])

    assert result == 2
    assert not (tmp_path / "credit_ledger.csv").exists()


def test_token_command_records_observed_usage_and_estimated_cost(tmp_path):
    ledger = load_script("ledger")
    ledger.LED = str(tmp_path)

    result = ledger.cmd_token([
        "--category", "vertex-smoke", "--task", "account-a-auth-check",
        "--engine", "gemini-3.8-flash", "--tokens", "168",
        "--est-cost-usd", "0.000558", "--evidence-tag", "[LOCAL OBSERVED 2026-09-09]",
        "--notes", "two approved smoke calls; estimated from official token prices",
    ])

    assert result == 0
    with (tmp_path / "token_ledger.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["tokens"] == "168"
    assert rows[0]["est_cost_usd"] == "0.000558"


def test_router_uses_most_restrictive_active_account_ratio_without_summing_currencies(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,INR,28320.75,-9433.05,18887.70,2026-10-02,active,google-cloud,x,[VERIFIED],x\n"
        "2026-09-09,C,USD,100,-75,25,2026-10-02,active,other,x,[VERIFIED],x\n",
        encoding="utf-8",
    )

    assert router.credit_mode()[0] == "PEAK"


def test_router_prioritizes_verified_credit_near_expiry(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,INR,28320.75,-9433.05,18887.70,2026-10-02,active,google-cloud,x,[VERIFIED],x\n",
        encoding="utf-8",
    )

    assert router.credit_mode(today=dt.date(2026, 9, 9))[0] == "EXPIRING"


def test_router_fails_closed_when_latest_credit_snapshot_has_no_currency(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,,100,-1,99,2026-10-02,active,google-cloud,x,[VERIFIED],x\n",
        encoding="utf-8",
    )

    assert router.credit_mode()[0] == "EMERGENCY"


def test_router_fails_closed_on_incomplete_currency_switch_snapshot(tmp_path):
    router = load_script("router")
    router.LED = str(tmp_path)
    (tmp_path / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-08,A,USD,299,0,299,UNKNOWN,active,,,x,x\n"
        "2026-09-09,A,INR,28320.75,,18887.70,2026-10-02,active,google-cloud,x,[VERIFIED],x\n",
        encoding="utf-8",
    )

    assert router.credit_mode()[0] == "EMERGENCY"


def test_bootstrap_displays_credit_native_currency(tmp_path, monkeypatch, capsys):
    bootstrap = load_script("bootstrap_check")
    bootstrap.MEM = str(tmp_path / "memory")
    bootstrap.LED = str(tmp_path / "memory" / "ledgers")
    bootstrap.STATE = str(tmp_path / "memory" / "STATE.md")
    Path(bootstrap.LED).mkdir(parents=True)
    Path(bootstrap.STATE).write_text("fresh\n", encoding="utf-8")
    for name in ("study_log.jsonl", "error_log.jsonl", "mock_results.jsonl"):
        (Path(bootstrap.LED) / name).write_text("", encoding="utf-8")
    for name in ("token_ledger.csv", "cash_ledger.csv"):
        (Path(bootstrap.LED) / name).write_text("date\n", encoding="utf-8")
    (Path(bootstrap.LED) / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,INR,28320.75,-9433.05,18887.70,2026-10-02,active,google-cloud,x,[VERIFIED],x\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(bootstrap.sys, "argv", ["bootstrap_check.py", "--quick"])

    assert bootstrap.main() == 1
    output = capsys.readouterr().out
    assert "balance INR 18887.70" in output
    assert "$18887.70" not in output


def test_bootstrap_does_not_prompt_about_dormant_credit_account(tmp_path, monkeypatch, capsys):
    bootstrap = load_script("bootstrap_check")
    bootstrap.MEM = str(tmp_path / "memory")
    bootstrap.LED = str(tmp_path / "memory" / "ledgers")
    bootstrap.STATE = str(tmp_path / "memory" / "STATE.md")
    Path(bootstrap.LED).mkdir(parents=True)
    Path(bootstrap.STATE).write_text("fresh\n", encoding="utf-8")
    for name in ("study_log.jsonl", "error_log.jsonl", "mock_results.jsonl"):
        (Path(bootstrap.LED) / name).write_text("", encoding="utf-8")
    for name in ("token_ledger.csv", "cash_ledger.csv"):
        (Path(bootstrap.LED) / name).write_text("date\n", encoding="utf-8")
    (Path(bootstrap.LED) / "credit_ledger.csv").write_text(
        "date,account,currency,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,INR,100,0,100,2027-12-31,active,google-cloud,x,[VERIFIED],x\n"
        "2026-09-09,B,,300,0,300,UNKNOWN,dormant,,,x,deferred\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(bootstrap.sys, "argv", ["bootstrap_check.py", "--quick"])

    assert bootstrap.main() == 0
    assert "Account B" not in capsys.readouterr().out
