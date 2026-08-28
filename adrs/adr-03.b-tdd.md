---
title: adr-03.b-tdd
type: adr
status: active
version: v0.1.2
tags: [tdd, testing]
description: "Service code is born through docs/tdds/ specs and failing tests first."
applies_when:
  - When creating or changing service models, handlers, or domain services.
  - When writing or closing a TDD entry under docs/tdds/.
related_agents:
  - hb-ag-test
---

# ADR-03.b — TDD

> Test-first specs bind service code to declared contracts before the implementation exists.

Instantiation: keep this sub unless the project is truly not a tested service. Surface tests stay under the frontend family / [[adr-04-frontend]], still written by The Trickster.

1. **Service TDD.** Service code under `{{service tree}}` is born through the [[TDD]] flow. Unspecified service additions are not the path.

2. **Lifecycle.** Each unit of work has `docs/tdds/tdd-NN-slug.md`: `draft` → `red` → `green` → `done`.

3. **Red first.** Implementation follows failing tests in `red` ([[DEVELOPMENT-LOOP]]). Runner: `{{test runner}}`.

4. **Scope.** One TDD entry, one coherent unit. This sub does not govern surface-only tests.
