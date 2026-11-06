# Principal Engineering OMP template

Repository-local engineering governance, deterministic prompt routing, focused skills, specialist agents, and validation for Oh My Pi.

## Requirements

- OMP `18.16.0` is the verified compatibility target.
- Python 3.9 or later runs the dependency-free validator/tests.
- The template adds no global OMP configuration, provider credential, MCP server, package install, or standalone Bun dependency. Normal OMP use still requires an operator-configured model.

## Install

Run the installer from a trusted, provenance-verified copy of this template:

```bash
python3 scripts/apply_template.py /path/to/target-project
```

It copies only `.omp/`, `AGENTS.md`, and `CONTEXT.md`. It refuses to overwrite any of those target paths. Preview or explicitly replace the selected paths with:

```bash
python3 scripts/apply_template.py /path/to/target-project --dry-run
python3 scripts/apply_template.py /path/to/target-project --replace --dry-run
python3 scripts/apply_template.py /path/to/target-project --replace
```

`--replace` removes only the target `.omp/`, `AGENTS.md`, and `CONTEXT.md` after staging new copies; unrelated project files remain untouched. Review existing selected paths before using it. Extensions are executable code, while agent and skill files are repository-controlled instructions/data. None is trusted merely because it is project-local. For an untrusted target repository, apply and inspect the result only in a sandbox without host credentials, writable host paths, or unrestricted network access.

In the target project, verify OMP discovery:

```bash
omp config list --scope project --json
omp skill list --json
omp
```

OMP discovers the root `AGENTS.md`, `.omp/skills/*/SKILL.md`, `.omp/agents/*.md`, and `.omp/extensions/prompt-router.ts` automatically. Use ordinary prompts—no slash command is required:

```text
Fix the reorg bug in our blockchain indexer.
Design a multi-chain RFQ service.
Audit this Solidity contract.
Review my changes.
Implement this small validation change.
```

The router injects selected skill names. OMP then reads the corresponding `skill://...` bodies progressively. Consecutive prompts with the same route do not repeat routing context, and subagents rely on agent `autoloadSkills` rather than being routed again.

## What is native and what is custom

| Capability | Implementation |
|---|---|
| Governance/context | Native root `AGENTS.md` discovery |
| Skill discovery and `skill://` loading | Native OMP |
| Natural-language deterministic classification | Project extension using verified `before_agent_start` |
| Specialist agents | Native `.omp/agents/*.md` |
| General scout/review/security/task agents | OMP bundled agents |
| Quality gates | Governance; static integrity/routing are enforced by validator/tests |
| Model selection | Native role aliases such as `@task`, `@slow`, `@plan` |
| MCP | Native capability, intentionally unconfigured |
| Slash commands/custom tools | Intentionally omitted |

## Model policy

Agent definitions reference stable roles; `.omp/config.yml` maps those roles to exact installed `openai-codex` selectors and thinking suffixes.

| Role | Selector | Purpose |
|---|---|---|
| `default` | `openai-codex/gpt-6-luna:medium` | Routine main session |
| `smol` | `openai-codex/gpt-6-luna:low` | Small, bounded tasks |
| `slow`, `plan` | `openai-codex/gpt-6.1-terra:high` | On-demand deep reasoning and architecture |
| `task` | `openai-codex/gpt-6-luna:medium` | Bundled implementation subagents and `test-engineer` |
| `advisor` | `openai-codex/gpt-6.1-terra:high` | On-demand high-risk independent advice |
| `judge`, `commit` | `openai-codex/gpt-6-luna:medium` | Short correctness-sensitive work |
| `memory`, `tiny` | `openai-codex/gpt-6-luna:low` | Frequent lightweight side tasks |

This is the budget-aware default. Frequent main, implementation, judgment, commit, memory, and tiny work uses GPT-6 Luna, the cheapest installed model at 0.1 input / 0.5 output catalog rates. GPT-6.1 Terra is loaded only through explicit `slow`, `plan`, or `advisor` roles, providing 500K context at half GPT-6.1 Sol's rate. Sol is intentionally unused. The installed catalog provides no quality score, so price is not treated as proof of capability. If a selector is unavailable in another installation, revalidate the mapping rather than assuming an equivalent fallback. Never put credentials in this file.

## Structure

```text
AGENTS.md                         authoritative governance
CONTEXT.md                        template boundaries and terminology
implementation-notes.md           consequential decisions and limitations
.omp/
  config.yml                      verified project model-role mapping
  agents/                         four focused project specialists
  extensions/prompt-router.ts     single deterministic router
  skills/                         seven discoverable skills plus references
docs/
  research.md                     sources, versions, verified capabilities, gaps
  validation-report.md            executed evidence, reviews, failures, limitations
  architecture/overview.md        runtime architecture and failure behavior
  adr/                            routing and agent-role decisions
  runbooks/incident-response.md   authorization-safe incident procedure
scripts/apply_template.py         safe three-path project installer
scripts/validate_template.py      static validator
scripts/test_runtime_router.py    installed-OMP TypeScript runtime harness
tests/scenarios.json              twenty acceptance scenarios
tests/test_prompt_router.py       Python-oracle routing tests
tests/test_apply_template.py      installer boundary and overwrite tests
tests/runtime-router-check.ts     actual classifier and handler transition tests
```

## Validation

```bash
python3 scripts/validate_template.py
python3 -m unittest tests.test_apply_template tests.test_prompt_router -v
python3 scripts/test_runtime_router.py
omp config list --scope project --json
```

Static validation proves file contracts, the canonical model-role policy, and deterministic selection through a dependency-free Python oracle over the shared JSON. Installer tests prove the exact three-path copy boundary, refusal-before-write behavior, explicit replacement, and dry-run behavior. `omp config list --scope project --json` proves that the installed runtime accepted the YAML layer; `omp models --json` proves selector availability. The router harness uses OMP's embedded Bun in headless RPC mode to execute the actual TypeScript classifier and handler transitions without a model request. These checks do not prove model compliance. For end-to-end activation evidence, run a no-write OMP prompt smoke and observe a `read skill://...` call; file existence or route selection alone is not activation.

## Agents and orchestration

Use direct execution for small work. For consequential work, the main session remains integration owner and may dispatch:

- `architect`: capability-read-only design and tradeoffs;
- `test-engineer`: behavior, property, concurrency, and failure tests;
- `sre`: capability-read-only production readiness or incident assessment;
- `smart-contract-auditor`: capability-read-only static contract/DeFi exploitability review;
- bundled `scout`, `reviewer`, `security-reviewer`, or `task` for exploration, review, security, and scoped implementation.

Parallel readers may share a working tree. Writers in one working tree are serialized; justified parallel writers require isolated worktrees and one integration owner.

## Security and limitations

- Project extensions are security-sensitive executable code; validators and tests also execute with user authority. Agent files and skills are repository-controlled instructions/data. Review all of them before use, and do not run repository-local executable code from an untrusted checkout outside a sandbox.
- The router performs no file, network, process, credential, model, or tool operations. It selects skill names only.
- No Markdown gate is described as runtime enforcement. OMP approvals remain the authority for tool execution.
- No production, deployment, transaction-signing, fund movement, or destructive action is authorized by this template.
- Current OMP `main` contains changes newer than the installed target. `docs/research.md` records the discrepancy; update only after source and runtime smoke validation.

## Maintenance

When adding a skill, first prove a distinct trigger, decision value, non-duplication, discoverability, and evaluation case. Keep skill directories one level under `.omp/skills`, add representative positive/collision/negative scenarios, run the validation commands above, and perform an OMP activation smoke when delivery risk warrants it.
