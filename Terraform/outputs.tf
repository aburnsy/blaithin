output "bucket_name" {
  value = google_storage_bucket.blaithin_bucket.name
}
output "big_query_table" {
  value = google_bigquery_table.rhs.id
}
