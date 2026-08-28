---
title: Service architecture
type: reference
status: active
version: v0.1.0
tags: [services, architecture, ssot]
description: "The service tree's architecture: layout, layering, domain modules, and conventions. Ships as a placeholder."
applies_when:
  - When placing new code in the service tree.
  - When checking the service's layering and module conventions.
related_adrs:
  - adr-02-stack
---
# SERVICES — service architecture

> This file is **expected** and currently a placeholder. Instantiation writes
> it once `{{service tree}}` exists ([[CLONE]]).

## What it must eventually contain

- **Layout** — the service tree's top-level structure: `{{service tree}}` and its module/area convention.
- **Framework** — `{{domain framework}}` and `{{interface framework}}` as this repo programs them (the stack decision: [[adr-02-stack]]).
- **Layering** — where handlers, domain services, and data access live; the pure-compute boundary.
- **Authorization** — the permission-class pattern and where checks happen.
- **Toolchain** — `{{service toolchain}}` commands for run, check, and test; pins in [[REQUIREMENTS]].
- **Conventions** — naming, file placement, and the things this tree deliberately never does.
