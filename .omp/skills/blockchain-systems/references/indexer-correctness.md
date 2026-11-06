# Reorg-safe indexer procedure

## Data model

Persist at minimum:

- chain/network identity;
- block number/slot, hash, parent hash, timestamp, and canonical status;
- transaction hash/signature plus block identity and status;
- log/event natural key: chain + block hash + transaction identity + log/instruction index;
- checkpoint number **and hash**;
- provenance/provider and observed/safe/finalized state where useful.

Derived rows must link to source block/event identities so orphaned effects can be reversed, invalidated, or recomputed.

## Advance algorithm

1. Read the local checkpoint `(height, hash)` and candidate remote head.
2. Fetch the block at checkpoint height from the chosen provider. If its hash differs, stop forward ingestion.
3. Walk local and remote ancestors backward with bounded RPC calls until a common ancestor is proven. If history is unavailable or bound exceeded, halt and require a configured recovery/backfill path.
4. In one transaction per safe batch:
   - mark/delete orphan source records and reverse/recompute dependent state in dependency order;
   - set checkpoint to the common ancestor;
   - insert canonical blocks/events with uniqueness constraints;
   - apply idempotent derived effects;
   - advance checkpoint to the last fully applied block hash.
5. Replay forward in parent-linked order. Never advance across a missing block/range.
6. Independently reconcile recent windows and finalized checkpoints to detect silent provider gaps.

If deletion destroys auditability or reversal inputs, mark canonicality instead and build queries/views that exclude orphan data.

## Provider discipline

- Pin range queries to explicit block numbers/hashes where the API permits; avoid mixing an unpinned “latest” across calls.
- Detect endpoint disagreement by hash, not height alone.
- Cap log ranges and adapt to provider limits without skipping a range. Persist the inclusive/exclusive boundaries.
- Failover starts from the last verified checkpoint. A new provider must agree on the ancestor before its events are accepted.
- Distinguish transport errors, rate limits, pruned/archive gaps, malformed responses, and chain disagreement.

## Finality

Use the chain's native finalized/safe semantics when available. Otherwise configure confirmations from threat/risk requirements and monitor deeper reorgs. Separate ingestion latency from finalization latency. Never label an effect final merely because a worker processed it once.

## Verification

- synthetic short and deep reorgs;
- duplicate ranges and worker restarts at every persistence boundary;
- missing middle range and provider response truncation;
- two providers disagreeing at the same height;
- backfill overlapping live ingestion;
- invariant/count reconciliation against chain over sampled windows;
- lag, checkpoint age, reorg depth, duplicate suppression, gap, RPC error, and replay metrics.
