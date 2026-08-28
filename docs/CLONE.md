---
title: Instantiation guide — a new project from harness-base
type: reference
status: active
version: v0.1.0
tags: [harness, clone, instantiation, template]
description: "Step-by-step instantiation of harness-base into a new project: placeholders, prefix rename, the stack decision, trees, and first commit."
applies_when:
  - When creating a new project from the harness-base template.
  - When auditing whether an instantiation left placeholders behind.
related_adrs:
  - adr-02-stack
  - adr-05-after-versioning
---
# CLONE — instantiating harness-base

harness-base is the stack-agnostic project harness template, successor of
`harness-default`, born from the evolution of `alvs-financial-gateway` (a
Django/Astro/AWS treasury product) into a reusable, product-free harness. Where
that lineage shows through as an example — a Kotlin service, a flat site — it
is illustration, never prescription.

Operator steps for a new project from this template. Order matters where
noted.

## 1. Copy the template

Copy the tree, not the git history:

```bash
cp -r /path/to/harness-base /path/to/my-project
cd /path/to/my-project
git init
```

## 2. Fill every placeholder

Every product- or stack-specific string in the template is a placeholder in
double curly braces — English, lowercase, spaced. Replace each one everywhere
it appears:

```bash
grep -rn "{{" --exclude-dir=.git . | sort
```

The full inventory:

