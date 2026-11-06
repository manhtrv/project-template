---
name: production-sre
description: Production reliability procedure for incidents, Kubernetes/EKS, AWS, IaC, CI/CD, secrets, migrations, OpenTelemetry, logs/metrics/traces, SLI/SLOs, rollout, rollback, capacity, RPC availability, and disaster recovery. Use for infrastructure changes, outages, deployment safety, and operational readiness.
compatibility: OMP 18.16.0 with read support for skill URIs (verified).
---

# Production SRE

## Incident mode

1. Confirm impact from independent signals; establish incident scope, start time, affected users/regions/tenants, and current change window.
2. Protect people and data. Freeze risky changes, preserve evidence, and choose the safest reversible mitigation. Do not execute production actions without authorization.
3. Form a timeline from deploys, config changes, saturation, dependency health, errors, and traces. Correlation is not cause; test hypotheses against telemetry.
4. Mitigate first when impact is active, but do not hide evidence. Record exact commands/actions and expected rollback.
5. Verify recovery using user-facing SLIs, not only pod/process health. Watch for backlog, retries, data inconsistency, and recurrence.
6. After stabilization, identify root cause, contributing controls, detection gap, and durable corrective actions with owners and validation.

## Change/readiness mode

- Define service SLI/SLO and error-budget effect.
- Check resource requests/limits, disruption budgets, probes, autoscaling signals, topology spread, termination grace, and dependency timeouts/backpressure.
- For EKS/IaC, inspect IAM least privilege, network boundaries, state locking, drift, immutable artifacts, admission/policy controls, and upgrade compatibility.
- For migrations, separate expand, backfill, cutover, and contract; make each resumable and rollback-aware. Avoid long blocking transactions and mixed-version incompatibility.
- Instrument structured logs, RED/USE metrics, trace context propagation, cardinality bounds, and actionable alerts before rollout.
- Define canary stages, stop signals, rollback mechanics, and post-deploy verification. Backups count only after restore tests.

Read `skill://production-sre/references/production-operations.md` for Kubernetes, observability, secrets, rollout, and disaster-recovery checklists.
