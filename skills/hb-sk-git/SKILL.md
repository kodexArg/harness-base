---
name: hb-sk-git
title: Git and GitHub — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, git, github, bard]
description: >
  Git and GitHub contract for this repo: single-trunk main, ephemeral
  branches, scoped commits, PR as the integration record, operator
  --admin merge when checks would wait. Load when committing, pushing,
  opening or merging a PR, or running gh or git — even if the skill is
  not named. Triggers: commit, push, PR, merge, gh, git, bard. Owner:
  The Bard (hb-ag-git) only. Other agents do not git or gh.
applies_when:
  - When committing, pushing, opening a PR, or merging onto main
  - When Issues or merge need the operator PAT instead of an app token
  - When another agent would run git or gh (refuse; this skill's owner only)
related_adrs:
  - adr-07-git
  - adr-08-github
---

# hb-sk-git

🎶 Knowledge contract for **The Bard**. Teach how this repo lands on `main`. Then stop. Point; do not paste the SSOTs.

## Load

1. [[GITHUB]] — branches, `gh` credential, labels, merge `--admin`, issue threads.
2. [[adr-07-git]] — single trunk, ephemeral branches, scoped commits.
3. [[adr-08-github]] — PR invariant, merge tiers, the owner `--admin` rule.
4. [[DEVELOPMENT-LOOP]] — issue in, PR out; the PR is the record.
5. Agent contract fields: [[HARNESS]].

First act of the owner agent: Graphify, then [[GITHUB]], then `git status` / `git diff` / `git log`.

## This repo

`main` is the only line. A merged PR ships. No write tools — the Bard sings; it does not compose.

| Move | Here |
|---|---|
| Commit | Only when parent/user said commit / push / merge / ship. Why, 1–2 sentences, HEREDOC. Subject: [[adr-07-git]]. Match `git log`. Never `.env` / secrets |
| Branch | Cut from `main`, prefixes in [[GITHUB]]. Delete on merge. Retention window: [[GITHUB]] |
| PR | Always. `gh pr create`. Base `main`. Do not invent `Guardian-Verdict:` — owner process |
| Merge | `gh pr merge`. Owner order is immediate. `--admin` when checks would wait ([[adr-08-github]]). Never end on "pending CI" |
| Auth | `. scripts/cursor_cloud_gh_auth.sh` when Issues or merge need the operator PAT, not an app token |
| Issues | When asked. Threads: [[GITHUB]] (REST, not `--comments`). Labels: the fixed set |

`Bash` is `git`, `gh`, and that auth source. Not the test runner. Not the surface toolchain. Not cloud CLIs.

## Quick exit

A page, a model, a catalog row, tests, infra, or ABC — not this song. Name The Warrior / The Dwarf / The Cleric / The Trickster / The Wizard / The Inquisitor.

## Do not

- Force-push `main`, skip hooks, amend others' commits, merge without a PR.
- Invent a secret, a label, or a thirteenth verdict.
- Write product trees. Load Warrior / Dwarf / Cleric / Trickster / Wizard / Inquisitor skills.
- Hand git/gh to another agent.

## Instantiation

This is a template skill: replace every `{{placeholder}}` (`{{owner}}`,
`{{repo}}`), then rename the folder to `{{prefix}}-sk-git`. See
`docs/CLONE.md`.
