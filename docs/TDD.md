---
title: Service Test-Driven Development instruction manual and TDD lifecycle
type: reference
status: active
version: v0.1.2
tags: [harness, tdd, service, testing]
description: "Manual governing test-driven development workflows and specification authoring in docs/tdds/."
applies_when:
  - When initiating service development through the TDD flow.
  - When authoring TDD specifications under docs/tdds/.
related_adrs:
  - adr-02-stack
  - adr-03-backend
---
# TDD — instruction manual for `docs/tdds/`

Owner: **The Trickster** (`hb-ag-test`) via `hb-sk-tdd`. The Dwarf implements after red; The Dwarf never writes this tree or the tests.

Every new service piece is born here, wherever its subject exists ([[DEVELOPMENT-LOOP]]). This manual rules the format; the `tdd-NN` entries live under `docs/tdds/`.

## Scope

This manual is the `docs/tdds/` service specification. Surface testing follows the surface architecture doc; The Trickster still **writes** those tests (may load `hb-sk-surface-framework`). Other `hb-ag-*` agents are forbidden from writing tests.

## Purpose

From activation onward, every new piece of service code is **born here**. `docs/tdds/` is where service code generation starts — never directly in the code. No model, handler, service, or command exists before its TDD entry does.

## The flow

1. An approved [[INTERFACES]] row exists — The Cleric wrote it (the contract comes first).
2. The Trickster creates `docs/tdds/tdd-NN-slug.md` — sequential `NN`, kebab-case slug — following the section layout described below.
3. The Trickster writes the failing tests the entry lists. Run them; they must fail.
4. The Dwarf writes the model changes and implements until the tests can pass.
5. The Trickster greens / adds more. No shadow tests from other agents.
6. The Trickster marks the entry `done`.

## Entry frontmatter contract

Every entry carries:

```yaml
title: tdd-NN-slug
type: tdd
status: draft | red | green | done
created: YYYY-MM-DD
api: []        # list of the [[INTERFACES]] rows/paths this entry covers
tags: [tdd]
```

Status transitions:

- `draft` — entry written, tests not yet coded.
- `red` — tests exist and fail; implementation may begin.
- `green` — implementation passes every listed test.
- `done` — implementation notes filled; entry closed.

An entry covers a single coherent unit of code: a model plus its handlers, a service, a command. Entries are small. If an entry needs a plural of concerns, split it.

## Entry layout

Every entry follows the frontmatter contract and flow above; a project's first entry sets the section layout that the rest reuse (`docs/tdds/tdd-00-template.md`). Do not invent divergent layouts.
