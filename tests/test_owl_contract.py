#!/usr/bin/env python3
"""Guard The Owl's web research contract and markdown findings format."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_KEYS = {
    "name",
    "description",
    "model",
    "color",
    "tools",
    "related_adrs",
}
GRAPHIFY_FIRST = (
    "query_graph",
    "get_neighbors",
    "get_node",
    "shortest_path",
)


def agent_parts(stem: str) -> tuple[str, str]:
    path = ROOT / "agents" / f"{stem}.md"
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path.relative_to(ROOT)} has no frontmatter"
    end = text.find("\n---\n", 4)
    assert end != -1, f"{path.relative_to(ROOT)} has unclosed frontmatter"
    return text[4:end], text[end + 5 :]


def frontmatter_tools(frontmatter: str) -> list[str]:
    match = re.search(r"^tools:\n((?:  - .+\n?)+)", frontmatter, re.MULTILINE)
    assert match, "frontmatter has no tools block"
    return re.findall(r"^  - (\S+)\s*$", match.group(1), re.MULTILINE)


def assert_closed_frontmatter(stem: str, frontmatter: str) -> list[str]:
    keys = re.findall(
        r"^([a-z][a-z0-9_]*):(?:\s|$)",
        frontmatter,
        re.MULTILINE,
    )
    assert len(keys) == len(AGENT_KEYS) and set(keys) == AGENT_KEYS, (
        f"{stem} frontmatter keys must be exactly {sorted(AGENT_KEYS)}, got {keys}"
    )
    assert re.search(rf"^name:\s*{re.escape(stem)}\s*$", frontmatter, re.MULTILINE)
    assert re.search(r"^model:\s*inherit\s*$", frontmatter, re.MULTILINE)

    tools = frontmatter_tools(frontmatter)
    assert tools[:4] == list(GRAPHIFY_FIRST), (
        f"{stem} must list Graphify first, got {tools[:4]}"
    )
    assert tools.index("Read") > 3
    assert tools.index("Glob") > tools.index("Read")
    return tools


def test_owl_frontmatter_and_tools() -> None:
    frontmatter, body = agent_parts("hb-ag-owl")
    tools = assert_closed_frontmatter("hb-ag-owl", frontmatter)
    assert "Agent" not in tools, "The Owl must not have the Agent tool"
    assert "Write" not in tools, "The Owl must not have the Write tool"
    assert "Edit" not in tools, "The Owl must not have the Edit tool"
    assert "You are **The Owl** (`hb-ag-owl`)" in body


def test_owl_skill_contract() -> None:
    skill_path = ROOT / "skills" / "hb-sk-owl" / "SKILL.md"
    assert skill_path.is_file(), "skills/hb-sk-owl/SKILL.md is missing"
    text = skill_path.read_text(encoding="utf-8")
    assert "Markdown Findings Report" in text or "Standard Markdown Findings Report" in text
    assert "Sources & Citations" in text
    assert "Key Findings" in text


def main() -> int:
    test_owl_frontmatter_and_tools()
    test_owl_skill_contract()
    print("all 2 Owl contract test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
