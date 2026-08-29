#!/usr/bin/env python3
"""Overlay docs/adrs/agents headings onto graph.json with no LLM key.

After a --code-only AST extract, Graphify skips markdown. This pass adds
file, stem, title, and heading nodes plus wikilink edges so query_graph
can find the roster. Replaces any prior overlay (_origin: harness-docs).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
GRAPH_JSON = ROOT / "skills" / "kskill-graphify" / "graphify-out" / "graph.json"
ORIGIN = "harness-docs"
TREES = ("docs", "adrs", "agents")
ROOT_MARKDOWN = ("AGENTS.md", "CLAUDE.md")
HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
YOU_ARE = re.compile(r"You are \*\*(.+?)\*\*")
FRONTMATTER_NAME = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)
FRONTMATTER_TITLE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)


class Overlay(NamedTuple):
    nodes: tuple[dict, ...]
    edges: tuple[dict, ...]


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return (s or "x")[:80]


def node_id(source_file: str, kind: str, label: str, line: int) -> str:
    return f"harness_docs_{slug(source_file)}_{kind}_{slug(label)}_l{line}"


def clean_heading(raw: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
    return text.replace("**", "").replace("`", "").strip()


def iter_markdown_files(root: Path) -> list[Path]:
    seen: set[int] = set()
    files: list[Path] = []
    for tree in TREES:
        directory = root / tree
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            inode = path.stat().st_ino
            if inode in seen:
                continue
            seen.add(inode)
            files.append(path)
    for name in ROOT_MARKDOWN:
        path = root / name
        if not path.is_file():
            continue
        inode = path.stat().st_ino
        if inode in seen:
            continue
        seen.add(inode)
        files.append(path)
    return files


def stem_index(files: list[Path], root: Path) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in files:
        rel = path.relative_to(root).as_posix()
        index[path.stem] = rel
        index[path.stem.lower()] = rel
    return index


def _skip_frontmatter(lines: list[str]) -> int:
    if not lines or lines[0].strip() != "---":
        return 0
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return i + 1
    return 0


def extract_file(path: Path, root: Path, wiki: dict[str, str]) -> Overlay:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    body_at = _skip_frontmatter(lines)
    nodes: list[dict] = []
    edges: list[dict] = []
    community = int(hashlib.md5(rel.encode("utf-8")).hexdigest(), 16) % 50 + 50

    def add_node(kind: str, label: str, line: int) -> str:
        nid = node_id(rel, kind, label, line)
        nodes.append(
            {
                "id": nid,
                "label": label,
                "_callable": False,
                "_origin": ORIGIN,
                "community": community,
                "file_type": "document",
                "norm_label": label.lower(),
                "source_file": rel,
                "source_location": f"L{line}",
            }
        )
        return nid

    file_id = add_node("file", rel, 1)
    stem_id = add_node("stem", path.stem, 1)
    edges.append(_edge(file_id, stem_id, "contains", rel, 1))

    fm = "\n".join(lines[:body_at])
    name_m = FRONTMATTER_NAME.search(fm)
    if name_m and name_m.group(1) != path.stem:
        nid = add_node("name", name_m.group(1), 1)
        edges.append(_edge(file_id, nid, "contains", rel, 1))
    title_m = FRONTMATTER_TITLE.search(fm)
    if title_m:
        title = title_m.group(1).strip().strip('"')
        if title:
            nid = add_node("title", title, 1)
            edges.append(_edge(file_id, nid, "contains", rel, 1))

    in_fence = False
    cited: set[str] = set()
    seen_titles: set[str] = set()
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if i > body_at:
            heading = HEADING.match(line)
            if heading:
                label = clean_heading(heading.group(2))
                if label:
                    hid = add_node("heading", label, i)
                    edges.append(_edge(file_id, hid, "contains", rel, i))
            you = YOU_ARE.search(line)
            if you and you.group(1) not in seen_titles:
                seen_titles.add(you.group(1))
                nid = add_node("title", you.group(1), i)
                edges.append(_edge(file_id, nid, "contains", rel, i))
        for token in WIKILINK.findall(line):
            target = wiki.get(token) or wiki.get(token.lower())
            if target and target != rel:
                cited.add(target)

    for target in sorted(cited):
        tid = node_id(target, "file", target, 1)
        edges.append(_edge(file_id, tid, "cites", rel, 1))
    return Overlay(nodes=tuple(nodes), edges=tuple(edges))


def _edge(source: str, target: str, relation: str, source_file: str, line: int) -> dict:
    return {
        "source": source,
        "target": target,
        "relation": relation,
        "_origin": ORIGIN,
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "context": relation,
        "source_file": source_file,
        "source_location": f"L{line}",
        "weight": 1.0,
    }


def build_overlay(root: Path) -> Overlay:
    files = iter_markdown_files(root)
    wiki = stem_index(files, root)
    nodes: list[dict] = []
    edges: list[dict] = []
    for path in files:
        part = extract_file(path, root, wiki)
        nodes.extend(part.nodes)
        edges.extend(part.edges)
    return Overlay(nodes=tuple(nodes), edges=tuple(edges))


def merge_overlay(graph: dict, overlay: Overlay) -> dict:
    nodes = [n for n in graph.get("nodes") or [] if n.get("_origin") != ORIGIN]
    edges = [e for e in graph.get("edges") or [] if e.get("_origin") != ORIGIN]
    known = {n["id"] for n in nodes}
    for node in overlay.nodes:
        if node["id"] not in known:
            nodes.append(node)
            known.add(node["id"])
    edge_keys = {(e.get("source"), e.get("target"), e.get("relation")) for e in edges}
    for edge in overlay.edges:
        key = (edge["source"], edge["target"], edge["relation"])
        if key not in edge_keys:
            edges.append(edge)
            edge_keys.add(key)
    out = dict(graph)
    out["nodes"] = nodes
    out["edges"] = edges
    return out


def main(argv: list[str] | None = None) -> int:
    del argv
    if not GRAPH_JSON.is_file():
        print(f"missing {GRAPH_JSON.relative_to(ROOT)}", file=sys.stderr)
        return 2
    graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    overlay = build_overlay(ROOT)
    merged = merge_overlay(graph, overlay)
    GRAPH_JSON.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"harness-docs overlay: {len(overlay.nodes)} nodes, "
        f"{len(overlay.edges)} edges -> {GRAPH_JSON.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
