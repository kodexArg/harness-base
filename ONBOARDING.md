# Onboarding — {{project name}}

Welcome. The objective ([PRD](docs/PRD.md)) is **{{one-line product statement}}**.

The harness is **the support of that objective, not the objective** — the PRD's own words. A
live documentation system plus skills, hooks and guardian agents, oriented to growth by
addition without compromising the foundations. It exists so the product can be
built safely; it is not the thing being built.

Owner: **{{owner}}**.

> Fresh from the template? Run [docs/CLONE.md](docs/CLONE.md) first — this file
> reads as a fill-in guide until instantiation replaces its `{{placeholders}}`.

## Read these two first — and keep them open

The whole project runs on a single discipline: **[docs/PRD.md](docs/PRD.md)** and
**[docs/INTERFACES.md](docs/INTERFACES.md)** are held in memory at all times. Read both at the start of
every session; re-read whenever they change. No other file carries this standing requirement.

Then read the entry index: **[AGENTS.md](AGENTS.md)** (= `CLAUDE.md`). It is a trustworthy
index — reach content through its wikilinks instead of re-scanning the repo.

## The ABC gate — verify before adding ANYTHING

Every change, no matter how small, passes three questions:

1. **Does it follow [PRD](docs/PRD.md)?**
2. **Does it comply with the ADRs?** (`adrs/` = `.claude/rules/`)
3. **Does it modify [INTERFACES](docs/INTERFACES.md)?**

## How we work

- **Development loop** ([docs/DEVELOPMENT-LOOP.md](docs/DEVELOPMENT-LOOP.md)):
  `idea → user-facing? → … → needs the service? → enter through INTERFACES`.
  The service zone is entered and exited **only through [INTERFACES.md](docs/INTERFACES.md)**: an
  interface is valid if and only if it has a row there. Undeclared route in code = defect.
- **TDD** for every service piece ([docs/TDD.md](docs/TDD.md), `docs/tdds/`).
- **Guardians** (AGENTS.md "Agents" section) — three subagents gate the SSOTs:
  `kbot-prd`, `kbot-adr`, `kbot-api`. Engage the matching guardian
  **before** touching PRD, the ADRs, or INTERFACES; the dispatch discipline is the safety net, not the trigger.
  Their verdicts are binding.

## The skill harness — vendored, self-contained

The **required skills travel with the repo**. They are real copies under `skills/`
(git-tracked, what the harness loads) — no dependence on any machine's
global skill harness, so a fresh clone works anywhere. The inventory and the "why" for each
is [docs/HARNESS.md](docs/HARNESS.md).

Use them as the sanctioned path, not optional aids: the surface → the surface-skill
templates, the service → the service-skill templates, cloud → the cloud skill, git → the git
skill. Skills **reinforce** the ABC gate; they never waive it or a guardian verdict.

## Doctrine that will surprise you

- **Toolchains are fixed** by [adr-02](adrs/adr-02-stack.md) — no substitute package managers.
- **Everything that is code is English** — always; the screen renders in the interface
  language ([adr-01](adrs/adr-01-nomenclature.md)).
- **Secrets live in the project's secret store only**; the inventory is
  [docs/VARIABLES.md](docs/VARIABLES.md).
- ADRs state **rules, never information**; facts live in `docs/` and are reached by wikilink
  ([adr-00](adrs/adr-00-adr-doctrine.md)).

## Git

| Branch | Role |
|--------|------|
| `main` | **The single line** — default PR target *and* production. `main` IS live: every push ships. |

Issues + PRs are the default surface. Direct push to `main`: **{{owner}} only** — everyone
else uses feature branches and PRs into `main`. There is no production branch. Release tags are semver `v*`,
cut from `main`, and record what shipped rather than triggering it.
Detail: [docs/GITHUB.md](docs/GITHUB.md) · [adr-08](adrs/adr-08-github.md).

## Local setup

- Service: `{{service tree}}` (`{{domain framework}}`, `{{service toolchain}}`).
- Surface: `{{surface tree}}` (`{{surface framework}}`, `{{surface toolchain}}`) — absent when headless.
- Local orchestration: root **`{{local runtime}}`** only.
- Copy `.env.example` → `.env` (names from [docs/VARIABLES.md](docs/VARIABLES.md); no secrets in git).

## Where we are

The project advances in stages, and **which one is current is [docs/ROADMAP.md](docs/ROADMAP.md)'s to say** — this
file does not restate it, because a second copy goes stale the moment a stage moves.

## Doc map

- **Product**: [PRD](docs/PRD.md) · [GLOSSARY](docs/GLOSSARY.md) · [ROADMAP](docs/ROADMAP.md)
- **Contracts**: [INTERFACES](docs/INTERFACES.md) · [VARIABLES](docs/VARIABLES.md) · [REQUIREMENTS](docs/REQUIREMENTS.md) · [GITHUB](docs/GITHUB.md)
- **Stack**: [SERVICES](docs/SERVICES.md) · [AUTH](docs/AUTH.md) · [DB](docs/DB.md) · [INFRASTRUCTURE](docs/INFRASTRUCTURE.md)
- **Method**: [TDD](docs/TDD.md) · [DEVELOPMENT-LOOP](docs/DEVELOPMENT-LOOP.md)
- **Harness**: [HARNESS](docs/HARNESS.md) — required skills, vendored
- **Template**: [CLONE](docs/CLONE.md) — instantiation guide
