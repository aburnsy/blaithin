#!/bin/bash

export PROJECT_NAME=blaithin
export GCS_BUCKET_NAME=$(terraform -chdir=Terraform output -raw bucket_name)
export GCP_PROJECT=$(terraform -chdir=Terraform output -raw gcp_project)

cd docker && docker compose down