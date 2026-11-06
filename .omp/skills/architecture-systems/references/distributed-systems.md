# Distributed-systems decision reference

## Delivery and effects

- Assume messages can be duplicated, delayed, reordered, and lost unless a proven protocol states otherwise.
- “At least once” requires idempotent consumers. “At most once” permits loss. Broker “exactly once” rarely covers database or external effects.
- Give every command/event a stable identity and schema version. Deduplicate at the effect boundary for at least the maximum replay horizon.
- Use an outbox to atomically couple state and publication; use an inbox/idempotency row to couple receipt and effects. Reconciliation is still required for external systems.

## Ordering and coordination

Define the ordering scope: global, aggregate/key, partition, or none. A partition key is a correctness choice. If multiple writers update one invariant, choose one:

- single owner/leader;
- database transaction and constraint;
- compare-and-swap/version check;
- commutative/mergeable data type;
- explicit conflict resolution.

Distributed locks are expiring leases. If a stale holder can write after expiry, include a monotonic fencing token checked by the resource.

## Consistency

State which operations require linearizable, serializable, snapshot, causal, read-your-writes, monotonic, bounded-staleness, or eventual behavior. Match the datastore transaction/isolation semantics; names such as “repeatable read” vary by system.

For caches, define source of truth, invalidation owner, maximum stale age, stampede control, negative caching, and behavior when cache and source disagree.

## Failure-mode table

For every dependency/path, answer:

| Failure | Detection | Bounded response | Recovery/reconciliation |
|---|---|---|---|
| timeout/unknown outcome | deadline and request identity | do not assume failure | query/reconcile before retrying effect |
| duplicate | idempotency identity | return prior result | compact keys after replay horizon |
| out of order | version/sequence | buffer, reject, or recompute | replay from durable source |
| partition | health and quorum evidence | degrade or reject unsafe writes | reconcile divergent state |
| overload | queue depth/latency/saturation | backpressure, shed, rate-limit | drain with fairness and caps |
| partial deploy | version telemetry | compatible contracts | roll forward/back within window |

## Capacity arithmetic

Show units and peak factors:

- requests/s × work/request = work/s;
- event rate × retained bytes × retention = storage;
- arrival rate × mean service time = average concurrency (Little's Law);
- replicas = peak work / safe per-replica capacity, then add failure and deployment headroom.

Measure safe capacity under representative data and dependency latency. Autoscaling cannot repair an unbounded queue, shared bottleneck, or downstream quota.

## Migration

Prefer expand → deploy compatible readers/writers → backfill with checkpoints → verify counts/invariants → cut over → observe → contract. Make rollback compatible with every state written during the window. Dual writes need an authority and reconciliation; they are not automatically atomic.
