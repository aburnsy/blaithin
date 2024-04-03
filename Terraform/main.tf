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

resource "random_string" "key_suffix" {
  length  = 5
  special = false
  upper   = false
}

resource "google_storage_bucket" "blaithin_bucket" {
  name     = "blaithin-${random_string.key_suffix.result}"
  location = var.GCP_BUCKET_LOCATION

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  force_destroy               = true
  public_access_prevention    = "enforced" # Don't allow public access
}
