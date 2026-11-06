# Production operations reference

## Kubernetes/EKS

Check:

- immutable image digest, SBOM/signing policy, non-root/read-only filesystem, dropped capabilities, seccomp;
- service account and IRSA/pod identity least privilege; no static cloud keys;
- requests/limits based on measured working set; OOM/throttling signals;
- startup/readiness/liveness probes that reflect their distinct purposes;
- PodDisruptionBudget, topology spread/anti-affinity, multi-AZ dependency behavior;
- HPA signal and stabilization, queue/backpressure limits, graceful termination and preStop/drain;
- NetworkPolicy/ingress/egress, TLS, DNS and dependency timeouts;
- version skew for cluster, nodes, controllers, CNI/CSI, admission policies, and APIs.

## CI/CD and IaC

Pin actions/images/modules; minimize token permissions; isolate untrusted PRs from secrets; protect artifacts/provenance; scan dependencies/IaC without treating scanner output as proof. Use remote state locking/encryption, reviewed plans, drift detection, import discipline, and bounded blast radius. A plan is not authorization to apply.

## Secrets

Keep secrets in an approved manager, inject at runtime with least scope, avoid command-line/log exposure, rotate with overlap, audit access, and test revocation. Never commit encrypted material unless the repository's established design explicitly owns key management.

## Observability and SLOs

- SLIs reflect user outcomes: availability, correctness, latency, freshness, durability.
- Define SLO window/target and error-budget policy.
- RED metrics for request-driven services; USE for resources; queue lag/age for async; chain/RPC lag and disagreement for blockchain.
- Structured logs carry request/trace/tenant-safe identifiers and error class; redact secrets and bound cardinality.
- Trace context crosses async and external boundaries; sampling preserves errors and high-latency paths.
- Alerts require an action and runbook, favor burn-rate/user-impact over noisy component symptoms.

## Rollout and rollback

Before rollout: compatibility matrix, migration phase, canary population, stop signals, dashboard/query links, on-call ownership, rollback command/path, and data consequences. Verify after each stage with user-facing SLIs and invariants. Rollback is unsafe if new writes are unreadable by old code; choose roll-forward or a compatible expand phase instead.

## Disaster recovery

Define RPO/RTO per data class and dependency. Inventory backups, replication, keys, DNS/network, artifacts, IaC state, and external providers. Encrypt and separate backups, monitor age/completeness, and run restore/failover exercises that measure actual RPO/RTO. Document reconciliation after partial-region/provider recovery.
