# DeFi, RFQ, aggregation, and execution invariants

## Quote/RFQ contract

A quote binds maker/solver, taker or open-taker policy, input/output assets, exact-in or exact-out semantics, amount, price/limit, fees, recipient, chain/domain, venue/route commitment if relevant, nonce, expiry, partial-fill policy, and signature scheme.

- Reject stale quotes using an explicit time/slot source and clock-skew policy.
- Consume nonces atomically with fills; define unordered nonce bitmaps or sequential semantics precisely.
- For partial fills, track filled input/output in one canonical unit and prove cumulative rounding cannot exceed signed limits.
- Domain-separate every chain, verifying contract/program, version, and action type.

## AMM/accounting invariants

Depending on mechanism, verify:

- reserves and balances reconcile after fees/transfers;
- shares represent proportional claim under deposits, withdrawals, fees, donations, and loss;
- invariant movement and fee rounding favor the protocol-defined side without enabling extraction loops;
- price/tick/liquidity transitions remain bounded at extremes;
- flash liquidity restores required balances/invariant in the same transaction;
- token decimals, rebasing, fee-on-transfer, callbacks, and approval behavior are either supported or rejected.

## Aggregation and bots

- Market data has source, sequence/timestamp, max age, and cross-source consistency rules.
- Simulation occurs against a state close enough to intended execution; define invalidation on block/hash, nonce, pool state, or price movement.
- Enforce slippage, min-out/max-in, deadline, gas/fee cap, exposure, inventory, per-asset and per-counterparty limits.
- Submission is idempotent by logical intent. Reconcile unknown outcomes before retrying.
- Circuit breakers specify trigger, scope, automatic versus authorized reset, and behavior for in-flight orders.
- Record signed quote/intent, decision inputs, simulation result, route, transaction identities, and final accounting without leaking keys.

## MEV and oracle risk

Analyze whether an attacker can observe and reorder, sandwich, back-run, censor, or force liquidation. Mitigations may include protected orderflow, batch auctions, commit/reveal, tighter bounds, TWAP/median, multiple sources, delayed finalization, or explicit user choice. Never claim “MEV-proof”; state the adversary and remaining ordering power.

## Properties

Property/invariant tests should cover conservation, no profitable round-trip from rounding alone, monotonic nonce/fill state, bounded user loss, stale-price rejection, equivalent split versus single fills within specified rounding, and idempotent repeated execution.
