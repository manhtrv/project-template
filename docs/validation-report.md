# Validation report

## Verdict

**Goal achieved for the verified OMP 18.16.0 target.** The repository contains a safe three-path installer, project-local governance, a validated `openai-codex` model-role mapping, seven focused skills, four differentiated project agents, one deterministic routing extension, domain procedures, a dependency-free validator, twenty routing scenarios, direct TypeScript runtime checks, and operator documentation. No global configuration, provider credential, MCP server, or custom tool was added.

## Executed evidence

| Check | Observed result |
|---|---|
| `python3 scripts/validate_template.py` | Passed: 7 skills, 4 project agents, 7 routed skill slots, 20 scenarios |
| `python3 -m unittest tests.test_prompt_router -v` | Passed: 5 tests |
| `python3 -m unittest tests.test_apply_template -v` | Passed: 4 installer boundary tests |
| installer CLI smoke in a temporary project | Copied exactly `.omp/`, `AGENTS.md`, and `CONTEXT.md`; preserved an unrelated file; OMP discovered 10 roles and 7 skills |
| `python3 -m py_compile scripts/apply_template.py scripts/validate_template.py scripts/test_runtime_router.py tests/test_apply_template.py tests/test_prompt_router.py` | Passed: exit 0, no diagnostics |
| `python3 scripts/test_runtime_router.py` | Passed under OMP's embedded Bun: 20 scenarios plus handler state/bypass transitions; headless RPC sent no model request |
| `omp config list --scope project --json` | Passed: installed OMP accepted all 10 project model-role selectors |
| `omp models --json` capability check | Passed: GPT-6 Luna and GPT-6.1 Terra are available and support every requested effort |
| default-role inference smoke | Returned exact `MODEL_OK` from `gpt-6-luna`; observed cost `0.0001903` |
| `@task` role inference smoke | Returned exact `TASK_ROLE_OK` from `gpt-6-luna`; observed cost `0.0001909` |
| controlled model-role drift smoke in a temporary copy | Passed: validator rejected an unapproved model selector |
| controlled symlink-preflight smoke in a temporary copy | Passed: validator exited 1 before content reads and reported the escaping template-owned symlink |
| `omp skill list --json` | Discovered all 7 skills with source `native:project` |
| project-agent roster smoke through OMP's advertised `task` schema | Returned `architect,smart-contract-auditor,sre,test-engineer` |
| routed activation smoke with only `read` enabled | Observed `read skill://agent-workflow-engineering` and final `ACTIVATION_OK` |

The direct runtime test proves exact route selection and extension state transitions. The activation smoke proves one native `skill://` read through the installed model/tool loop; it does not prove that a model will read every selected skill.

## Independent review

The first architecture audit found eight issues: cross-language runtime-test overclaim, duplicate-suppression state, shell-enabled read-only roles, backend over-routing, inconsistent trust wording, conflicting parallel-writer policy, unsupported forward-compatibility claims, and an implementation agent overlapping bundled `task`.

The first security audit found four issues: unsafe broad test discovery in a target repository, shell/network capability in read-only roles, post-use symlink/reference checks, and lack of direct TypeScript router execution.

After remediation, both independent agents re-reviewed the repository read-only. Each explicitly reported all prior findings resolved and no remaining material finding in scope.

## Failed checks and adaptations

- No standalone `bun`, `node`, or `deno` executable was available. Runtime tests now use OMP's embedded Bun through headless RPC; no package was added.
- OMP guards `process.exit()` during extension loading, so the first test-extension termination approach was rejected by the runtime. The final harness closes RPC stdin cleanly instead.
- `--max-cost=0` is invalid because OMP requires a positive amount. Headless RPC avoids a model request rather than relying on a cost sentinel.
- `omp agents unpack --project --dry-run` is unsupported in 18.16.0. Agent discovery was instead observed through OMP's actual task-tool roster.
- A low-cost activation attempt stopped after its first skill read. The repeated smoke completed with a higher cap, but the model still chose to read only one selected skill; this is a model-compliance limitation, not a classifier failure.

## Residual limitations

- Compatibility is verified only for OMP 18.16.0. Newer versions require source review plus validator, runtime, discovery, and activation smokes.
- Routing selection is deterministic; skill activation and compliance remain model-mediated.
- Contextual quality gates, review requirements, and writer isolation are governance unless OMP approvals or repository automation enforce them.
- Capability-read-only specialists intentionally cannot run shell commands, network research, live production queries, or contract tooling. The authorized parent must run justified commands in an appropriately isolated environment and pass sanitized evidence.
- Model-role selectors are project-owned and verified against the current catalog; provider authentication remains operator-owned. The budget-aware policy uses Luna for every frequent role and Terra only for explicit deep reasoning, planning, and advice. Sol is intentionally unused. Another installation must revalidate availability and price before using or changing the mapping.
- MCP is supported by OMP but intentionally unconfigured because this template has no concrete server requirement or credential boundary to validate.
