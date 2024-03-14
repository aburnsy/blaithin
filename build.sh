#!/bin/bash
set -o allexport && source .env && set +o allexport || true # Ignore errors if .env doesn't exist. Terraform will request any missing variables.

## Verify that required parameters are present
terraform  -chdir=Terraform init
terraform -chdir=Terraform apply --auto-approve
bucket_name=$(terraform -chdir=Terraform output -json bucket_name)
bucket_id=$(terraform -chdir=Terraform output -json bucket_id)

echo "##################"
echo $bucket_id
echo $bucket_name