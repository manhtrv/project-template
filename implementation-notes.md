# Implementation notes

## Assumptions

- Installed OMP 18.16.0 is the compatibility authority even when current `main` has newer APIs.
- This repository is the template product; `CONTEXT.md` therefore describes the template itself rather than an unspecified downstream application.

## Decisions

- Commit `.omp/config.yml` because this installation's exact `openai-codex` catalog is now an explicit project requirement. Keep credentials operator-owned and validate selectors through OMP 18.16.0.
- Omit `.omp/mcp.json`, custom tools, and commands: no capability requires them; adding them would increase trust and maintenance surface.
- Use one extension because native discovery does not offer deterministic prompt classification. Keep it pure and top-level-only.
- Reuse bundled OMP agents, including `task` for implementation, instead of copying or shadowing their definitions; add only four differentiated project specialists.
- Merge broad topic lists into seven decision-oriented skills with progressive references.
- Apply the runtime template with `scripts/apply_template.py`, copying only `.omp/`, `AGENTS.md`, and `CONTEXT.md`. Refuse conflicts by default; require explicit `--replace` for those selected paths.

## Deviations from candidate structure

- No empty `commands/` or custom-tool directory.
- No custom `reviewer`, `security-auditor`, or `researcher`; bundled `reviewer`, `security-reviewer`, and `scout` already provide those contracts.
- The installed OMP binary embeds Bun but no standalone Bun executable is available. The validator and oracle tests use Python's standard library; `scripts/test_runtime_router.py` uses OMP's headless RPC mode to execute the actual TypeScript classifier and handler without a model request.

## Tradeoffs

- Deterministic routing selects skills but cannot force a model to follow them. Actual activation is evidenced by `read skill://...` calls, not by classifier output alone.
- Role aliases keep agent definitions decoupled from provider IDs, while the project mapping intentionally trades cross-installation portability for reproducible local selection. Luna handles every frequent role; Terra is retained only for explicit deep reasoning, planning, and advice because it provides 500K context at half Sol's catalog rate. Sol is not used. Catalog price is a cost signal, not a quality proof.
- Governance gates remain instructions unless the validator or OMP approval system explicitly enforces them.

## Verification

- Static validator: 7 skills, 4 project agents, 7 routed skill slots, and 20 scenarios passed.
- Project config: OMP accepted all ten role selectors. GPT-6 Luna and GPT-6.1 Terra support every requested effort. Default and `@task` smokes both resolved to GPT-6 Luna and returned the required exact response.
- Installer: 4 behavioral tests passed. A CLI smoke copied exactly the three selected paths into a temporary project, preserved an unrelated file, and OMP discovered 10 model roles and 7 project skills there.
- Python oracle: 5 tests passed; Python compilation completed without diagnostics.
- Installed OMP runtime: direct TypeScript classifier/handler checks passed in headless RPC mode without a model request; native discovery found 7 project skills and 4 project agents.
- Safety smoke: a temporary escaping symlink was rejected before content reads.
- End-to-end activation: the installed model read one selected `skill://` resource and returned `ACTIVATION_OK`; reading every selected skill remains model-mediated.
- Independent architecture and security rechecks reported all prior findings resolved. Full command evidence and limitations are in `docs/validation-report.md`.
