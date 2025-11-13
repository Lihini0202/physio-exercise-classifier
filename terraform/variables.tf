variable "region" {
  description = "The Azure region to deploy resources in (e.g., 'eastus')"
  type        = string
  # IMPORTANT: CHANGE THIS to a region you are allowed to use!
  default     = "eastus"
}
