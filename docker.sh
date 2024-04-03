#!/bin/bash

# Fetch Terraform output for use within Mage
export PROJECT_NAME=blaithin
export GCS_BUCKET_NAME=$(terraform -chdir=Terraform output -raw bucket_name)

cd docker && docker compose up -d --build