---
name: architecture-systems
description: Implementable architecture and distributed-systems decisions covering boundaries, contracts, state, consistency, concurrency, capacity, failure modes, migrations, and security. Use for system design, event-driven services, multi-region or multi-chain systems, major interfaces, and high-impact migrations.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Architecture and distributed systems

Produce the smallest design that makes correctness and operations explicit.

## Workflow

1. **Frame the decision.** Define actors, use cases, non-goals, load/latency/availability targets, trust boundaries, data sensitivity, and constraints already fixed by the repository or request.
2. **Model state and ownership.** Name the authoritative owner of each fact, identifiers, invariants, lifecycle states, retention, and recovery source. Avoid shared ownership without a conflict rule.
3. **Draw contracts.** Specify request/event schemas, ordering, idempotency, timeouts, errors, versioning, compatibility, and cancellation. State which guarantees are end-to-end versus transport-local.
4. **Compare viable options.** Include the boring baseline. Evaluate correctness, coupling, operational burden, migration, cost, and reversibility. Reject options that require guarantees the platform cannot provide.
5. **Analyze failure.** Cover partitions, retries, duplicate/out-of-order/lost messages, stale reads, overload, partial deploys, dependency degradation, clock skew, and operator error.
6. **Size the system.** Show assumptions and simple arithmetic for peak throughput, storage growth, connection/concurrency limits, and headroom. Mark unknown inputs rather than inventing precision.
7. **Design evolution.** Define compatibility window, backfill/dual-read/dual-write only when necessary, cutover criteria, observability, rollback, and data reconciliation.
8. **Make it implementable.** Produce module boundaries, interfaces, state transitions, acceptance tests, and rollout checkpoints. Do not end at a conceptual diagram.

Read `skill://architecture-systems/references/distributed-systems.md` before deciding delivery, consistency, coordination, or capacity semantics.

## Decision quality

Prefer cohesive modules with small interfaces. Add a boundary only when ownership, lifecycle, scaling, trust, or independent change requires it. A service per noun is not architecture. “Exactly once” must resolve to idempotent effects or a proven atomic boundary; transport delivery alone is insufficient.
