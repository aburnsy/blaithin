#!/bin/bash
set -o allexport && source .env && set +o allexport || true # Ignore errors if .env doesn't exist. Terraform will request any missing variables.

## Verify that required parameters are present
terraform -chdir=Terraform init
terraform -chdir=Terraform validate -json
terraform -chdir=Terraform apply --auto-approve


# Fetch Terraform output for use later
bucket_name=$(terraform -chdir=Terraform output bucket_name)
airflow_uri=$(terraform -chdir=Terraform output airflow_uri)
composer_env_id=$(terraform -chdir=Terraform output composer_env_id)
composer_env_name=$(terraform -chdir=Terraform output composer_env_name)
gcs_bucket=$(terraform -chdir=Terraform output gcs_bucket)
gke_cluster=$(terraform -chdir=Terraform output gke_cluster)
# echo $bucket_name