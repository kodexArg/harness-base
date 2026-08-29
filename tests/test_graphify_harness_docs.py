"""No-LLM harness markdown overlay for Graphify graph.json."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "graphify_harness_docs.py"
GRAPH_JSON = ROOT / "skills" / "kskill-graphify" / "graphify-out" / "graph.json"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def load():
    spec = importlib.util.spec_from_file_location("graphify_harness_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extracts_headings_stems_and_wikilinks() -> None:
    module = load()
    overlay = module.build_overlay(ROOT)
    labels = {n["label"] for n in overlay.nodes}
    for needed in (
        "docs/ADND-AGENTS.md",
        "ADND-AGENTS",
        "hb-ag-hunter",
        "The Hunter",
        "adr-35-graphify",
    ):
        if needed not in labels:
            fail(f"overlay missing label {needed!r}")
            return
    cites = [e for e in overlay.edges if e["relation"] == "cites"]
    if not cites:
        fail("expected wikilink cites edges")
        return
    print("  overlay has stems, The Hunter, and wikilink cites")


def test_merge_replaces_prior_overlay() -> None:
    module = load()
    graph = {
        "nodes": [
            {"id": "ast_a", "label": "Foo", "_origin": "ast"},
            {"id": "old", "label": "stale", "_origin": module.ORIGIN},
        ],
        "edges": [
            {"source": "ast_a", "target": "x", "relation": "calls", "_origin": "ast"},
            {"source": "old", "target": "x", "relation": "contains", "_origin": module.ORIGIN},
        ],
    }
    overlay = module.Overlay(
        nodes=(
            {
                "id": "new",
                "label": "The Hunter",
                "_origin": module.ORIGIN,
            },
        ),
        edges=(
            {
                "source": "new",
                "target": "ast_a",
                "relation": "cites",
                "_origin": module.ORIGIN,
            },
        ),
    )
    merged = module.merge_overlay(graph, overlay)
    origins = [n["_origin"] for n in merged["nodes"]]
    if origins.count(module.ORIGIN) != 1 or "stale" in {n["label"] for n in merged["nodes"]}:
        fail(f"overlay was not replaced: {merged['nodes']}")
        return
    if any(n["id"] == "ast_a" for n in merged["nodes"]) is False:
        fail("AST node was dropped")
        return
    print("  merge strips old harness-docs nodes and keeps AST")


def test_tracked_graph_has_overlay_when_present() -> None:
    if not GRAPH_JSON.is_file():
        fail("graph.json missing")
        return
    payload = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    overlay_nodes = [n for n in payload.get("nodes") or [] if n.get("_origin") == "harness-docs"]
    if not overlay_nodes:
        print("  SKIPPED: graph.json has no harness-docs overlay yet")
        return
    labels = {n["label"] for n in overlay_nodes}
    if "The Hunter" not in labels or "hb-ag-hunter" not in labels:
        fail(f"tracked overlay lacks roster labels; got {len(labels)} labels")
        return
    print(f"  tracked graph overlay has {len(overlay_nodes)} nodes including The Hunter")


def main() -> int:
    tests = [
        test_extracts_headings_stems_and_wikilinks,
        test_merge_replaces_prior_overlay,
        test_tracked_graph_has_overlay_when_present,
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
