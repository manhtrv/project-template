# Project Context

## Purpose

This repository is a repository-local Principal Engineering template for Oh My Pi (OMP). It supplies governance, prompt routing, focused skills, specialist agent definitions, validation, and representative routing scenarios without modifying global OMP state.

## Runtime boundary

- Compatibility authority: installed OMP `18.16.0` and source tag `v18.16.0`.
- Native project surfaces used: root `AGENTS.md`, `.omp/skills/*/SKILL.md`, `.omp/agents/*.md`, and `.omp/extensions/*.ts`.
- No global profile, credentials, provider catalog, MCP server, or model assignment is owned by this repository.
- The prompt router selects skill names; native OMP `skill://` resolution loads their content progressively.

## Components

- `AGENTS.md`: always-on governance and adaptive execution policy.
- `.omp/extensions/prompt-router.ts`: deterministic top-level prompt classifier.
- `.omp/skills/`: domain procedures and on-demand references.
- `.omp/agents/`: project specialists that complement, rather than replace, OMP's bundled agents.
- `scripts/validate_template.py`: standard-library structure, metadata, reference, safety, and scenario validator.
- `tests/`: executable routing behavior and scenario contracts.
- `docs/`: research, architecture decisions, and operational guidance.

## Invariants

1. Project-local files must be sufficient; global OMP configuration is optional and never mutated by installation.
2. Skill directories are one level below `.omp/skills` and names match Agent Skills constraints.
3. The router never executes tools or loads credentials. It injects routing metadata only for the main session.
4. Skills are original, concise procedures. External repositories are research inputs, not vendored dependencies.
5. Model routing uses OMP role aliases in agent definitions. Concrete provider/model selection remains operator-owned.
6. Runtime enforcement claims must name the implementing code. Markdown-only rules are identified as governance.
7. A simple task remains direct: no mandatory plan, design document, worktree, or agent hierarchy.

## Terminology

- **Route:** ordered set of skill names selected from a natural-language prompt.
- **Skill activation:** reading a selected `skill://<name>` body, explicitly or through an agent's `autoloadSkills`.
- **Gate:** a proportional quality question; enforced only when code or an approval mechanism implements it.
- **Independent review:** review performed by a separate agent/context, not the implementer's self-review.
- **Production-impacting:** capable of changing live availability, data, permissions, funds, or shared infrastructure.
