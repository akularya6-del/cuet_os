import datetime as dt
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).parents[1]


def load_dispatch():
    path = ROOT / "scripts" / "dispatch.py"
    spec = importlib.util.spec_from_file_location("cuet_dispatch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def configured(tmp_path):
    config = tmp_path / "vertex.json"
    config.write_text(json.dumps({
        "enabled": True,
        "project": "trim-hash-471406-t4",
        "location": "global",
        "routes": {
            "volume": "gemini-3.8-flash",
            "complex": "gemini-2.5-pro",
            "preview": "gemini-3.1-pro-preview"
        },
        "max_prompt_chars": 100000,
        "min_output_tokens": 128,
        "default_output_tokens": 512,
        "max_output_tokens": 4096,
        "initial_cap_inr": 100
    }), encoding="utf-8")
    ledger = tmp_path / "credit_ledger.csv"
    ledger.write_text(
        "date,account,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
        "2026-09-09,A,18887.70,0,18887.70,2026-10-02,active,,,verified,INR\n"
        "2026-09-09,B,0,0,0,UNKNOWN,dormant,,,unknown,\n",
        encoding="utf-8",
    )
    return config, ledger


def test_dry_run_routes_volume_without_calling_model(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    called = False

    def model_call(**_kwargs):
        nonlocal called
        called = True

    result = dispatch.run(
        task="volume", prompt="Create ten practice questions.", config_path=config,
        ledger_path=ledger, today=dt.date(2026, 9, 9), model_call=model_call,
    )

    assert result == {
        "account": "A", "approved_cap_inr": None, "location": "global",
        "max_output_tokens": 512, "mode": "dry-run",
        "model": "gemini-3.8-flash", "project": "trim-hash-471406-t4",
        "task": "volume",
    }
    assert called is False


def test_complex_task_uses_stable_pro(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    result = dispatch.run(
        task="complex", prompt="Analyze the mock errors.", config_path=config,
        ledger_path=ledger, today=dt.date(2026, 9, 9),
    )
    assert result["model"] == "gemini-2.5-pro"


def test_preview_requires_both_explicit_selection_and_gate(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    with pytest.raises(ValueError, match="preview.*gate"):
        dispatch.run(
            task="complex", prompt="Compare strategies.", model="preview",
            config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
        )
    assert dispatch.run(
        task="complex", prompt="Compare strategies.", model="preview", allow_preview=True,
        config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
    )["model"] == "gemini-3.1-pro-preview"


def test_execution_requires_explicit_approval(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    with pytest.raises(ValueError, match="approval"):
        dispatch.run(
            task="volume", prompt="Create questions.", execute=True,
            config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
        )


def test_approved_execution_applies_output_cap(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    received = {}

    def model_call(**kwargs):
        received.update(kwargs)
        return {"text": "generated", "usage": {"total_token_count": 42}}

    result = dispatch.run(
        task="complex", prompt="Analyze the mock errors.", execute=True,
        approved_cap_inr=100,
        config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
        model_call=model_call,
    )
    assert received["max_output_tokens"] == 512
    assert result["text"] == "generated"
    assert result["usage"] == {"total_token_count": 42}


def test_usage_metadata_exposes_counts_only():
    dispatch = load_dispatch()
    response = SimpleNamespace(usage_metadata=SimpleNamespace(
        prompt_token_count=10, candidates_token_count=20, total_token_count=30,
        cached_content_token_count=None, thoughts_token_count=3,
        access_token="must-not-leak",
    ))
    assert dispatch._usage_counts(response) == {
        "prompt_token_count": 10,
        "candidates_token_count": 20,
        "total_token_count": 30,
        "thoughts_token_count": 3,
    }


@pytest.mark.parametrize(
    ("max_output_tokens", "approved_cap_inr", "message"),
    [(32, 100, "output token"), (4097, 100, "output token"), (512, 101, "approved cap")],
)
def test_execution_rejects_limits_above_config_before_model_call(
        configured, max_output_tokens, approved_cap_inr, message):
    dispatch = load_dispatch()
    config, ledger = configured
    called = False

    def model_call(**_kwargs):
        nonlocal called
        called = True

    with pytest.raises(ValueError, match=message):
        dispatch.run(
            task="complex", prompt="Analyze the mock errors.", execute=True,
            max_output_tokens=max_output_tokens, approved_cap_inr=approved_cap_inr,
            config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
            model_call=model_call,
        )
    assert called is False


def test_execution_rejects_empty_model_response(configured):
    dispatch = load_dispatch()
    config, ledger = configured

    with pytest.raises(RuntimeError, match="no text"):
        dispatch.run(
            task="volume", prompt="Return a short answer.", execute=True,
            approved_cap_inr=100, config_path=config, ledger_path=ledger,
            today=dt.date(2026, 9, 9),
            model_call=lambda **_kwargs: {
                "text": None,
                "usage": {"total_token_count": 41, "thoughts_token_count": 29},
            },
        )


def test_rejects_prompt_over_configured_limit(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    with pytest.raises(ValueError, match="prompt exceeds"):
        dispatch.run(
            task="volume", prompt="x" * 100001, config_path=config,
            ledger_path=ledger, today=dt.date(2026, 9, 9),
        )


@pytest.mark.parametrize(
    ("account", "ledger_row", "message"),
    [
        ("B", None, "Account B"),
        ("A", "2026-09-09,A,10,0,10,2026-09-08,active,,,verified,INR\n", "expired"),
        ("A", "2026-09-09,A,10,0,10,2026-10-02,dormant,,,verified,INR\n", "not active"),
        ("A", "2026-09-09,A,10,-10,0,2026-10-02,active,,,verified,INR\n", "exhausted"),
    ],
)
def test_rejects_unavailable_accounts(configured, account, ledger_row, message):
    dispatch = load_dispatch()
    config, ledger = configured
    if ledger_row:
        ledger.write_text(
            "date,account,balance_before,delta,balance_after,expiry,status,engine,task_ref,evidence_tag,notes\n"
            + ledger_row,
            encoding="utf-8",
        )
    with pytest.raises(ValueError, match=message):
        dispatch.run(
            task="volume", prompt="Create questions.", account=account,
            config_path=config, ledger_path=ledger, today=dt.date(2026, 9, 9),
        )


def test_rejects_disabled_integration(configured):
    dispatch = load_dispatch()
    config, ledger = configured
    data = json.loads(config.read_text(encoding="utf-8"))
    data["enabled"] = False
    config.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="disabled"):
        dispatch.run(
            task="volume", prompt="Create questions.", config_path=config,
            ledger_path=ledger, today=dt.date(2026, 9, 9),
        )


@pytest.mark.parametrize("prompt", ["", "AIza" + "A" * 32, "sk-" + "A" * 20])
def test_rejects_missing_or_secret_prompt(configured, prompt):
    dispatch = load_dispatch()
    config, ledger = configured
    with pytest.raises(ValueError, match="prompt|secret"):
        dispatch.run(
            task="volume", prompt=prompt, config_path=config,
            ledger_path=ledger, today=dt.date(2026, 9, 9),
        )
