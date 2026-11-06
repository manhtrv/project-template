# Testing and independent review

## Test selection

Test the narrowest public seam that includes the real failure mode. A seam includes observable results, errors, state transitions, and externally relevant side effects—not private call order.

Permanent tests should catch a plausible consumer-visible regression:

- boundary values and malformed/partial input;
- lifecycle transitions and illegal transitions;
- retry/idempotency and duplicate delivery;
- cancellation, timeout, and partial failure;
- ordering and concurrency invariants;
- compatibility and migration states;
- authorization and trust boundaries;
- financial conservation and rounding.

Prefer worked literals, protocol specs, independent models, and property invariants as expected values. Avoid deriving expected output with the same algorithm under test.

## Review procedure

1. Establish the intended change: request/spec, base revision, and actual diff.
2. Read changed code in surrounding context.
3. Trace every new or changed value crossing a module/process/protocol boundary to its consumer dispatch point.
4. Check behavior, security, data integrity, concurrency, errors, compatibility, and operability before style.
5. Confirm tests can fail for the defect they claim to cover and do not lock implementation details.
6. Report only introduced, actionable defects with a reachable trigger and impact. Do not invent findings to fill a quota.
7. Separate spec compliance from engineering quality when both are relevant.

Finding format:

- severity/priority and confidence;
- exact file and minimal line range;
- trigger/preconditions;
- incorrect behavior and consumer impact;
- evidence and a concrete correction direction.

A clean review states scope and reviewed paths. It does not imply unreviewed systems are safe.

## Dependency investigation

Before changing an external API:

- identify the installed version/lockfile and runtime;
- inspect local types/source and official versioned documentation;
- search all affected call sites with language-aware references when available;
- check error, cancellation, concurrency, and resource ownership contracts;
- use a small executable probe when documentation and runtime behavior differ.

Pinning or upgrading a dependency is a behavior change. Review changelog, transitive/security impact, build artifacts, and rollback path proportionately.
