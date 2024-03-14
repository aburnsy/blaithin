variable "GCP_PROJECT" {
  type = string
}

variable "GCP_REGION" {
  type    = string
  default = "us-central1"
}

variable "GCP_BUCKET_LOCATION" {
  description = "Location of Storage Bucket"
  type        = string
  default     = "US"
}

variable "GCP_BUCKET_NAME" {
  description = "Name of the Storage Bucket. This has to be unique across all GCP."
  type        = string
}
