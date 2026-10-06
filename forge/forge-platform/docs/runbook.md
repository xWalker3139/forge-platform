# Forge operations exercises

## Deployment not ready
`kubectl -n forge-dev get pods` -> `describe pod` -> `logs`.
Check image availability, probe status, CPU/memory limits, and events.
ImagePullBackOff in kind: import exact tag. In AWS: use public/authorized registry.

## 5xx / latency alert
Check version and image digest, graph error ratio and p95, inspect request IDs.
In dev check whether fault injection is being called. Do not disable probes to
hide an outage. Stop synthetic requests and document recovery measurements.

## Rollback in GitOps
Revert the commit that changed image digest and merge through review. Argo CD
reconciles. `kubectl rollout undo` is temporary when GitOps self-heal is enabled.
Check `/version`, readiness and representative requests after reconciliation.
This Git rollback workflow is manual. The optional Rollouts analysis configuration
is described in canary.md; runtime behaviour has not been verified in this build.

## Restart and graceful shutdown
Send traffic, delete one deployment pod, watch replacements become ready.
Record error count and recovery time. A PDB governs voluntary disruptions (drain),
not arbitrary pod deletion or Deployment rolling updates.

## HPA
Install Metrics Server first, enable autoscaling, generate load and watch HPA.
CPU load may be low for this I/O-oriented service; a latency injection does not
prove CPU autoscaling. Do not invent scale-out claims without observed evidence.

## Cleanup
Stop port-forwards and load scripts. Local: `kind delete cluster --name forge`
removes the lab cluster. Compose: `docker compose down`. AWS cleanup is described
in infra/aws/README.md; deleting kind does not remove any AWS resources.
