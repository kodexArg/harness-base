#!/usr/bin/env python3
"""Merge-time SSOT conformance gate, CI job `pr-merge-gate`.

Contract: [[GITHUB]]. The PR body records `Plan-Verdict:` lines.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from ssot_watchlists import matching_ssots

WATCHLISTS_MODULE = ROOT / "scripts" / "ssot_watchlists.py"

PLAN_VERDICT_RE = re.compile(
    r"^Plan-Verdict:\s*(prd|adr|api):\s*"
    r"(pass|clear|compliant|valid|ok|drift)\s*$",
    re.IGNORECASE,
)


def load_watchlists() -> dict:
    spec = importlib.util.spec_from_file_location("ssot_watchlists", WATCHLISTS_MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WATCHLISTS


def ssots_for(rel: str, watchlists: dict) -> list[str]:
    return matching_ssots(rel, watchlists)


def required_ssots(changed_files: list[str], watchlists: dict) -> dict[str, list[str]]:
    required: dict[str, list[str]] = {}
    for rel in changed_files:
        for ssot in ssots_for(rel, watchlists):
            required.setdefault(ssot, []).append(rel)
    return required


def changed_files_from_git(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        check=True,
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def recorded_verdicts(body: str | None) -> set[str]:
    if not body:
        return set()
    recorded = set()
    for raw in body.splitlines():
        match = PLAN_VERDICT_RE.match(raw.strip())
        if match:
            recorded.add(match.group(1).lower())
    return recorded


def pr_body_from_event(event_path: str | None) -> str | None:
    if not event_path:
        return None
    try:
        payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return (payload.get("pull_request") or {}).get("body")


def default_base() -> str:
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        return f"origin/{base_ref}"
    return "origin/main"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=None,
        help="diff base (default: origin/<GITHUB_BASE_REF> if set, else origin/main)",
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="path to a file holding the PR body text (local/test runs; "
        "CI reads GITHUB_EVENT_PATH instead)",
    )
    args = parser.parse_args()

    base = args.base or default_base()
    changed = changed_files_from_git(base)

    watchlists = load_watchlists()
    required = required_ssots(changed, watchlists)

    if not required:
        print("merge-gate: no watched files changed — passing trivially")
        return 0

    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    else:
        body = pr_body_from_event(os.environ.get("GITHUB_EVENT_PATH"))

    recorded = recorded_verdicts(body)

    for ssot, files in sorted(required.items()):
        status = "recorded" if ssot in recorded else "MISSING"
        print(f"merge-gate: {ssot} required by {files} -> {status}")

    missing = sorted(set(required) - recorded)
    if missing:
        print(
            "\nmerge-gate: FAIL — missing recorded verdict(s). Record one line per SSOT:",
            file=sys.stderr,
        )
        for ssot in missing:
            print(f"  Plan-Verdict: {ssot}: pass", file=sys.stderr)
        return 1

    print("\nmerge-gate: PASS — every required SSOT has a recorded Plan-Verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
