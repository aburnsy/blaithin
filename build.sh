#!/bin/bash
set -o allexport && source .env && set +o allexport || true # Ignore errors if .env doesn't exist. Terraform will request any missing variables.

## Verify that required parameters are present
terraform -chdir=Terraform init
terraform -chdir=Terraform validate -json
terraform -chdir=Terraform apply --auto-approve


# Fetch Terraform output for use later
bucket_name=$(terraform -chdir=Terraform output -raw bucket_name)
# echo $bucket_name