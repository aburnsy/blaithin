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

resource "google_service_account" "blaithin_service_account" {
  account_id   = "blaithin-composer-account"
  display_name = "Service Account for Composer Environment"
}

resource "google_project_iam_member" "composer-worker" {
  project = var.GCP_PROJECT
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.blaithin_service_account.email}"
}
resource "google_compute_network" "blaithin_network" {
  name                    = "blaithin-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "blaithin_subnetwork" {
  name          = "blaithin-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  network       = google_compute_network.blaithin_network.id
}
module "composer_example_simple_composer_env_v2" {
  source                   = "terraform-google-modules/composer/google//modules/create_environment_v2"
  version                  = "5.0.0"
  composer_env_name        = "blaithin-composer"
  network                  = "blaithin-network"
  project_id               = var.GCP_PROJECT
  subnetwork               = "blaithin-subnetwork"
  composer_service_account = google_service_account.blaithin_service_account.name
  environment_size         = "ENVIRONMENT_SIZE_SMALL"
  image_version            = "composer-2-airflow-2"
  scheduler                = { "count" : 1, "cpu" : 1, "memory_gb" : 2, "storage_gb" : 1 }
  web_server               = { "cpu" : 1, "memory_gb" : 2, "storage_gb" : 1 }
  worker                   = { "cpu" : 4, "max_count" : 3, "memory_gb" : 16, "min_count" : 1, "storage_gb" : 8 }
  region                   = var.GCP_REGION
}

resource "google_storage_bucket" "blaithin_bucket" {
  name     = "blaithin-${random_string.key_suffix.result}"
  location = var.GCP_BUCKET_LOCATION

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  force_destroy               = true
  public_access_prevention    = "enforced" # Don't allow public access
}
