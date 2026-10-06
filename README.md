# forge-platform

Internal developer platform reference implementation with self-service scaffolding, Kubernetes golden paths, GitOps configuration, CI/CD, observability, and AWS EKS infrastructure definitions.

Forge — Internal Developer Platform

Forge is a platform engineering reference project that standardizes how developers create, package, deploy, and observe stateless HTTP services.
It combines a self-service service generator, a FastAPI reference application, reusable Helm deployment templates, GitOps configuration, and optional AWS infrastructure definitions. The project starts with a local Kubernetes lab and keeps cloud infrastructure separate from application delivery.
Status: functional reference implementation. Application tests and static checks have passed; Kubernetes, GitOps, canary and AWS behaviour still require validation in a running environment.

Problem addressed

Teams often repeat service setup, container configuration, CI pipelines and deployment manifests. Differences between those implementations make operations harder and leave important defaults to individual developers.
Forge provides a reusable golden path: developers generate a service from a shared template, CI produces a versioned image, and an explicit GitOps change selects what the cluster should run.
