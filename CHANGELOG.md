# CHANGELOG

Every change landing on `main` records an entry here in the same batch
([[adr-05-after-versioning]]). Version format: `vA.B.C`.

## v0.1.4 — 2026-08-29

Add The Paladin for surgical, framework-neutral Python business logic
and complex scripts: implementation first, then Trickster-owned tests.
Add The Adventurer as the parent-dispatched single-agent lane for
complete triage cards totaling below 5 with no axis above 2; it carries
one bounded implementation plus tests with broad context, default
effort, and no subagents. Agent files keep the HARNESS closed
frontmatter set (`name`/`model`/`tools`), distinct from docs/ADRs.
The Dwarf carries `adr-03.b-tdd`. Adventurer work may start from a
Hunter bulletin or a parent card; the PR remains required, the issue
does not.

## v0.1.3 — 2026-08-29

Hunting party at **The Three Feathers** (Las Tres Plumas): The Hunter
pins a noise-stripped issue bulletin (`problem` + one imperative `goal`)
for a later Hunter. Hawk and Hound scout in parallel; The Hunter
reproduces against existing tests (quick-exit). Issue `gh` is the
hunting party; The Bard still ships git/PR.

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
