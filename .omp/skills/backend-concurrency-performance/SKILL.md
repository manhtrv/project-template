---
name: backend-concurrency-performance
description: Backend reliability for TypeScript/Node/Bun, Rust, APIs, PostgreSQL, Redis, queues, concurrency, synchronization, idempotency, performance profiling, capacity, and regression prevention. Use for races, deadlocks, duplicate work, slow APIs, database contention, distributed jobs, or backend architecture changes.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Backend concurrency and performance

## Concurrency diagnosis

1. Build a deterministic interleaving harness using barriers, latches, controlled clocks, or a repeated stress loop. Arbitrary sleeps alone are weak evidence.
2. Identify shared mutable state, ownership, atomicity boundary, ordering, cancellation, and retry semantics.
3. Draw the interleaving that violates the invariant. Distinguish an in-process race, database isolation anomaly, distributed duplicate, stale cache, and queue redelivery.
4. Fix at the narrowest correct boundary: transaction/constraint, compare-and-swap, idempotency record, single-flight, ownership transfer, or explicit synchronization.
5. Test the bad interleaving and a normal path. Verify no lock-order inversion, starvation, leaked work, or unbounded queue.

## Performance diagnosis

1. Define the consumer-visible metric and workload. Capture baseline distribution, data size, concurrency, environment, and warm/cold state.
2. Profile before optimizing. Use traces, flamegraphs, query plans, allocation profiles, or counters that locate cost.
3. Separate CPU, allocation/GC, lock wait, I/O, database, network, and downstream time.
4. Change one bottleneck. Avoid cache/batch/concurrency changes unless their invalidation, ordering, memory, and backpressure semantics are explicit.
5. Repeat the comparable measurement and check correctness under load.

Read `skill://backend-concurrency-performance/references/concurrency-and-performance.md` for test and profiling patterns. Read `skill://backend-concurrency-performance/references/data-and-jobs.md` for PostgreSQL, Redis, API, and job-processing rules.

## Durable effects

Assume at-least-once execution. Couple state change and idempotency marker atomically where possible; otherwise use a transactional outbox/inbox or reconciler. A distributed lock is a lease, not proof of sole ownership after pauses or partitions; use fencing when stale holders can write.
