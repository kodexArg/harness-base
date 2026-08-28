---
name: hb-sk-surface-framework
title: Surface framework host contract — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, surface-framework, warrior, trickster]
description: >
  The surface framework contract for this repo's rendering host and its
  interactive components. Load when adding or changing a page, layout,
  host configuration, or hydration choice, or when writing surface
  tests for those pages — even if the skill is not named. Owner: The
  Warrior (hb-ag-surface). The Trickster (hb-ag-test) may load this
  skill for surface tests. The surface's own toolchain only. Not the
  catalog.
applies_when:
  - When adding or changing a {{surface framework}} page, layout, or host configuration
  - When choosing a hydration directive on a {{component framework}} component
  - When The Trickster writes surface tests against pages or components
related_adrs:
  - adr-02-stack
---

# hb-sk-surface-framework

Knowledge contract for **The Warrior**, and for **The Trickster** when planting surface tests. Teach the {{surface framework}} host in this project, then stop.

## Load

1. Read the project's surface architecture doc (named at instantiation) and [[SERVICES]].
2. Doctrine stays in that architecture doc; pins in [[REQUIREMENTS]].
3. Pages bind to rows already declared in [[INTERFACES]] — never to an invented path.

## This project

Rendering mode, host adapter, hydration defaults, and where non-trivial
markup lives are recorded here at instantiation:

- Rendering mode and adapter: `{{surface rendering mode}}`
- Hydration default: `{{hydration default}}`
- Page shape: thin host page + `{{component framework}}` view (`hb-sk-component-framework`)

Toolchain: **{{surface toolchain}}** — never a substitute.

## Do not

- Invent an endpoint or a path. The Warrior requests interfaces from The Cleric (`hb-ag-contracts`) as content-needed (fields, page, UI need). If the Cleric says adapt an existing row, adapt the component.
- Author tests as The Warrior. The Trickster (`hb-ag-test`) may load this skill for surface tests.
- Load Dwarf / Cleric / Wizard / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the surface framework's name).
A headless project deletes this skill, `hb-sk-component-framework`, and
`hb-ag-surface` together. See `docs/CLONE.md`.
