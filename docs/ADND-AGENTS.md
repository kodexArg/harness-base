---
title: Product area-owner agents — roster and who they know
type: reference
status: active
version: v0.1.0
tags: [harness, agents, hb-ag]
description: "SSOT for the hb-ag-* roster: stem, title, area, skills, and which other agents each one must know. Includes the soft dispatch graphs."
applies_when:
  - When dispatching or writing an hb-ag-* area owner.
  - When choosing who owns a tree vs who is called next.
related_adrs:
  - adr-01-nomenclature
  - adr-02-stack
  - adr-07-git
  - adr-08-github
---

# ADND-AGENTS — the product area owners

> Who owns which tree, and who they are allowed to call. The graphs of *how to proceed from a prompt* live in the included file [[ADND-DISPATCH]].

Inventory and kind prefixes stay in [[HARNESS]]. Names and forbidden forms stay in [[GLOSSARY]]. This file is the **working roster** a parent session or a dispatched `hb-ag-*` reads after [[PRD]] and [[INTERFACES]].

**Included:** [[ADND-DISPATCH]] — soft graphs (prompt class → first agent → then if). Do not copy those graphs here.

Host-agnostic: the stems below are the names. Where a host runtime exposes a native subagent type for a stem, the definition file is the same; otherwise the **parent** loads `agents/<stem>.md` and still obeys this roster. The playbook is the markdown, not the host.

## Roster

| Stem | Title | File | Owns (write) | Skills | `Agent` |
|---|---|---|---|---|---|
| `hb-ag-contracts` | The Cleric ✝️ | `agents/hb-ag-contracts.md` | `docs/INTERFACES.md`, `docs/contracts/` **only** | `hb-sk-contracts` only | **yes** → Dwarf, Warrior, Trickster |
| `hb-ag-service` | The Dwarf 🔨 | `agents/hb-ag-service.md` | `{{service tree}}` **only** (not `docs/tdds/`, not tests) | `hb-sk-domain-framework`, `hb-sk-interface-framework` | **yes** → Cleric (Trickster for tests; Wizard for infra; **never** Warrior) |
| `hb-ag-surface` | The Warrior 🗡️ | `agents/hb-ag-surface.md` | `{{surface tree}}` except tests | `hb-sk-component-framework`, `hb-sk-surface-framework` | **yes** → Cleric (Trickster for tests; Wizard for infra; **never** Dwarf) |
| `hb-ag-ops` | The Wizard 🧙 | `agents/hb-ag-ops.md` | the local runtime, cloud/CI/secrets surfaces named in [[INFRASTRUCTURE]], [[VARIABLES]] — not app trees, not [[INTERFACES]] | `hb-sk-local-runtime`, `hb-sk-cloud` | infra only (prefer parent) |
| `hb-ag-judge` | The Inquisitor ⚖️ | `agents/hb-ag-judge.md` | **nothing**. Read-only. Reports only. | **none** — does not load skills | **no** |
| `hb-ag-test` | The Trickster 🃏 | `agents/hb-ag-test.md` | `docs/tdds/`, service tests, surface tests, harness tests. No product code, no screen, no [[INTERFACES]] | `hb-sk-tdd`, `hb-sk-test-runner`; may load `hb-sk-surface-framework` for surface tests | **no** — returns the traps |
| `hb-ag-git` | The Bard 🎶 | `agents/hb-ag-git.md` | **nothing** in product trees. Only git + GitHub via Bash (`git`, `gh`) | `hb-sk-git` | **no** |

Areas do not overlap. Tool allowlists cannot path-filter `Write`; the **body** of each agent file is the bound.

**Decouple surface ↔ service.** The Warrior never Agents The Dwarf. The Dwarf never Agents The Warrior. Only The Cleric carries messages both ways.

**The Bard is the only `hb-ag-*` allowed to interact with Git and GitHub.** No other area owner may `git`, `gh`, push, PR, merge, or commit. Their Bash is not a loophole. Quick-exit: git/GitHub → Bard.

**The Warrior is optional.** A headless project deletes `hb-ag-surface`, `hb-sk-surface-framework`, and `hb-sk-component-framework` in one batch ([[CLONE]]).

These are not archived `kbot-*` lobes and not the `kwf-*` delivery party. `kwf-warrior` was the *service* builder of `triage-and-fix`; `kwf-archer` was the *surface* builder; `kwf-bard` was a publish node. Titles here are inverted on purpose ([[GLOSSARY]]). Forbidden: unprefixed `warrior` / `archer` / `cleric` / `trickster` / `bard`; restoring `The Archer` as a live title; restoring `kbot-*` builders.

## Each agent knows the others

Every live `hb-ag-*` definition must name the stems it may call. A parent that implements instead of dispatching is out of area.

### The Cleric (`hb-ag-contracts`)

✝️ Sole writer of [[INTERFACES]] and `docs/contracts/`. Translates a Warrior **interface ask** (content needed: fields, page, UI need in `{{interface language}}` — not framework, not paths, not payload shapes) into a six-column row and/or a request to The Dwarf.

Knows and may call:

- **The Dwarf** — forge only after the row lands, and only if the need has logic, lives in domain+model, and is **not** already computable from data already served. If already computable: tell The Warrior to adapt — no new row.
- **The Warrior** — deliver the contract (row) or the adaptation instruction.
- **The Trickster** — TDD entry + failing tests after a new row; never product code.

Does not write `{{service tree}}` or `{{surface tree}}`. Does not emit ABC verdicts — that is The Inquisitor (and, for *writing* `adrs/`, the guardian `kbot-adr`). Does not `git` / `gh` — that is The Bard.

### The Dwarf (`hb-ag-service`)

🔨 Forges `{{service tree}}` only. Never writes tests or `docs/tdds/`. Never Agents The Warrior.

Knows and may call:

- **The Cleric** — catalog row missing or wrong; never edit [[INTERFACES]] yourself. Accept a Cleric request only if (1) it has logic, (2) it lives in domain+model, (3) it is **not** already computable from data already served. If already computable: reply to The Cleric "tell the Warrior to adapt" — no new row. If new: wait for the row, then forge.
- **The Trickster** — via the Cleric, or a direct request-for-tests. The Dwarf does not write the tests.
- **The Wizard** — local runtime, cloud, secrets, CI. Dispatch; do not eat infra.

Does not know The Warrior as someone to call. Does not `git` / `gh` — that is The Bard.

### The Warrior (`hb-ag-surface`)

🗡️ The screen in `{{interface language}}`. Writes `{{surface tree}}` except tests. Never Agents The Dwarf. Optional — a headless project deletes it.

Knows and may call:

- **The Cleric** — request interfaces as **content needed** (fields, page, UI need). Not framework, not paths, not payload shapes.
- **The Trickster** — after the screen is built, for surface tests (`hb-sk-surface-framework` is allowed there; not the Trickster's specialty).
- **The Wizard** — local runtime / cloud / secrets. Dispatch; do not eat infra.

Does not carry the contracts ADR. The service owns fragment markup; the surface host loads the client. Does not `git` / `gh` — that is The Bard.

### The Wizard (`hb-ag-ops`)

🧙 Devops for **this** repo only: the local runtime, the cloud layout, secrets names in [[INFRASTRUCTURE]] / [[VARIABLES]]. The agent file exists; the parent may dispatch it. Stop-and-name is over.

Knows: does not write `{{surface tree}}`, `{{service tree}}`, tests, or [[INTERFACES]]. Skills `hb-sk-local-runtime`, `hb-sk-cloud`. Does not `git` / `gh` — that is The Bard.

### The Inquisitor (`hb-ag-judge`)

⚖️ Read-only. Reports only. Does not load skills — looks inward at **this** harness and at logic already in code. If we did it a certain way before, insist it was that way. `hb-sk-abc` stays as a **parent** fallback; this agent does not load it.

Quick-exit reports. If findings pile up: say remaining ~70% unexplored but this is enough. Full explore only if insisted. Prefer a lightweight high-context model at dispatch; agent `model:` stays `inherit` ([[HARNESS]]). **Not a merge gate.**

**Not** the guardian `kbot-adr`. The guardian is dispatched when *writing* `adrs/` (watchlist in [[AGENTS]]). The Inquisitor is dispatched when *judging* a diff or an ADR claim. Does not spawn Dwarf / Warrior / Trickster to "fix" a finding. Does not `git` / `gh`.

### The Trickster (`hb-ag-test`)

🃏 Owns every test write: `docs/tdds/`, service tests, surface tests, harness tests. No product code, no screen, no [[INTERFACES]]. Cannot "give face."

Knows: **no** `Agent` — returns the traps. Does not spawn builders to fix a red. After The Cleric's row: write the TDD entry + failing unit tests; The Dwarf implements; then green / add more. After The Warrior builds: may load `hb-sk-surface-framework` for surface tests. Other agents are forbidden from writing tests (no shadow tests). Does not `git` / `gh` — that is The Bard.

### The Bard (`hb-ag-git`)

🎶 The only `hb-ag-*` that may touch Git or GitHub. Writes **nothing** in product trees. Bash is `git` and `gh` only.

Knows: **no** `Agent`. Does not write app code to "fix while shipping." `main` is the single line; only `{{owner}}`; a PR is required; `--admin` when an owner merge would wait on checks ([[adr-08-github]]). Skill `hb-sk-git`.

## Guardians vs area owners

| Role | Stems | Writes product trees? |
|---|---|---|
| Area owners | `hb-ag-*` | yes, each one tree (Inquisitor: no; Trickster: tests only; Bard: git/gh only) |
| Guardians | `kbot-prd`, `kbot-adr`, `kbot-api` | the watched SSOT they gate, per [[HARNESS]] |

Do not dispatch a guardian to implement a screen. Do not dispatch The Cleric to emit `Guardian-Verdict:`.

## First act (dispatched `hb-ag-*`)

`SessionStart` does not reach a subagent ([[HARNESS]]). Read [[PRD]] and [[INTERFACES]], then this file, then the included [[ADND-DISPATCH]] if the prompt class is not already obvious from the area you own.