| Placeholder | Replaced by | Example |
|---|---|---|
| `{{project name}}` | the product's prose name | `Acme Billing Console` |
| `{{company name}}` | the company or organization | `Acme` |
| `{{owner}}` | the GitHub owner account | `acme-co` |
| `{{repo}}` | the repository name | `acme-billing-console` |
| `{{project slug}}` | the slug used in names, hosts, env seeds | `acme-billing` |
| `{{prefix}}` | the product kind prefix that replaces `hb-` | `abc-` |
| `{{interface language}}` | the screen's human language | `Spanish (es-AR)` |
| `{{interface locale}}` | the screen's locale | `es-AR` |
| `{{number format}}` | locale number format | `1.234.567,89` |
| `{{date format}}` | locale date format | `DD/MM/YYYY` |
| `{{timezone}}` | the product's timezone | `America/Argentina/Buenos_Aires` |
| `{{service tree}}` | the service code root | `service/` (a Kotlin service), `backend/` |
| `{{surface tree}}` | the surface code root | `web/`, `frontend/` — deleted when headless |
| `{{main flow}}` | the one-line data flow | `source → store → service → surface` |
| `{{domain framework}}` | the service's domain framework | `Django`, `Rails`, `Ktor` |
| `{{interface framework}}` | the service's interface framework | `DRF`, `FastAPI`, `Ktor Routing` |
| `{{surface framework}}` | the surface host framework | `Astro`, `Next.js` |
| `{{component framework}}` | the surface component framework | `Svelte`, `React` |
| `{{service toolchain}}` | the service's package/run toolchain | `uv`, `gradle`, `cargo` |
| `{{surface toolchain}}` | the surface's package/run toolchain | `bun`, `pnpm` |
| `{{test runner}}` | the service test runner | `pytest`, `JUnit` |
| `{{local runtime}}` | the local orchestration file | `compose.yaml`, `Procfile` |
| `{{local runtime profiles}}` | the local runtime's profiles | `db / service / surface / full` |
| `{{local ports}}` | the local stack's ports | `5432 / 8000 / 4321` |
| `{{cloud provider}}` | the cloud platform | `AWS`, `GCP`, `Fly.io` |
| `{{deploy target}}` | the deployment layout | `two Fargate services`, `one VPS` |
| `{{region}}` | the deploy region | `us-east-1` |
| `{{host}}` | the product's public host | `billing.acme.com` |
| `{{database}}` | the database engine | `PostgreSQL 17` |
| `{{data layer}}` | the service's data access layer | `Django ORM + Psycopg` |
| `{{secret store}}` | the secret store | `AWS Secrets Manager`, `Vault` |
| `{{secret naming}}` | the secret naming scheme | `acme/<env>/<project>/*` |
| `{{secret exceptions}}` | bounded exceptions to the secret store, or "none" | `none` |
| `{{infrastructure absences}}` | what the layout deliberately lacks | `no NAT, no cache server` |
| `{{baseline sizing}}` | the deployment baseline size | `1 task, 256/512` |
| `{{service integrations}}` | the service's external integrations | `S3, SES` |
| `{{surface styling}}` | the surface's styling stack | `Tailwind 4` |
| `{{surface rendering mode}}` | the surface host's rendering mode | `SSR, standalone adapter` |
| `{{hydration default}}` | the default hydration choice | `none — static unless declared` |
| `{{api prefix}}` | the catalog's declared path prefixes | `/api/`, `/admin/` |
| `{{handler idiom}}` | the handler + path idiom | `APIView + path()` |
| `{{payload split pattern}}` | the read/write payload split pattern | `ReadSerializer vs WriteSerializer` |
| `{{permission pattern}}` | the permission-class pattern | `GroupBasedPermission subclasses` |
| `{{authorization pattern}}` | where authorization lives | `service-side permission classes` |
| `{{identity provider}}` | who authenticates | `Cognito`, `Auth0`, `session login` |
| `{{domain framework rules}}` | the framework rules this repo programs by | `CheckConstraint(condition=)` |
| `{{pure-compute boundary}}` | the pure-compute rule | `no framework imports in services/` |
| `{{component reactivity idiom}}` | the component reactivity idiom | `signals`, `runes` |
| `{{component composition idiom}}` | the component composition idiom | `snippets + render` |
| `{{product kind}}` | what kind of product this is | `SaaS workspace`, `CLI tool` |
| `{{project terms}}` | the project's domain glossary section | one row per term, [[GLOSSARY]] |
| `{{author name}}` / `{{author email}}` / `{{author role}}` | an author of record | [[CLAUDE-TEAM]] |
| `{{stage N}}` | a roadmap stage | [[ROADMAP]] |
| `{{package}}` / `{{version}}` / `{{date}}` / `{{why this pin}}` | a pin row | [[REQUIREMENTS]] |
| `{{VARIABLE_NAME}}` / `{{PUBLIC_VARIABLE_NAME}}` / `{{scope}}` / `{{envs}}` / `{{source}}` / `{{description}}` / `{{yes/no}}` | a variable row | [[VARIABLES]] |
| `{{REQ-DOMAIN-NN}}` / `{{requirement summary}}` / `{{open issues}}` / `{{closed issues}}` | a requirement-id row | [[REQ]] |
| `{{user role N}}` / `{{need N}}` / `{{core capability N}}` / `{{observable acceptance criterion N}}` | the PRD's product content | [[PRD]] |
| `{{one paragraph naming the product: what it is, what it reads, what it serves}}` | the PRD opening paragraph | [[PRD]] |
| `{{primary read story}}` / `{{primary exception story}}` / `{{primary action story}}` / `{{precondition}}` / `{{user action}}` / `{{observable outcome}}` / `{{a condition that needs attention}}` / `{{the product evaluates it}}` / `{{the responsible user sees an actionable result}}` / `{{an authorized user identifies a required action}}` / `{{they perform it in the product}}` / `{{the action is validated, recorded, and attributable}}` | the PRD's gherkin scenario slots | [[PRD]] |
| `{{one-line product statement}}` | the product in one line | `AGENTS.md`, `ONBOARDING.md` |
| `{{service responsibilities}}` / `{{surface responsibilities}}` | what each tree owns, in prose | `AGENTS.md` |
| `{{component extension}}` | the surface's component file extension | `.cursor/rules/section-articles.mdc` |
| `{{ruleset id}}` | the GitHub ruleset id | `scripts/apply_main_ruleset.py` |
| `{{technology}}` | the technology a stack-skill folder is renamed to | `hb-sk-*` instantiation notes |
| `{{GET}}` / `{{/api/example/}}` / `{{handler name}}` / `{{payload shape or —}}` / `{{permission class}}` / `{{what it serves; link payload shapes into docs/contracts/}}` | the INTERFACES example row | [[INTERFACES]] |
| `{{example term}}` / `{{canonical form}}` / `{{forbidden forms}}` | the GLOSSARY example row | [[GLOSSARY]] |
| `{{PLACEHOLDER}}` | `.env.example` seed values | `.env.example` |

One-shot fill-in content (PRD gherkin scenarios, the INTERFACES example row,
the GLOSSARY example row, the roadmap stages) is written fresh at
instantiation rather than search-replaced — the placeholders mark where.
Numbered families (`{{user role 1}}`, `{{user role 2}}`, `{{stage 1}}`, …) are
listed once in the table as their `N`-form.

