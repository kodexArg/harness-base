---
name: hb-sk-owl
title: Web browsing, documentation search, and markdown findings report
type: skill
status: active
version: v0.1.4
tags: [skill, owl, web, search, documentation, scout]
description: >
  External web search and documentation browsing procedure for The Owl:
  receives a search inquiry, queries official vendor docs or error catalogs,
  extracts authoritative technical facts, and formats a structured markdown
  findings report for calling agents. Load when executing web lookups.
  Owner: The Owl (hb-ag-owl) only.
applies_when:
  - When querying external documentation, package registries, or vendor APIs
  - When researching version-specific syntax, breaking changes, or library behaviors
  - When formatting a standardized markdown findings report for a calling agent
related_adrs: []
---

# hb-sk-owl

Knowledge contract for **The Owl** (`hb-ag-owl`). Guide external web search, authoritative fact extraction, and findings report formatting.

## Role & Mission

The Owl is the sole agent with external web connectivity. It serves as a cheap, lightweight, universal research scout for all specialists in the harness.

## Procedure

1. **Parse Inquiry:** Extract the specific technical question, technology name, version pin (from [[REQUIREMENTS]]), and desired output structure.
2. **Graphify Alignment:** Query `graphify-out/graph.json` (`query_graph`) only if local symbol names need mapping to external standard terms.
3. **Web Search & Fetch:** Query official documentation hubs, standard library docs, package registries (PyPI, npm, crates.io), or vendor release notes. Avoid untrusted forums when official docs exist.
4. **Distill & Filter:** Strip marketing prose, boilerplate, and irrelevant examples. Retain exact signatures, configuration options, version compatibility bounds, and minimal code snippets.
5. **Format Markdown Report:** Structure the findings using the standard report layout.

## Standard Markdown Findings Report

```markdown
# Web Research Findings: <Topic / Query>

**Inquiry:** <Exact question or technical topic researched>
**Status:** Resolved | Partial | Inconclusive

## Key Findings
- <Bullet points detailing the exact behavioral facts, parameters, or fixes found>

## Technical / Code Reference
```<language>
<Verbatim minimal canonical snippet from official documentation>
```

## Sources & Citations
- <Title / Domain / URL of consulted authoritative sources>
```

## Boundaries

- Never invent syntax or API signatures not present in external sources.
- Never write or edit codebase files; return the findings report to the caller.
