# Contract audit evidence checklist

## Authorization and lifecycle

- Every privileged transition names the authorized principal and scope.
- Initialization is one-time and cannot be front-run or replayed.
- Upgrade authorization, implementation compatibility, storage/account layout, timelock, rollback, and emergency powers are explicit.
- Pause behavior is complete and cannot permanently trap assets without a governed recovery path.

## Calls and reentrancy

- Apply checks-effects-interactions where it preserves semantics; guard all mutually reentrant entry points sharing an invariant, not one function in isolation.
- Check callbacks from ERC-777/721/1155, flash loans, token hooks, fallback/receive, Solana CPI, and arbitrary adapters.
- Handle return values and non-standard token behavior. Balance deltas may be safer than requested amounts for fee-on-transfer tokens.
- Bound gas/compute and untrusted iteration; avoid denial of service through recipient behavior.

## Signatures and replay

Verify scheme, signer recovery/verification, canonical encoding, domain separator, chain/program identity, contract/account identity, nonce, deadline/slot, action type, amount, recipient, and upgrade/domain changes. Mark the nonce consumed in the same atomic execution as the action. Do not use transaction origin as authorization.

## Arithmetic and accounting

State conservation equations and rounding direction for every conversion. Test zero, one unit, max values, first/last depositor, empty/full liquidity, extreme price/decimal ratios, fee boundaries, and repeated tiny operations. Rounding must not create a profitable loop.

## Oracles and ordering

Check source trust, heartbeat/staleness, confidence/deviation, decimal normalization, zero/negative values, sequencer status, manipulation window, fallback behavior, and liquidation impact. Analyze sandwiching, back-running, transaction ordering, private orderflow assumptions, and block timestamp/slot dependence.

## Finding proof

A reportable vulnerability needs:

1. attacker capability and initial state;
2. reachable calls/transactions;
3. control bypass or invariant break;
4. concrete impact and affected assets/users;
5. environmental assumptions;
6. code locations and test/simulation or rigorous trace.

Severity considers impact **and** realistic exploitability. A dangerous-looking opcode/API without a reachable exploit path is a review candidate, not a confirmed vulnerability.

## Tools

Use only installed tools and record versions/commands: compiler/tests; Slither/Mythril or equivalent; Foundry/Hardhat fuzzing and invariants; Anchor/Solana program tests; Move Prover; Cairo/Starknet tests; fork/local-validator simulation. Tool output is a lead, never the final finding.
