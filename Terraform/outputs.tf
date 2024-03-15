output "bucket_name" {
  value = google_storage_bucket.blaithin_bucket.name
}

output "airflow_uri" {
  value = module.composer_example_simple_composer_env_v2.airflow_uri
}

output "composer_env_id" {
  value = module.composer_example_simple_composer_env_v2.composer_env_id
}
output "composer_env_name" {
  value = module.composer_example_simple_composer_env_v2.composer_env_name
}
output "gcs_bucket" {
  value = module.composer_example_simple_composer_env_v2.gcs_bucket
}
output "gke_cluster" {
  value = module.composer_example_simple_composer_env_v2.gke_cluster
}
