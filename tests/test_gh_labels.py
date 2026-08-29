"""Guard for the repository's GitHub label set.

docs/GITHUB.md owns the fixed label set ([[adr-08-github]] rule 6).
scripts/sync_gh_labels.py parses that table and can apply it.
This test PARSES via the script rather than typing the set out.

The live half needs authenticated `gh`. Where that is unavailable the live
comparison is SKIPPED. This file must never become a merge gate that depends
on a network.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "sync_gh_labels.py"
GH_DOC = REPO_ROOT / "docs" / "GITHUB.md"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load():
    spec = importlib.util.spec_from_file_location("sync_gh_labels", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_heading_matches_the_doc() -> None:
    module = load()
    text = GH_DOC.read_text(encoding="utf-8")
    if module.TABLE_HEADING not in text:
        fail(
            f"{GH_DOC.relative_to(REPO_ROOT)} no longer contains "
            f"{module.TABLE_HEADING!r}"
        )
        return
    print(f"  heading {module.TABLE_HEADING!r} is in docs/GITHUB.md")


def test_parse_fixed_set_from_doc() -> None:
    module = load()
    fixed = module.parse_fixed_set(GH_DOC.read_text(encoding="utf-8"))
    required = {
        "bug",
        "feat",
        "harness",
        "invalid",
        "cursor-issue-triage",
        "🟢 severity:1",
        "prd-approved",
    }
    missing = required - set(fixed)
    if missing:
        fail(f"parsed set is missing required names: {sorted(missing)}")
        return
    if len(fixed) < 40:
        fail(f"expected a full catalog, parsed {len(fixed)} labels")
        return
    print(f"  docs/GITHUB.md declares {len(fixed)} labels")


def test_parse_stops_at_next_h2() -> None:
    module = load()
    text = (
        f"{module.TABLE_HEADING}\n\n"
        "| Label | Use |\n"
        "|---|---|\n"
        "| `feat` | New capability |\n"
        "\n## Merge-gate contract (CI job `pr-merge-gate`)\n\n"
        "| `leak` | Must not parse |\n"
    )
    fixed = module.parse_fixed_set(text)
    if fixed != {"feat": "New capability"}:
        fail(f"expected only feat; got {fixed}")
        return
    print("  parse stops at the next h2")


def test_diff_labels_names_and_descriptions() -> None:
    module = load()
    fixed = {"feat": "New capability", "bug": "Defect"}
    live = {"bug": "Something isn't working", "wontfix": "No"}
    diff = module.diff_labels(fixed, live)
    if diff.missing != ("feat",):
        fail(f"missing: {diff.missing}")
        return
    if diff.extra != ("wontfix",):
        fail(f"extra: {diff.extra}")
        return
    if [row[0] for row in diff.description_mismatch] != ["bug"]:
        fail(f"mismatch: {diff.description_mismatch}")
        return
    print("  diff reports missing, extra, and description mismatch")


def test_github_description_fits() -> None:
    module = load()
    long_use = "x" * (module.GITHUB_DESCRIPTION_MAX + 20)
    out = module.github_description(f"**{long_use}**")
    if len(out) > module.GITHUB_DESCRIPTION_MAX:
        fail(f"description is {len(out)} chars")
        return
    if "**" in module.github_description("**Owner only**"):
        fail("markup was not stripped")
        return
    print("  GitHub descriptions strip markup and fit 100 chars")


def test_color_for_verdicts_before_adr_prefix() -> None:
    module = load()
    if module.color_for("adr-approved") == module.color_for("adr-08"):
        fail("verdict labels must not share the ADR-number colour")
        return
    print("  adr-approved is not coloured as an ADR-number label")


def test_live_set_matches_fixed_set() -> None:
    module = load()
    fixed = module.parse_fixed_set(GH_DOC.read_text(encoding="utf-8"))
    live = module.live_labels()
    if live is None:
        print(
            "  SKIPPED (live): `gh label list` unavailable. "
            "The live half of this guard did NOT run."
        )
        return

    missing = sorted(set(fixed) - set(live))
    unsanctioned = sorted(set(live) - set(fixed))
    problems = []
    if missing:
        problems.append("missing from the live repo: " + ", ".join(missing))
    if unsanctioned:
        problems.append("present live but not in docs/GITHUB.md: " + ", ".join(unsanctioned))
    if problems:
        fail(
            "the repository label set has drifted from docs/GITHUB.md "
            "(adr-08-github rule 6):\n    - " + "\n    - ".join(problems)
        )
        return
    print(f"  live label set matches docs/GITHUB.md ({len(fixed)} labels)")


def main() -> int:
    tests = [
        test_heading_matches_the_doc,
        test_parse_fixed_set_from_doc,
        test_parse_stops_at_next_h2,
        test_diff_labels_names_and_descriptions,
        test_github_description_fits,
        test_color_for_verdicts_before_adr_prefix,
        test_live_set_matches_fixed_set,
    ]
    failed = 0
    for fn in tests:
        print(f"{fn.__name__}:")
        before = len(failures)
        try:
            fn()
        except Exception as exc:
            fail(f"{fn.__name__}: {exc}")
        if len(failures) > before:
            failed += 1
            print(f"FAIL: {failures[-1]}", file=sys.stderr)

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {len(tests)} test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
