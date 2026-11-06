# APIs, PostgreSQL, Redis, and jobs

## API reliability

Define request identity, authentication/authorization, validation owner, idempotency semantics, deadline/cancellation propagation, pagination consistency, error taxonomy, rate limits, and compatibility/versioning. Bound payloads and fan-out. Do not return success before required durable effects are committed.

## PostgreSQL

- Put invariants in constraints where expressible.
- Know the actual isolation level and anomaly it permits; use serializable or explicit locking only for the invariant that needs it.
- Keep transactions short and free of remote calls.
- Establish lock order and inspect query plans with production-like cardinality.
- Migrate via expand/backfill/cutover/contract; use resumable keyed batches and verify counts/checksums/invariants.
- Connection pools are finite queues. Set acquisition/query/statement timeouts and reserve operational capacity.

## Redis

Treat Redis as authoritative only when persistence/replication/failover semantics meet the data-loss contract. Otherwise design cache loss and stale data as normal.

- Use atomic scripts/transactions for multi-key invariants only with explicit cluster slot constraints.
- Set TTL, eviction, stampede, serialization version, and invalidation behavior.
- Pub/Sub is ephemeral; use streams/queues or durable source when loss matters.
- Distributed locks require unique ownership tokens, bounded lease assumptions, safe unlock, and fencing for stale writers.

## Job processing

- Stable job ID and payload schema version.
- At-least-once-safe handler with atomic idempotency/effect boundary.
- Retry only classified transient failures; cap attempts and total age with jitter.
- Visibility/lease exceeds normal processing or is renewed safely.
- Dead-letter/poison handling preserves evidence and supports reviewed replay.
- Backpressure, per-key ordering, fairness, shutdown drain, and cancellation are explicit.
- Metrics: age, lag, depth, attempt distribution, success/error class, duration, lease loss, duplicates, dead letters.

A queue acknowledgment after a non-atomic external effect leaves an unknown-outcome window. Close it with provider idempotency keys, intent records, and reconciliation.
