#!/usr/bin/env python3
"""ci_select.py: same path list → same slice. No git required."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_merge_gate  # noqa: E402
import ci_select  # noqa: E402


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def test_surface_only_skips_service() -> None:
    sel = ci_select.classify(["surface/src/lib/foo.ts", "surface/tests/foo.test.ts"])
    if sel.service:
        fail("surface-only diff must not run the service job")
    if not sel.surface:
        fail("surface-only diff must run the surface job")
    if sel.merge_gate:
        fail("surface-only diff must not run merge-gate")
    ok("surface-only skips service and merge-gate")


def test_interfaces_doc_runs_service() -> None:
    sel = ci_select.classify(["docs/INTERFACES.md"])
    if not sel.service:
        fail("docs/INTERFACES.md must run the service job")
    if sel.service_args:
        fail("INTERFACES.md must run the full service suite, not an area slice")
    if not sel.merge_gate:
        fail("docs/INTERFACES.md must run merge-gate")
    if sel.surface:
        fail("INTERFACES.md must not run the surface job")
    ok("INTERFACES.md runs full service + merge-gate")


def test_service_area_slice() -> None:
    sel = ci_select.classify(
        [
            "service/billing/handlers.py",
            "service/billing/test_handlers.py",
        ]
    )
    if not sel.service or sel.service_args != "service/billing":
        fail(f"billing-only should slice service/billing, got {sel.service_args!r}")
    if sel.surface or sel.harness:
        fail("billing-only must not wake surface or harness")
    ok("billing-only slices service/billing")


def test_tdds_force_full_service() -> None:
    sel = ci_select.classify(["docs/tdds/tdd-01-example.md"])
    if not sel.service or sel.service_args:
        fail("docs/tdds/ must force the full service suite")
    if sel.merge_gate:
        fail("docs/tdds/ is not an SSOT watchlist path")
    ok("tdds force full service and skip merge-gate")


def test_ci_yml_keeps_dot_github() -> None:
    sel = ci_select.classify([".github/workflows/ci.yml"])
    if not sel.harness or "tests/test_ci_select.py" not in sel.harness_files:
        fail(f"ci.yml must map to its own guard, got {sel}")
    if "tests/test_every_test_file_runs.py" not in sel.harness_files:
        fail(f"ci.yml must map to the runner audit, got {sel}")
    if not sel.merge_gate:
        fail("ci.yml is on the prd and adr watchlists")
    ok("ci.yml path is not stripped and maps to its guards")


def test_an_unmapped_workflow_runs_the_whole_harness() -> None:
    sel = ci_select.classify([".github/workflows/some-new-pipeline.yml"])
    if not sel.harness or not sel.harness_files:
        fail(f"an unmapped workflow must run the harness, got {sel}")
    if "tests/test_ci_select.py" not in sel.harness_files:
        fail(f"expected the full harness, got {sel.harness_files}")
    if not sel.merge_gate:
        fail("an unmapped workflow is still a .github/workflows hit")
    ok("an unmapped workflow falls back to the whole harness")


def test_quick_win_skills_map() -> None:
    sel = ci_select.classify(["skills/kskill-qw/SKILL.md"])
    if not sel.harness or "tests/test_quick_win_skills.py" not in sel.harness_files:
        fail(f"kskill-qw must map to its harness test, got {sel.harness_files}")
    if "tests/test_micro_solid_font.py" not in sel.harness_files:
        fail("kskill-qw must also map to the micro-solid font test")
    ok("kskill-qw maps to test_quick_win_skills")


def test_graphify_skill_maps_to_its_guards() -> None:
    sel = ci_select.classify(["skills/kskill-graphify/SKILL.md"])
    if not sel.harness or "tests/test_kskill_graphify.py" not in sel.harness_files:
        fail(f"kskill-graphify must map to its harness test, got {sel.harness_files}")
    if "tests/test_graphify.py" not in sel.harness_files:
        fail("kskill-graphify must also map to the graphify test")
    ok("kskill-graphify maps to its guards")


def test_agents_map_to_the_agent_guards() -> None:
    sel = ci_select.classify(["agents/hb-ag-service.md"])
    for expected in (
        "tests/test_agents_are_subagents.py",
        "tests/test_hb_ag_roster.py",
        "tests/test_agent_model_inherit.py",
    ):
        if expected not in sel.harness_files:
            fail(f"an agent change must select {expected}, got {sel.harness_files}")
    if not sel.merge_gate:
        fail("an agent file is on the adr watchlist")
    ok("agents map to the agent guards")


def test_adrs_map_to_the_adr_guards() -> None:
    sel = ci_select.classify(["adrs/adr-02-stack.md"])
    for expected in (
        "tests/test_adr_frontmatter.py",
        "tests/test_wikilink_targets.py",
    ):
        if expected not in sel.harness_files:
            fail(f"an ADR change must select {expected}, got {sel.harness_files}")
    if not sel.merge_gate:
        fail("an ADR change must run the merge gate")
    ok("adrs map to the adr guards + merge gate")


def test_merge_gate_follows_watchlists() -> None:
    watchlists = check_merge_gate.load_watchlists()
    watched = [
        "AGENTS.md",
        "README.md",
        "agents/hb-ag-service.md",
        ".github/workflows/ci.yml",
        "docs/PRD.md",
        "docs/INTERFACES.md",
        "docs/VARIABLES.md",
        "docs/contracts/contract-billing.md",
        "CHANGELOG.md",
    ]
    unwatched = [
        "docs/tdds/tdd-01-example.md",
        "surface/src/lib/foo.ts",
        "service/billing/handlers.py",
    ]
    for path in watched:
        if not check_merge_gate.ssots_for(path, watchlists):
            fail(f"fixture {path} must hit a watchlist")
        if not ci_select.classify([path]).merge_gate:
            fail(f"watched path {path} must run merge-gate")
    for path in unwatched:
        if check_merge_gate.ssots_for(path, watchlists):
            fail(f"fixture {path} must not hit a watchlist")
        if ci_select.classify([path]).merge_gate:
            fail(f"unwatched path {path} must not run merge-gate")
    if not ci_select.classify(["scripts/ssot_watchlists.py"]).merge_gate:
        fail("editing the watchlist module must run merge-gate")
    ok("merge-gate job tracks SSOT watchlists")


def test_surface_test_file_selects_itself() -> None:
    sel = ci_select.classify(["surface/tests/thing.test.ts"])
    if "surface/tests/thing.test.ts" not in sel.surface_files:
        fail(f"a surface test must select itself, got {sel.surface_files}")
    ok("a surface test selects itself")


def test_unknown_surface_surface_runs_the_whole_suite() -> None:
    sel = ci_select.classify(["surface/Dockerfile"])
    if not sel.surface or sel.surface_files:
        fail(f"an unrecognised surface file must run every test, got {sel.surface_files}")
    ok("unrecognised surface surface runs the whole suite")


def test_service_slice_never_matches_by_filename() -> None:
    sel = ci_select.classify(["service/billing/ingestion.py"])
    if sel.service_args != "service/billing":
        fail(f"service must slice by area directory, not by filename, got {sel.service_args!r}")
    ok("service arm slices whole area dirs, so no naming convention can hide a test")


def test_idempotent() -> None:
    paths = ["surface/src/a.ts", "docs/INTERFACES.md"]
    a = ci_select.classify(paths)
    b = ci_select.classify(list(reversed(paths)))
    if (a.service, a.service_args, a.surface, a.harness_files, a.merge_gate) != (
        b.service,
        b.service_args,
        b.surface,
        b.harness_files,
        b.merge_gate,
    ):
        fail("classify is not idempotent under path order")
    ok("same paths → same selection")


if __name__ == "__main__":
    test_surface_only_skips_service()
    test_interfaces_doc_runs_service()
    test_service_area_slice()
    test_tdds_force_full_service()
    test_ci_yml_keeps_dot_github()
    test_an_unmapped_workflow_runs_the_whole_harness()
    test_quick_win_skills_map()
    test_graphify_skill_maps_to_its_guards()
    test_agents_map_to_the_agent_guards()
    test_adrs_map_to_the_adr_guards()
    test_merge_gate_follows_watchlists()
    test_surface_test_file_selects_itself()
    test_unknown_surface_surface_runs_the_whole_suite()
    test_service_slice_never_matches_by_filename()
    test_idempotent()
    sys.exit(0)
