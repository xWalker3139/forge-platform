# Optional AWS lab

Prerequisites: Terraform >=1.6, AWS CLI authenticated to your own sandbox account,
and a public admin IP. No cloud resources were deployed while producing this bundle.

Create a local `lab.tfvars` (ignored by Git):

```hcl
region = "eu-west-1"
kubernetes_version = "REPLACE_WITH_CURRENTLY_SUPPORTED_EKS_VERSION"
admin_cidrs = ["REPLACE_WITH_YOUR_PUBLIC_IP/32"]
```

Choose a supported version from current AWS EKS documentation; don't apply the
placeholder. Run `terraform init`, `terraform validate`, `terraform plan -var-file=lab.tfvars`.
Review cost and changes before `terraform apply -var-file=lab.tfvars`.
Then `aws eks update-kubeconfig --name forge-lab --region eu-west-1`.
Use the GitOps/Helm setup with a registry image, not kind's local-only image.

State is local by default for the lab. Before collaboration, configure an encrypted
remote backend with locking and limited IAM; do not upload terraform state to Git.
The generated `.terraform.lock.hcl` is included. Modules and provider
baselines must be reviewed against the EKS version and current security advisories.

Design: 2 AZs, private worker subnets, restricted public control-plane access,
2 worker nodes, one NAT gateway (cost-saving lab tradeoff, single-AZ dependency).
This is not a production HA network. No load balancers, external DNS, cluster
autoscaler, budget alarm, storage driver, or service mesh are provisioned.

Cleanup: remove Kubernetes resources that create load balancers/volumes first,
review `terraform plan -destroy -var-file=lab.tfvars`, then intentionally run
`terraform destroy -var-file=lab.tfvars`. Inspect the account for orphan resources.
