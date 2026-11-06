# ADR 0002: Complement bundled agents instead of replacing them

- Status: Accepted

## Context

OMP 18.16.0 already bundles `scout`, `reviewer`, `security-reviewer`, `task`, `sonic`, and `seance`. Project agents override bundled agents on exact name collision. Recreating them would add maintenance and silently replace runtime defaults.

## Decision

Add only `architect`, `test-engineer`, `sre`, and `smart-contract-auditor`. Reuse bundled exploration, review, general security, and `task` implementation agents. Keep project specialists non-recursive; the top-level session owns orchestration and integration. Grant the three analysis-only specialists only `read`, `grep`, and `glob`.

## Consequences

- Four differentiated project roles, no accidental shadowing, and no custom implementation role overlapping bundled `task`.
- Role aliases remain operator-configurable.
- Independent review uses separate bundled specialists unless domain-specific contract analysis is needed; their output remains evidence to verify, not authority.
