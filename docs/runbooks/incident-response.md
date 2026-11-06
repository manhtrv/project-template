# Incident response runbook

## Authority boundary

This runbook authorizes investigation and planning only. Production changes, traffic shifts, deploys, rollbacks, restarts, secret rotation, data repair, contract actions, and fund movement require an explicitly authorized operator.

## Stabilize

1. Name incident lead, communications owner, and recorder.
2. Confirm user impact from service-level indicators; record start time, scope, and severity.
3. Freeze unrelated changes and preserve logs/traces/config/deploy metadata.
4. Identify the safest reversible mitigation with expected effect, risk, rollback, and verification.
5. Obtain authorization, execute one controlled action, and observe user-facing recovery plus backlog/data effects.

## Investigate

Build a timestamped timeline of deploys, config/IaC changes, dependency health, saturation, errors, and traces. Rank falsifiable hypotheses. Use read-only queries first; redact secrets and customer data. Correlation with the latest deploy is evidence, not proof.

## Recover

- Verify availability, correctness, latency, freshness, and durability SLIs.
- Reconcile queues, transactions, chain/indexer state, caches, and partial migrations.
- Confirm canaries/regions/tenants independently.
- Maintain heightened observation through the relevant recurrence window.

## Follow-up

Document root cause, contributing conditions, why controls did not prevent/detect it, and corrective actions. Each action needs an owner, due condition, and verification method. Test rollback and disaster-recovery changes; documentation alone is not a control.
