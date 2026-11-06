# Concurrency and performance procedure

## Interleaving tests

Replace timing guesses with controlled points:

1. Arrange two operations at the same precondition.
2. Block each at the boundary before the contested read/write/effect.
3. Release in the failing order.
4. Assert the externally visible invariant and durable state.
5. Repeat with cancellation/error at each boundary.

For distributed workers, include lease expiry, redelivery, process crash after effect but before acknowledgment, and stale owner writes. For databases, test at the actual isolation level and with real constraints; an in-memory fake cannot reproduce lock/isolation semantics.

## Synchronization choices

- Database uniqueness/check constraint: reject impossible durable states.
- Transaction with row/advisory lock: serialize a small durable critical section; define lock order and timeout.
- Compare-and-swap/version: detect conflict and retry the whole decision from fresh state.
- Single-flight: coalesce identical in-process work; it does not coordinate processes.
- Queue partition/actor: single owner per key; handle rebalance and poison work.
- Lease + fencing: coordinate distributed ownership where stale holders can reach the resource.

Document fairness, cancellation, maximum wait, lock order, crash behavior, and backpressure.

## Performance measurement

Capture median and tail (p95/p99), throughput, errors, saturation, allocations/GC, and dependency spans. Warm-up and sample count must be comparable. Pin dataset, concurrency, machine/container limits, build mode, and dependency versions.

Use the tool that isolates the cost: CPU/allocation profile, async trace, database `EXPLAIN (ANALYZE, BUFFERS)`, lock-wait view, network trace, or load test. Optimize the measured bottleneck, then rerun correctness checks under representative load.

## Common traps

- increasing concurrency while moving the bottleneck downstream;
- unbounded `Promise.all`, task spawn, channels, or queues;
- retry amplification and synchronized backoff;
- cache stampede or incorrect invalidation;
- N+1 calls hidden by low test data;
- benchmark dead-code elimination, debug builds, unrealistic warm cache, or different datasets;
- throughput improvement that worsens tail latency, errors, or memory beyond limits.