**Not placeholders:** GitHub Actions `${{ … }}` expressions in
`.github/workflows/` are CI syntax, and mermaid's `{{…}}` hexagon syntax
documented inside `skills/kskill-report/` is literal brace syntax — neither is
filled at instantiation.

**Vendored-skill template slots.** The reusable skills carry their own
`{{UPPERCASE}}` fill-at-use slots — `kskill-report`'s HTML templates
(`{{TITLE}}`, `{{HOOK}}`, `{{STAT_LABEL}}`, …) and `diagram-design`'s
templates. Those are inputs to the skill at render time, documented in each
`SKILL.md`; they are not instantiation placeholders and are not replaced here.

## 3. Batch-rename the `hb-` prefix

`hb-` is the template's own product prefix. Pick the project's prefix (short,
lowercase, ending in a dash) and rename every `hb-sk-*` and `hb-ag-*` artifact
and every reference to them — skills, agents, docs, tests, and the roster
tables move in the same batch ([[HARNESS]]: a rename of an artifact moves every
reference in the same batch):

```bash
grep -rl "hb-sk-\|hb-ag-" --exclude-dir=.git . | xargs sed -i 's/hb-sk-/abc-sk-/g; s/hb-ag-/abc-ag-/g'
```

Then rename the directories: `git mv skills/hb-sk-contracts skills/abc-sk-contracts`,
`git mv agents/hb-ag-service.md agents/abc-ag-service.md`, and so on. Run
`python3 -m pytest tests/ -q` (or `python3 tests/test_<x>.py` per file) — the
roster guard (`tests/test_hb_ag_roster.py`, renamed alongside) asserts the new
stems.

## 4. Make the stack decision

Fill `adrs/adr-02-stack.md` — it ships as the placeholder shape of the
decision, not the decision. Choose the service stack, the surface stack (or
delete that section), infrastructure, and the development variant. Record the
pins in [[REQUIREMENTS]].

## 5. Create the stack trees

Create `{{service tree}}` and (unless headless) `{{surface tree}}`. Then:

- Wire the trees into `scripts/ci_select.py` (`SERVICE_PREFIXES` /
  `SURFACE_PREFIXES`) and `scripts/guardian_watchlists.py` (route-surface
  globs for `kbot-api`).
- Fill [[SERVICES]], [[INFRASTRUCTURE]], [[DB]], [[AUTH]], [[VARIABLES]],
  [[REQUIREMENTS]], [[ROADMAP]] — they ship as placeholders that say what they
  must contain.
- Write the first real row of [[INTERFACES]] before the first route.

## 6. Instantiate the stack-skill templates

Each `hb-sk-*` template (after the prefix rename, `abc-sk-*`) holds the
contract shape with `{{placeholders}}` for the chosen technology. Fill each
one, then rename the folder to name the technology: `abc-sk-domain-framework`
→ `abc-sk-django`, `abc-sk-test-runner` → `abc-sk-pytest`, and so on. Update
the skill names in each agent definition's body and in [[HARNESS]]'s required
skills table in the same batch.

## 7. Delete the surface agent if headless

A headless project deletes, in one batch: `agents/hb-ag-surface.md`,
`skills/hb-sk-surface-framework/`, `skills/hb-sk-component-framework/`, and
every roster/dispatch row that names The Warrior ([[ADND-AGENTS]],
[[ADND-DISPATCH]], [[HARNESS]], `AGENTS.md`, `tests/test_hb_ag_roster.py`).
The Cleric then mediates between the caller and The Dwarf directly.

## 8. First commit and remote

```bash
git add -A
git commit -m "chore(harness): instantiate harness-base as {{project name}}"
gh repo create {{owner}}/{{repo}} --private --source . --push
```

Then apply the branch ruleset (`scripts/apply_main_ruleset.py`, after filling
its `{{owner}}`/`{{repo}}` and ruleset id), fill [[PRD]] and [[CLAUDE-TEAM]],
and open the first issue. The development loop ([[DEVELOPMENT-LOOP]]) takes
over from there.

## Done when

No `{{placeholder}}` remains outside vendored-skill templates
(`grep -rn "{{" --exclude-dir=.git .` shows only `kskill-report` /
`diagram-design` slots), no `hb-` prefix remains, [[adr-02-stack]] names a real
stack, the trees exist, and `python3 -m pytest tests/ -q` is green.
