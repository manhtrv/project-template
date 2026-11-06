---
name: engineering-core
description: Evidence-first engineering workflow for small changes, bugs, features, reviews, tests, dependencies, and completion. Use whenever code or configuration is changed, debugged, reviewed, or verified; scales from direct mechanical edits to consequential multi-step work.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Engineering core

Apply the smallest workflow that can prove the requested outcome.

## Route by task shape

- **Mechanical/local:** inspect the exact context, edit directly, run one focused behavioral check. No plan or subagent.
- **Bug:** reproduce the reported symptom, trace the bad state to its source, make one minimal fix, retain a regression test when it catches a plausible recurrence, rerun the original symptom.
- **Feature:** derive observable acceptance criteria from the request and existing contracts, implement a vertical slice, smoke the real path, then run focused checks.
- **Review:** identify the intended diff/spec, trace cross-boundary consumers, and report only actionable introduced defects with exact locations.
- **Dependency/API uncertainty:** inspect the installed version and primary source before coding. Do not infer an API from another runtime.
- **Performance/concurrency:** load `skill://backend-concurrency-performance` and measure or reproduce before changing behavior.

## Procedure

1. **Establish the truth boundary.** List the goal, known facts, consequential assumptions, and the command or observation that would prove success. Resolve repository-answerable questions with tools.
2. **Build feedback.** For a defect, create the tightest red-capable reproduction. For a feature, identify the real executable path. Keep it deterministic and scoped.
3. **Trace before fixing.** Follow input/state from symptom to origin. Compare a nearby working pattern. State one falsifiable root-cause hypothesis and test it with the smallest probe.
4. **Choose the smallest complete change.** Preserve contracts unless change is requested. Migrate every affected caller; remove code made obsolete by the clean cutover. Avoid unrelated cleanup.
5. **Test behavior.** Test through public seams and independent expectations. Cover boundaries, state transitions, errors, and invariants that can fail for consumers.
6. **Smoke the changed surface.** Run the command, API path, UI flow, job, or throwaway harness that exercises the new behavior. A test suite alone is not the smoke proof.
7. **Review proportionately.** Use independent review for security, funds, production, concurrency, protocol, migration, or broad cross-module risk.
8. **Report evidence.** State changed behavior, rationale, commands run, outcomes, and unresolved risk. Never promote an inference to a fact.

Read `skill://engineering-core/references/debugging-and-verification.md` for difficult diagnosis or completion claims. Read `skill://engineering-core/references/testing-and-review.md` when adding tests or reviewing a diff.

## Stop conditions

Ask one targeted question only if unresolved ambiguity can materially change behavior and cannot be answered from code, docs, history, or runtime evidence. Ask for authorization before irreversible, credential-sensitive, production-impacting, or financially consequential actions.
