#!/usr/bin/env python3
"""Safely route an approved CUET task to Vertex Gemini. Dry-run by default."""
import argparse
import csv
import datetime as dt
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
CONFIG = ROOT / "config" / "vertex.json"
LEDGER = ROOT / "memory" / "ledgers" / "credit_ledger.csv"
SECRET = re.compile(
    r"(sk-(?:ant-|proj-)?[A-Za-z0-9_-]{16,}|AIza[A-Za-z0-9_-]{30,}|"
    r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})"
)


def _latest_account(ledger_path, account):
    latest = None
    with open(ledger_path, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("account") == account:
                latest = row
    if latest is None:
        raise ValueError(f"Account {account} is absent from the credit ledger")
    return latest


def _usage_counts(response):
    metadata = getattr(response, "usage_metadata", None)
    usage = {}
    for field in ("prompt_token_count", "candidates_token_count", "total_token_count",
                  "cached_content_token_count", "thoughts_token_count"):
        value = getattr(metadata, field, None)
        if value is not None:
            usage[field] = value
    return usage


def _call_vertex(*, project, location, model, prompt, max_output_tokens):
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("google-genai is required for --execute") from exc
    client = genai.Client(vertexai=True, project=project, location=location)
    response = client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=max_output_tokens),
    )
    return {"text": response.text, "usage": _usage_counts(response)}


def run(*, task, prompt, account="A", model=None, allow_preview=False,
        execute=False, approved_cap_inr=None, max_output_tokens=None,
        config_path=CONFIG, ledger_path=LEDGER, today=None, model_call=None):
    if not prompt or not prompt.strip():
        raise ValueError("prompt is required")
    if SECRET.search(prompt):
        raise ValueError("prompt contains an apparent secret")
    if account != "A":
        raise ValueError("Account B is unavailable until its human review date")

    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if not config.get("enabled"):
        raise ValueError("Vertex integration is disabled")
    if len(prompt) > config["max_prompt_chars"]:
        raise ValueError("prompt exceeds the configured size limit")
    token_limit = config["default_output_tokens"] if max_output_tokens is None else max_output_tokens
    if not config["min_output_tokens"] <= token_limit <= config["max_output_tokens"]:
        raise ValueError("output token limit is outside the configured range")
    if approved_cap_inr is not None and (
            approved_cap_inr <= 0 or approved_cap_inr > config["initial_cap_inr"]):
        raise ValueError("approved cap exceeds the configured initial cap")

    row = _latest_account(ledger_path, account)
    if row.get("status", "").lower() != "active":
        raise ValueError(f"Account {account} is not active")
    try:
        balance = float(row.get("balance_after", ""))
    except ValueError as exc:
        raise ValueError(f"Account {account} balance is not verified") from exc
    if balance <= 0:
        raise ValueError(f"Account {account} credit is exhausted")
    try:
        expiry = dt.date.fromisoformat(row.get("expiry", ""))
    except ValueError as exc:
        raise ValueError(f"Account {account} expiry is not verified") from exc
    if expiry < (today or dt.date.today()):
        raise ValueError(f"Account {account} credit is expired")

    routes = config["routes"]
    if model == "preview":
        if not allow_preview:
            raise ValueError("preview model requires the explicit preview gate")
        selected = routes["preview"]
    elif model is not None:
        raise ValueError("model must be selected by task, or explicitly as preview")
    else:
        try:
            selected = routes[task]
        except KeyError as exc:
            raise ValueError(f"unsupported task: {task}") from exc

    project = os.getenv(config.get("project_env", ""), config["project"])
    location = os.getenv(config.get("location_env", ""), config["location"])
    if project != config["project"] or location != "global":
        raise ValueError("Vertex project/location must remain the verified Account-A project and global endpoint")
    plan = {
        "account": account, "approved_cap_inr": approved_cap_inr, "location": location,
        "max_output_tokens": token_limit,
        "mode": "execute" if execute else "dry-run", "model": selected,
        "project": project, "task": task,
    }
    if not execute:
        return plan
    if approved_cap_inr is None:
        raise ValueError("explicit human approval cap is required for execution")
    call = model_call or _call_vertex
    generated = call(
        project=project, location=location, model=selected, prompt=prompt,
        max_output_tokens=token_limit,
    )
    if not isinstance(generated, dict) or not generated.get("text"):
        raise RuntimeError("Vertex returned no text; output may have been consumed by reasoning")
    plan.update(generated)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=["volume", "complex"], required=True)
    prompt = parser.add_mutually_exclusive_group(required=True)
    prompt.add_argument("--prompt")
    prompt.add_argument("--prompt-file", type=Path)
    parser.add_argument("--account", default="A")
    parser.add_argument("--model", choices=["preview"])
    parser.add_argument("--allow-preview", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approved-cap-inr", type=float)
    parser.add_argument("--max-output-tokens", type=int)
    args = parser.parse_args()
    text = args.prompt if args.prompt is not None else args.prompt_file.read_text(encoding="utf-8")
    try:
        result = run(task=args.task, prompt=text, account=args.account, model=args.model,
                     allow_preview=args.allow_preview, execute=args.execute,
                     approved_cap_inr=args.approved_cap_inr,
                     max_output_tokens=args.max_output_tokens)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
