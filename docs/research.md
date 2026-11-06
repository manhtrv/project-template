# Research findings and gap assessment

## Authority and revisions

Research performed against the installed runtime and checked-out implementations, not README claims alone.

| Source | Revision inspected | License note | Relevant evidence |
|---|---|---|---|
| [Oh My Pi](https://github.com/can1357/oh-my-pi) | installed `18.16.0`, tag commit `650f3a108229ee11bf68ba3377f4e8c3391cd424`; latest `main` docs also compared | repository license applies | `docs/skills.md`, `config-usage.md`, `task-agent-discovery.md`, `extensions.md`, `hooks.md`, `models.md`, `mcp-config.md`, `session.md`, and corresponding TypeScript source |
| [Agent Skills](https://agentskills.io/specification) / [source](https://github.com/agentskills/agentskills) | `83021e2be457a9b6679148719c1f6074f0ad975e` | Apache-2.0 | specification and `skills-ref` parser/validator |
| [Matt Pocock skills](https://github.com/mattpocock/skills) | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT | debugging, TDD, codebase design, domain modeling, review, implementation workflows |
| [Superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | MIT | systematic debugging, verification, planning, parallel delegation, subagent development |
| [Anthropic skills](https://github.com/anthropics/skills) | `ca45fc496a3436251f191354091d557da31c15b5` | per-skill; inspected `skill-creator` is Apache-2.0 | progressive disclosure, description-driven activation, skill evaluation |

No external skill body is copied into this template. Adopted concepts are small original procedures: tight feedback loops, behavior-first tests, explicit verification, progressive disclosure, and independent review. Rejected concepts include compulsory brainstorming/design approval for every feature, mandatory worktrees, one subagent per plan step, and unconditional dual reviews; those conflict with proportional execution and cost control.

## Verified native OMP capabilities

- **Context:** root/ancestor `AGENTS.md` files are discovered separately from `.omp/AGENTS.md`. The root file is sufficient here.
- **Skills:** native project skills are discovered at `<ancestor>/.omp/skills/*/SKILL.md`; scanning is non-recursive at the skill-directory level. `name` and `description` are required for native `.omp` skills. The runtime exposes metadata in the system prompt and content through `skill://` when an active reader advertises skill URI support.
- **Activation:** OMP exposes skill metadata for model selection; `globs` and `alwaysApply` are metadata, not invocation controls. `/skill:` is optional manual invocation. There is no native deterministic prompt-to-skill rule table.
- **Agents:** project agents are discovered from nearest `.omp/agents/*.md`; project definitions override user, extension, and bundled names. Supported fields include `tools`, `spawns`, ordered `model`, `thinkingLevel`, `output`, `structured`, `autoloadSkills`, `prewalk`, and `advisor`.
- **Subagents:** the `task` tool supports batched parallel dispatch, `solutionSpace`, depth/spawn restrictions, structured output, live rediscovery, and optional isolation. The parent must prevent shared-write conflicts.
- **Models:** model roles live under `modelRoles` in `config.yml`; agent frontmatter can use `@task`, `@slow`, `@plan`, and other role aliases. Concrete availability depends on operator credentials and catalog state.
- **Installed catalog:** the inspected runtime exposed eight available OpenAI Codex chat models: GPT-5.6 Luna/Sol/Terra, GPT-6 Astra/Luna/Sol, and GPT-6.1 Sol/Terra. No model named “GPT-6 Medium” exists, so this template does not invent that identifier or pin provider-specific models.
- **Extensions:** project `.omp/extensions` auto-discovers `.ts`/`.js` modules. A default factory receives `ExtensionAPI`; `before_agent_start` exposes transformed prompt text and can inject a custom message. Extension factories are rebound for subagents and `ctx.agent.kind` distinguishes main from subagent sessions.
- **Hooks:** new integrations should use the extension runner. Native hook factories must be under `.omp/hooks/pre` or `post`; `tool_call` can block or replace validated input and fails closed on handler exceptions in the documented wrapper path.
- **Custom tools:** executable `.ts`/`.js` factory modules are supported under `.omp/tools`; declarative Markdown/JSON is metadata only. No custom tool is needed by this template.
- **MCP:** `.omp/mcp.json` is native project configuration. Servers can execute local commands or receive credentials, so no server is configured without a concrete project requirement. MCP instructions can be disabled per server.
- **Sessions:** JSONL sessions persist under the active profile's agent directory, with tree entries, compaction records, blob externalization, and subagent lineage. This repository does not depend on a global session path.
- **Configuration precedence:** environment/runtime overrides exceed CLI overlays, project settings, global settings, and defaults. Project arrays replace rather than merge lower arrays. Unknown/invalid settings may be ignored or fail depending on layer; therefore this template omits redundant settings.

## Version discrepancy

The installed tag is the compatibility authority. Fetching current `main` showed later changes in `docs/extensions.md`, `models.md`, `skills.md`, and `task-agent-discovery.md` (229 added and 11 removed lines across the inspected documents). The implementation uses only contracts verified in tag `v18.16.0`; it does not rely on post-tag additions.

## Gaps and decisions

| Requirement | Native support | Decision |
|---|---|---|
| Natural-language skill discovery | Metadata and semantic model selection | Use native catalog and progressive `skill://` reads |
| Deterministic prompt routing | No native rule table | One minimal `before_agent_start` extension selects skill names and injects routing metadata |
| Runtime quality-gate enforcement | Tool approval and hooks exist, but generic engineering gates need task context | Keep contextual gates as governance; enforce static integrity in the validator and router behavior through direct OMP-runtime tests |
| Specialized agents | Native project agent files and bundled specialists | Add only architect, test engineer, SRE, and contract auditor roles; reuse bundled scout/reviewer/security-reviewer/task, including `task` for implementation |
| Model optimization | Native role selectors with optional thinking suffixes; concrete availability varies | Keep agents on role aliases and commit an OMP-validated `openai-codex` role mapping for this installed catalog; credentials remain operator-owned |
| MCP capability discovery | Native | Do not configure an MCP server; the authorized main session inspects available tools at runtime |
| Slash commands | Native `.omp/commands` | Omit: prompt-first operation makes commands redundant |
| Project config | Native `.omp/config.yml`; unknown settings are rejected by the installed settings registry | Include only `modelRoles`, validate the canonical mapping statically, then prove runtime loading and catalog availability through OMP |

## Minimum supported architecture

One governance file, one project model-role mapping, one routing extension, seven skills with on-demand references, four differentiated custom agents, one validator, and scenario-driven Python-oracle plus direct OMP-runtime routing tests. No custom tool, MCP server, command, marketplace package, global config, standalone Bun, or external package dependency is required.
