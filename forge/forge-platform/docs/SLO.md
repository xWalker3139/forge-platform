# Service objective and experiment design

Lab target: 99.9% successful application requests over 30 days and p95 <500ms.
Health and scrape endpoints are excluded. All application traffic including
synthetic fault requests is included; keep experiments in a separate dev environment.
The alert ratio is a short-window operational warning, not a complete multi-window
error-budget burn-rate implementation. No historical achievement is claimed.

Estimate a request-based error budget as 0.001 * total requests in the window.
Use real observation data; a short local run does not prove monthly availability.

Experiment table to fill after execution:

| Experiment | Hypothesis | Actual result | Recovery time |
| --- | --- | --- | --- |
| Pod deletion | Other replica continues serving | Record load output | Measure |
| Bad image digest | Readiness prevents healthy replica removal | Record rollout events | Measure |
| Fault injection | Error/latency graphs increase | Record screenshots | Measure |
| Git revert | Argo restores previous image | Record sync/version | Measure |

Scale and routing experiments must use real Service traffic, not only port-forward
to one pod, which cannot demonstrate load balancing and replica failover.
