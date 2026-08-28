# CHANGELOG

Every change landing on `main` records an entry here in the same batch
([[adr-05-after-versioning]]). Version format: `vA.B.C`.

## v0.1.2 — 2026-08-28

Restore the backend (`adr-03` + subs) and frontend (`adr-04` + subs) ADR
families as stack-agnostic templates: fill slots, rewrite technologies, delete
subs this project does not use.

## v0.1.1 — 2026-08-28

Incoming-agent fill-in map (`docs/ONBOARDING.md`): placeholder inventory by
file, distinct from `AGENTS.md`. Graphify install is requested when the host
can (`bin/ensure`). Clearer slot names on the INTERFACES example row, PRD
paragraphs, REQUIREMENTS pins, and `.env.example`.

## v0.1.0 — 2026-08-28

Initial harness-base: the stack- and infrastructure-agnostic project harness
template. Successor of `harness-default`; generalized from the harness that
grew up around a production SaaS product into a product-free template.

- Seven area-owner agents (`hb-ag-*`): contracts, service, surface, ops, test,
  judge, git — roster and dispatch graphs in `docs/ADND-*.md`.
- Eleven product-skill templates (`hb-sk-*`) plus the reusable harness skills
  (`kskill-*`) and `diagram-design`, all vendored.
- Twelve ADRs: the doctrine set (00/01 series, 05, 07, 08, 35) plus
  `adr-02-stack` as the placeholder stack decision.
- Full docs set: PRD template, HARNESS inventory, development loop, GITHUB
  delivery contract, TDD manual, glossary, and placeholder SSOTs.
- Harness self-tests under `tests/`, Cursor session hooks, Graphify MCP
  wiring, and the instantiation guide `docs/CLONE.md`.
