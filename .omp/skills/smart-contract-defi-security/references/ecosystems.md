# Ecosystem-specific review points

## Solidity/EVM

Pin compiler and optimizer/via-IR settings. Inspect proxies, initializers, storage layout, delegatecall/callcode, fallback/receive, CREATE2, selfdestruct assumptions, transient storage, unchecked arithmetic, assembly, allowance races, permit variants, chain ID/domain caching, and external-call return handling. Fork tests must pin a block and document mutable external dependencies.

## Solana/Anchor

Validate every account's owner, signer, writable status, PDA seeds/bump, discriminator/type, executable program, token mint/authority, and relationship to other accounts. Do not trust client-supplied remaining accounts or CPI programs. Check account close/reinitialization, duplicate mutable accounts, lamport/rent handling, arithmetic, compute limits, transaction account locking, versioned transactions/address tables, and upgrade authority. Simulation success does not prove a later blockhash/account state remains valid.

## Move

Model resource ownership, abilities (`copy`, `drop`, `store`, `key`), signer/capability authority, module/friend visibility, object IDs, shared objects, generic type constraints, and upgrade compatibility. Prove no capability/resource can be duplicated, leaked, or destroyed outside intended lifecycle. Use specifications/provers where available, then back them with executable boundary tests.

## Cairo/Starknet

Check felt/range conversions, storage key/domain separation, L1↔L2 message identity and replay, account abstraction signature/nonce semantics, class replacement/upgrades, syscall and external-call behavior, reentrancy across components, sequencer/timestamp assumptions, and integer/field arithmetic differences. Verify compiler and Sierra/CASM toolchain versions.

## Other ecosystems

Do not project EVM vocabulary onto another VM. First verify its execution atomicity, account/resource model, authorization primitive, upgrade mechanism, message/reorg/finality semantics, arithmetic types, and available analysis tools from primary sources.
