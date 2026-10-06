# Validation report

Performed on Linux, Python 3.12.14:

- uv lock generation and uv sync --locked: passed.
- Ruff checks and formatting: passed.
- 8 service tests: passed, including actual Uvicorn startup, 20 HTTP requests,
  SIGTERM and completed application shutdown. That signal test is skipped on
  Windows because native process termination has different semantics.
- 2 scaffold tests: passed, including overwrite and path-traversal rejection.
- Helm 3.17.3 lint: passed (optional chart icon informational notice only).
- Helm render: dev, prod, monitoring/HPA/NetworkPolicy and canary options passed.
- 13 rendered Kubernetes objects: parsed and security/probe assertions passed.
- YAML files and Grafana dashboard JSON: parsed successfully.
- Terraform 1.9.8 formatting: passed.
- Terraform init with signed providers and readonly lockfile: passed after
  reinstalling an AWS cache package that initially failed integrity verification.
- Terraform validate: NOT completed. Provider schema processes failed their plugin
  handshake in this execution environment (all five providers). This is not a
  successful schema validation; run init/validate in your normal local environment
  and review the plan before any apply. The lockfile integrity guard was retained.

One non-failing Starlette/AnyIO deprecation warning was observed.
Docker daemon, kind cluster, Argo CD, monitoring stack and AWS deployment were
not available/executed here. Their runtime behaviour is not certified by static
checks. GitHub workflows were authored, not executed on GitHub.

Optional canary Rollout, AnalysisTemplate and HPA target were rendered and checked
for consistency. The Argo Rollouts controller was not run; automatic abort was
not demonstrated.
