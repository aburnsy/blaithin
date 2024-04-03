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



resource "google_bigquery_dataset" "blaithin" {
  dataset_id                  = "blaithin"
  description                 = "This dataset contains the rhs detailed data."
  location                    = var.GCP_BUCKET_LOCATION
  default_table_expiration_ms = 999999999

}

resource "google_bigquery_table" "rhs" {
  dataset_id = google_bigquery_dataset.blaithin.dataset_id
  table_id   = "rhs"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"

    source_uris = [
      "gs://${google_storage_bucket.blaithin_bucket.name}/rhs/*.parquet",
    ]
  }
  depends_on = [google_storage_bucket.blaithin_bucket]
}
