---
name: smart-contract-defi-security
description: Smart-contract and DeFi security procedure for Solidity/EVM, Solana/Anchor, Move, Cairo, access control, reentrancy, signatures, upgrades, accounting invariants, oracles, precision, MEV, AMMs, RFQ, simulation, fuzzing, and exploitability. Use for audits or any change that can move funds or alter protocol authorization/accounting.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Smart-contract and DeFi security

## Audit procedure

1. **Scope and build truth:** pin repository revision, compiler/toolchain, chain, deployment/proxy addresses if relevant, dependencies, generated code, test commands, and excluded components. Build with the repository's actual toolchain.
2. **Threat model:** enumerate privileged roles, users, keepers, relayers, signers, oracles, bridges, callbacks, token behaviors, upgrade authorities, and external protocols. Treat every external return value and callback as adversarial.
3. **State and invariants:** express authorization, conservation, solvency, share/asset conversion, fee, collateral, nonce, supply, and lifecycle invariants before searching for patterns.
4. **Trace value paths:** deposits, withdrawals, swaps, borrows, liquidation, claims, upgrades, emergency paths, and rescue functions. Follow checks, effects, calls, rounding, and failure rollback across contracts/programs.
5. **Investigate candidates:** prove attacker control, reachable path, broken control/invariant, impact, and preconditions. Run static analysis, tests, simulation, fuzzing, and invariant tools that are actually installed. Do not call a pattern exploitable without a concrete path.
6. **Report:** severity, confidence, affected code, invariant broken, attack sequence, impact, evidence/reproduction, and minimal remediation. Separate confirmed findings, conditional risks, and hardening suggestions.

Read `skill://smart-contract-defi-security/references/contract-audit.md` for vulnerability classes and evidence standards. Read `skill://smart-contract-defi-security/references/defi-execution.md` for AMM, oracle, RFQ, aggregation, and bot systems. Read `skill://smart-contract-defi-security/references/ecosystems.md` for EVM, Solana, Move, and Cairo differences.

## Mandatory independent review

A change affecting custody, authorization, upgrades, signatures, pricing, accounting, liquidation, or cross-chain acceptance requires a separate security review. Never sign, deploy, upgrade, transfer funds, or change live ownership without explicit authorization.
