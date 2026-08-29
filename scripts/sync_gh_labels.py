#!/usr/bin/env python3
"""Plan and apply the GitHub label set declared in docs/GITHUB.md.

Contract: [[GITHUB]] "Labels (issues + PRs) — fixed set", [[adr-08-github]] rule 6.

Default is a dry-run. `--apply` creates missing labels, updates descriptions,
and deletes unsanctioned ones. Not a CI gate — mutating labels needs a PAT.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
GH_DOC = ROOT / "docs" / "GITHUB.md"
TABLE_HEADING = "## Labels (issues + PRs) — fixed set"
GITHUB_DESCRIPTION_MAX = 100

_ROW = r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$"


class LabelDiff(NamedTuple):
    missing: tuple[str, ...]
    extra: tuple[str, ...]
    description_mismatch: tuple[tuple[str, str, str], ...]


def parse_fixed_set(text: str) -> dict[str, str]:
    """Return {name: use} from label tables under TABLE_HEADING until the next h2."""
    if TABLE_HEADING not in text:
        raise ValueError(f"GITHUB.md has no heading {TABLE_HEADING!r}")
    section = text.split(TABLE_HEADING, 1)[1].split("\n## ", 1)[0]
    labels: dict[str, str] = {}
    for line in section.splitlines():
        match = re.match(_ROW, line)
        if match:
            labels[match.group(1)] = match.group(2).strip()
    if not labels:
        raise ValueError("GITHUB.md label tables parsed empty")
    return labels


def github_description(use: str) -> str:
    """GitHub caps label descriptions at 100 characters; strip catalog markup."""
    plain = use.replace("**", "").replace("`", "")
    if len(plain) <= GITHUB_DESCRIPTION_MAX:
        return plain
    return plain[: GITHUB_DESCRIPTION_MAX - 1].rstrip() + "…"


def color_for(name: str) -> str:
    if name.endswith("-fail"):
        return "d73a4a"
    if name.endswith("-approved") or name == "clean-applied":
        return "0e8a16"
    if name.endswith("-observed"):
        return "fbca04"
    if name.startswith("🟢") or name == "feat":
        return "0e8a16"
    if name.startswith("🟠"):
        return "e4a820"
    if name.startswith("🔴") or name == "bug":
        return "d73a4a"
    if name.startswith("📦"):
        return "1d76db"
    if name.startswith("⚙️"):
        return "5319e7"
    if name.startswith("adr-") or name == "📜 adr":
        return "3e4b9e"
    palette = {
        "chore": "cfd3d7",
        "docs": "0075ca",
        "harness": "5319e7",
        "infra": "5319e7",
        "infra-cicd": "5319e7",
        "blocked": "b60205",
        "complex": "d93f0b",
        "service": "1d76db",
        "surface": "a2eeef",
        "enhancement": "a2eeef",
        "performance": "d4c5f9",
        "security": "ee0701",
        "tech-debt": "fef2c0",
        "needs-design": "fbca04",
        "needs-repro": "fbca04",
        "cursor-issue-triage": "c5def5",
        "invalid": "e4e669",
    }
    return palette.get(name, "cfd3d7")


def diff_labels(fixed: dict[str, str], live: dict[str, str]) -> LabelDiff:
    missing = tuple(sorted(set(fixed) - set(live)))
    extra = tuple(sorted(set(live) - set(fixed)))
    mismatch: list[tuple[str, str, str]] = []
    for name in sorted(set(fixed) & set(live)):
        wanted = github_description(fixed[name])
        actual = (live[name] or "").strip()
        if actual != wanted:
            mismatch.append((name, actual, wanted))
    return LabelDiff(missing=missing, extra=extra, description_mismatch=tuple(mismatch))


def _gh(*args: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def live_labels() -> dict[str, str] | None:
    try:
        proc = _gh("label", "list", "--limit", "200", "--json", "name,description")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    try:
        rows = json.loads(proc.stdout)
        return {row["name"]: row.get("description") or "" for row in rows}
    except (json.JSONDecodeError, TypeError, KeyError):
        return None


def apply_diff(diff: LabelDiff, fixed: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for name in diff.missing:
        proc = _gh(
            "label",
            "create",
            name,
            "--color",
            color_for(name),
            "--description",
            github_description(fixed[name]),
        )
        if proc.returncode != 0:
            errors.append(proc.stderr.strip() or proc.stdout.strip() or f"create failed: {name}")
    for name, _actual, wanted in diff.description_mismatch:
        proc = _gh("label", "edit", name, "--description", wanted)
        if proc.returncode != 0:
            errors.append(proc.stderr.strip() or proc.stdout.strip() or f"edit failed: {name}")
    for name in diff.extra:
        proc = _gh("label", "delete", name, "--yes")
        if proc.returncode != 0:
            errors.append(proc.stderr.strip() or proc.stdout.strip() or f"delete failed: {name}")
    return errors


def _print_plan(diff: LabelDiff) -> None:
    if diff.missing:
        print(f"create ({len(diff.missing)}):")
        for name in diff.missing:
            print(f"  {name}")
    if diff.description_mismatch:
        print(f"edit description ({len(diff.description_mismatch)}):")
        for name, _actual, wanted in diff.description_mismatch:
            print(f"  {name} -> {wanted}")
    if diff.extra:
        print(f"delete ({len(diff.extra)}):")
        for name in diff.extra:
            print(f"  {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="mutate the live repo (create / edit / delete). Default is dry-run.",
    )
    args = parser.parse_args(argv)

    fixed = parse_fixed_set(GH_DOC.read_text(encoding="utf-8"))
    live = live_labels()
    if live is None:
        print("github labels: UNKNOWN — gh could not list labels.", file=sys.stderr)
        return 0

    diff = diff_labels(fixed, live)
    if not diff.missing and not diff.extra and not diff.description_mismatch:
        print(f"github labels: ok — live set matches docs/GITHUB.md ({len(fixed)} labels).")
        return 0

    print(
        f"github labels: drift — {len(diff.missing)} missing, "
        f"{len(diff.extra)} unsanctioned, "
        f"{len(diff.description_mismatch)} description mismatch."
    )
    _print_plan(diff)

    if not args.apply:
        print("\nRe-run with --apply to mutate. Not a CI gate.")
        return 1

    errors = apply_diff(diff, fixed)
    if errors:
        print("github labels: APPLY FAILED", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 2

    after = live_labels()
    if after is None:
        print("github labels: applied, but could not re-list.", file=sys.stderr)
        return 2
    leftover = diff_labels(fixed, after)
    if leftover.missing or leftover.extra or leftover.description_mismatch:
        print("github labels: applied, but drift remains.", file=sys.stderr)
        _print_plan(leftover)
        return 2
    print(f"github labels: applied — live set matches docs/GITHUB.md ({len(fixed)} labels).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
