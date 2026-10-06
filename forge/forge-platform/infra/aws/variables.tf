variable "region" {
  type    = string
  default = "eu-west-1"
}
variable "name" {
  type    = string
  default = "forge-lab"
}
variable "kubernetes_version" {
  type        = string
  description = "Choose a currently supported EKS version after checking AWS documentation."
}
variable "admin_cidrs" {
  type        = list(string)
  description = "Explicit administrator public IP CIDRs; never allow the whole internet."
  validation {
    condition     = length(var.admin_cidrs) > 0 && alltrue([for cidr in var.admin_cidrs : can(cidrhost(cidr, 0)) && !contains(["0.0.0.0/0", "::/0"], cidr)])
    error_message = "Supply valid restricted administrator CIDRs."
  }
}
