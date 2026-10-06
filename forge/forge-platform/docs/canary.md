# Optional Argo Rollouts experiment

The chart implements an optional Rollout and AnalysisTemplate, disabled by default.
Install Argo Rollouts controller/CRDs and Prometheus Operator first. Enable
monitoring and progressiveDelivery together, and set the correct Prometheus URL.

For a lab migration from Deployment to Rollout, use a fresh release name, e.g.
`canary-demo`, rather than allowing GitOps to prune the working Deployment in place.
Configure the GitOps application releaseName accordingly. Ensure at least 5 replicas
and enough cluster capacity if you want 20% representable by replica counts.

The first deploy creates a baseline; promote a second image/digest to demonstrate
the canary steps: 20%, 60s pause, analysis, 50%, pause, analysis, 100%.
With no ingress traffic router, weights approximate the replica ratio, not exact
per-request percentages. Analysis uses the combined service success rate, not
canary-only metrics. This lab cannot claim precise traffic splitting or isolation.

Keep sustained requests flowing through the Service while Prometheus scrapes.
The metric query assumes Prometheus Operator's `service` target label is present.
Inspect the actual labels before the experiment. No data should not count as a
healthy release; empty/NaN results do not satisfy the success condition.

Demonstrate failure by promoting an intentionally modified lab image that returns
5xx from `/api/greeting`. Fault requests sent to all replicas test the aggregate
analysis but cannot attribute the fault exclusively to the canary. Do not manufacture
a claimed canary-specific result from this combined metric.

A failed inline analysis aborts the rollout to the stable revision. Repair/revert
the desired Git digest afterward: controller abort and GitOps rollback are distinct.
Record AnalysisRun output, replica counts, error ratio and final serving version.

The Rollout/AnalysisTemplate syntax was rendered locally; runtime abort behaviour
requires controller and cluster validation. This is not a production release gate.
