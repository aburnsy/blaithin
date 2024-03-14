terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.20.0"
    }
  }
}

provider "google" {
  project = var.GCP_PROJECT
  region  = var.GCP_REGION
}

resource "google_storage_bucket" "data-lake-bucket" {
  name     = var.GCP_BUCKET_NAME
  location = var.GCP_BUCKET_LOCATION

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  force_destroy               = true
  public_access_prevention    = "enforced" # Don't allow public access
}
