---
title: Gate table for main versus branch development
type: reference
status: active
version: v0.1.0
tags: [harness, branch, git, gates]
description: "Gate matrix specifying checks enforced on main versus branch development mode."
applies_when:
  - When evaluating branch protection rules on main.
  - When checking dirty push policies during local development.
  - When validating PR merge gates.
related_adrs:
  - adr-05-after-versioning
  - adr-08-github
---
# BRANCH-MODE — the gate x mode table

States branch-development mode directly: the gate table below, and which
checks postpone to PR time versus stay enforced on every branch.

## Gate x mode table

| Gate | Protected (main) | Branch-development mode (any other branch) |
|---|---|---|
| Issue before work ([[DEVELOPMENT-LOOP]] §0.5) | Required, per change | Not required mid-branch; must exist by the time a PR opens |
| PR as sole entry to main ([[adr-08-github]] rule 2) | Required, unchanged | Unchanged — still the only path to main |
| ADR conformance | Owner process / PR | Owner process / PR |
| Interface-row conformance | Owner process / PR | Owner process / PR |
| `Plan-Verdict:` record | Owner process / PR | Owner process / PR |
| PR-flow commit on main | GitHub branch protection | GitHub branch protection |
| Push-to-main | GitHub branch protection | GitHub branch protection |
| Tests / TDD flows | Enforced | Enforced, unchanged, no exception |
| VARIABLES SSOT | Owner process / PR | Owner process / PR |

## Honesty note on how re-enforcement actually happens at PR time

[[GITHUB]] requires `Plan-Verdict:` lines and test
suites to be green before merge. How that re-enforcement happens:

- **It is not a file-write hook.** There are no PostToolUse hooks.
- **The actual re-enforcement is the recorded `Plan-Verdict:`**, run as an explicit
  step of the merge procedure: before merging a PR into `main`, the
  integrating agent records a `Plan-Verdict:` for every SSOT whose watchlist
  the diff hits, and `scripts/check_merge_gate.py` checks those lines per [[GITHUB]].
  This is a procedural discipline, not a hook-enforced mechanism.
- If the agent returns to `main` and re-writes a watchlisted file there, re-enforcement is still the recorded `Plan-Verdict:`, not a hook.

## See also

- [[DEVELOPMENT-LOOP]], [[GITHUB]] — the rules this mode adds a bounded,
  branch-scoped reading to.
