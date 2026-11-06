# Transaction, RPC, and cross-chain reliability

## Transaction state machine

Use explicit transitions:

`created → simulated → signed → submitted → observed → confirmed → finalized`

Side states: `simulation-failed`, `submission-unknown`, `replaced`, `expired`, `dropped`, `reverted`, `orphaned`.

Rules:

- A submission timeout is `unknown`; query by signature/hash and nonce before resubmitting.
- Persist intent identity separately from transaction hash so fee-bumps/replacements remain one logical operation.
- Serialize nonce/account-sequence allocation or use compare-and-swap; reconcile with chain state after crashes.
- Simulation must use the intended block/state, sender, value, calldata/accounts, gas/compute limits, fee policy, and slippage/deadline. A successful simulation is not execution proof.
- Decode revert/program errors and receipts from the actual provider; do not convert every failure into “RPC error.”
- Reorgs can move observed/confirmed operations backward. Make downstream notifications and accounting idempotent/reversible until required finality.

## RPC reliability

- Assign providers capabilities: archive depth, websockets, trace/simulation methods, rate limits, chain ID/genesis, and trust class.
- Health checks verify chain identity and recent canonical hash, not only HTTP 200.
- Use bounded retries with jitter only for proven transient/idempotent calls. Respect rate-limit headers and total deadlines.
- Quorum reads need a field-specific comparison rule. Never majority-vote nondeterministic metadata blindly.
- Record provider, method, block tag/hash, latency, and error class with cardinality control.

## Cross-chain messages

Bind signatures/proofs to domain separator, source chain, destination chain, source sender, destination recipient, nonce/message ID, payload hash, amount/token semantics, and expiry/version.

State machine:

`source-created → source-observed → source-finalized → proof/attestation-ready → destination-submitted → destination-finalized`

Analyze:

- source and destination reorgs independently;
- duplicate relay and destination idempotency;
- validator/attester threshold and key rotation;
- message ordering versus independent nonces;
- partial completion and refund/recovery authority;
- decimal/token representation and wrapped/native asset accounting;
- pause/circuit-breaker scope and safe restart.

Verification includes replaying the same message, wrong-chain/domain signatures, delayed/expired messages, conflicting attestations, relayer crash after submit, and source reorg before/after attestation.
