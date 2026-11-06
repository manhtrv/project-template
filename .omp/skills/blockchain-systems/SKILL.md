---
name: blockchain-systems
description: Blockchain data and execution engineering for reorg-safe indexers, canonical reconciliation, finality, RPC reliability, checkpoints, backfills, transaction lifecycle, simulation, provider failover, and cross-chain messaging. Use for chain indexers, RPC services, wallets, relayers, bridges, and transaction systems.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Blockchain systems

Treat chain data as a forkable external log, not an immutable ordered database.

## Start with chain semantics

Record chain, client/provider behavior, block identifiers, finality mechanism, safe/finalized tags if available, maximum expected reorg, archive requirements, log limits, and contract upgrade/proxy behavior. Verify these against primary documentation or the running node.

## Indexer path

1. Define the canonical identity of blocks, transactions, logs/events, and derived records.
2. Persist checkpoint height **and block hash** in the same consistency boundary as effects, or make effects replay-safe.
3. Before advancing, verify the stored checkpoint remains an ancestor of the provider's current chain.
4. On mismatch, locate a common ancestor, reverse or invalidate orphan-derived effects in dependency order, then replay canonical blocks.
5. Make processing idempotent with chain-scoped natural keys. Detect duplicates and gaps explicitly.
6. Separate observed, safe, and finalized states where the chain supports them. Business effects choose the required state; one confirmation count does not fit every risk.
7. Reconcile multiple RPC responses by block hash and provenance. Fail over only after detecting inconsistency; never merge events from disagreeing forks.
8. Make backfill/replay use the production transformation path with bounded ranges, resumable checkpoints, rate limits, and lag/gap metrics.

Read `skill://blockchain-systems/references/indexer-correctness.md` before changing indexer persistence or reorg logic.

## Transaction and cross-chain path

Model `created → simulated → signed → submitted → observed → confirmed/finalized`, with replacement, expiry, drop, revert, and reorg transitions. Submission timeout means unknown, not failed. Reconcile by signature/hash and nonce; make external effects idempotent.

For bridges and relayers, distinguish source observation, source finality, attestation/proof, destination acceptance, and destination finality. Bind messages to source chain, destination chain, sender, recipient, nonce, payload hash, and expiry. Analyze replay and partial completion.

Read `skill://blockchain-systems/references/transaction-and-cross-chain.md` for execution and provider procedures. Load `skill://smart-contract-defi-security` when funds, signatures, protocol accounting, or oracle data are involved.
