"""Guardian watchlists. One of two copies; the other is each guardian's Watchlist section.

Instantiation ([[CLONE]]): add this project's route-surface globs to
`kbot-api` (the service's route/handler file shapes) and its manifest globs
to `kbot-adr` (the package manifests the stack decision pins).
"""

from __future__ import annotations

import fnmatch

WATCHLISTS = {
    "kbot-prd": (
        "docs/PRD.md",
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        ".github/workflows/*",
    ),
    "kbot-adr": (
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
    "kbot-api": (
        "docs/INTERFACES.md",
        "docs/contracts/*",
    ),
}


def matching_guardians(rel: str, watchlists: dict | None = None) -> list[str]:
    """Return guardian names whose watchlist glob hits `rel`."""
    lists = WATCHLISTS if watchlists is None else watchlists
    hits: list[str] = []
    for agent, patterns in lists.items():
        for pattern in patterns:
            if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(
                rel, pattern.rstrip("*") + "*"
            ):
                hits.append(agent)
                break
    return hits
