#!/usr/bin/env python3
"""SSOT watchlists for the merge-gate job.

Instantiation ([[CLONE]]): add this project's route-surface globs to `api`
and its package-manifest globs to `adr`.
"""

from __future__ import annotations

import fnmatch

WATCHLISTS = {
    "prd": (
        "docs/PRD.md",
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        ".github/workflows/*",
    ),
    "adr": (
        "agents/*",
        ".claude/rules/*",
        "adrs/*",
        ".github/workflows/*",
        "docs/REQUIREMENTS.md",
        "docs/GLOSSARY.md",
        "docs/INFRASTRUCTURE.md",
        "docs/VARIABLES.md",
        "CHANGELOG.md",
    ),
    "api": (
        "docs/INTERFACES.md",
        "docs/contracts/*",
    ),
}


def matching_ssots(rel: str, watchlists: dict | None = None) -> list[str]:
    """Return SSOT keys whose watchlist glob hits `rel`."""
    lists = WATCHLISTS if watchlists is None else watchlists
    hits: list[str] = []
    for ssot, patterns in lists.items():
        for pattern in patterns:
            if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(
                rel, pattern.rstrip("*") + "*"
            ):
                hits.append(ssot)
                break
    return hits
