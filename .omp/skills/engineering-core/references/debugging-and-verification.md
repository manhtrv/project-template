# Debugging and verification

## Tight feedback loop

A useful loop drives the real failing path and detects the exact symptom. Preferred order: focused existing test; API/CLI invocation; browser flow; captured request/event replay; throwaway harness; property/stress loop; old/new differential; automated bisection.

Record the command and redacted result. Tighten it until setup is minimal, outcome deterministic, and runtime short enough for repeated hypotheses. For a flake, increase the controlled reproduction rate with repeated runs, barriers, load, or fault injection; do not claim absence after one pass.

## Root-cause trace

1. Locate the first externally wrong observation.
2. Identify the value/state that made it wrong.
3. Walk callers, writes, messages, and persistence boundaries backward.
4. At every boundary record input, output, identity, ordering, version/config, and error handling.
5. Find the earliest divergence from an invariant or known-good path.
6. Form a falsifiable hypothesis: “If X is the cause, probe Y changes while Z remains stable.”
7. Change one variable or add one targeted observation. Remove temporary instrumentation after proof.

Retries, catches, default values, relaxed assertions, and increased timeouts are not root-cause fixes unless the external failure is the proven cause and the handling contract explicitly requires them.

## Red-green proof

For a retained regression test:

1. Run it against the failing behavior and observe the expected failure.
2. Apply the minimal fix and observe a pass.
3. When practical, temporarily remove/revert only the fix and confirm the test fails for the intended reason; restore and pass again.
4. Rerun the original, less-minimized symptom.

Do not preserve a test that asserts implementation text, forwarding, mock echoes, incidental defaults, or bare non-throwing behavior.

## Completion evidence

Map each claim to fresh evidence:

| Claim | Required observation |
|---|---|
| Bug fixed | Original symptom no longer reproduces and regression check passes |
| Build works | Actual build exits successfully |
| API works | Real request exercises serialization, handler, dependency boundary, and response |
| Migration safe | Mixed-version/cutover/rollback scenario or dry run proves the path |
| Performance improved | Comparable before/after distributions with workload and environment stated |
| Concurrency safe | Bad interleaving is controlled or stress run has an explicit detection oracle |
| Agent/tool ran | Runtime trace/output identifies the actual execution |

If the proving environment is unavailable, finish all local work and report the exact unverified boundary. Never describe a hypothetical check as passed.
