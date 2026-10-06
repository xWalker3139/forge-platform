# Decisions, boundaries and next work

ADR-001: keep application, desired state and infrastructure in distinct repos.
CI builds immutable images; a reviewed GitOps change promotes a digest.
Infrastructure changes and application changes have separate approval boundaries.

ADR-002: start with kind, not EKS, to test deployment mechanics without cloud cost.
The same Helm chart can be used on both; CNI, IAM, metrics and storage differ.

ADR-003: self-service starts as a CLI that creates reviewable files. The generator
does not receive GitHub admin credentials. Next step: Backstage scaffolder calls
the same golden path, with approval, catalog ownership and audit history.

ADR-004: bounded route labels, JSON request metadata, no user payloads in logs.
No tracing or central log collector is claimed in this baseline.

ADR-005: security context is part of the common chart, not developer opt-in.
Network policy and monitoring require installed platform dependencies.

Next milestones:
1. Automated digest-update PRs with scoped GitHub App credentials.
2. Backstage portal, catalog ingestion and template tests.
3. Validate optional Argo Rollouts templates in a cluster and add precise traffic
   routing and canary-specific metric analysis.
4. Preview namespaces with quotas, TTL cleanup and secret isolation.
5. Workload identity / external secrets, policy admission and signature checks.
6. SLO error-budget dashboard, distributed tracing and disaster recovery drills.

These milestones extend the baseline; rendered templates do not prove runtime behaviour.
