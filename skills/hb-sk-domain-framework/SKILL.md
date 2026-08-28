---
name: hb-sk-domain-framework
title: Domain framework this-repo contract — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, domain-framework, dwarf]
description: >
  The domain framework contract as this repo programs it: models,
  settings, domain services, pure-compute boundaries, and the service
  toolchain. Load when writing models, settings, or services under the
  service tree — even if unnamed. Owner: The Dwarf (hb-ag-service).
  TDD and tests: The Trickster (hb-ag-test, hb-sk-tdd). The service's
  own toolchain only. Not the catalog.
applies_when:
  - When authoring a {{domain framework}} model, constraint, setting, or domain service
  - When placing compute in a request handler vs a pure-compute service module
related_adrs:
  - adr-02-stack
---

# hb-sk-domain-framework

Knowledge contract for **The Dwarf**. Teach this project's {{domain framework}}, then stop.

## Load

1. Read the stack SSOT for this layer ([[SERVICES]]) and the pins in [[REQUIREMENTS]].
2. Loop: the Cleric's [[INTERFACES]] row (read) → wait for the Trickster's failing TDD (`hb-ag-test`, `hb-sk-tdd`) → models → handlers (`hb-sk-interface-framework`). Missing row → The Cleric. Do not write `docs/tdds/` or tests.
3. Toolchain: **{{service toolchain}}**, never a substitute. Pins live in [[REQUIREMENTS]].

## This project

At instantiation this section records the framework-specific rules this repo
programs by — the constraint spellings, the settings surfaces, the
pure-compute boundary (no framework imports inside `{{service tree}}` service
modules), and the authorization pattern. Until then it holds placeholders:

- Framework rules: `{{domain framework rules}}`
- Pure-compute boundary: `{{pure-compute boundary}}`
- Authorization pattern: `{{authorization pattern}}`

## Do not

- Write `docs/tdds/` or tests — The Trickster (`hb-ag-test`, `hb-sk-tdd`).
- Write the local runtime (The Wizard) or `docs/INTERFACES.md` (The Cleric).
- Substitute the toolchain, add an unsanctioned dependency, or invent routing doctrine.
- Load Warrior / Cleric / Trickster / Wizard / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the domain framework's name).
See `docs/CLONE.md`.
