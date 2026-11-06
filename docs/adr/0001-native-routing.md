# ADR 0001: Native discovery with one deterministic router

- Status: Accepted
- Compatibility target: OMP 18.16.0

## Context

OMP natively discovers repository skills and exposes their names/descriptions to the model, but does not provide a deterministic natural-language rule table. Pure AGENTS.md routing would be advisory and difficult to test. Injecting full skill bodies would defeat progressive disclosure.

## Decision

Use `.omp/extensions/prompt-router.ts` with the verified `before_agent_start` event. It classifies only main-session prompt text and injects ordered skill names. The model then reads native `skill://` resources. Export the pure classifier and exercise both it and the stateful handler through an explicit test extension loaded by the installed OMP runtime.

## Consequences

- One routing authority; no slash command or second semantic router.
- Deterministic selection is tested without a model request: the Python oracle checks shared-rule scenarios, and the OMP headless-RPC harness executes the runtime TypeScript classifier and handler transitions.
- Skill execution remains model-mediated, not a hard runtime gate.
- Extension loading is security-sensitive code execution; the implementation is dependency-free, has no filesystem/network/process access, and is covered by static validation, direct runtime checks, and an end-to-end activation smoke. The Python oracle does not claim JavaScript-regex or handler equivalence.
