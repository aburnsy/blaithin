# Build Instructions

# Assumptions
* terraform cli is installed
* docker can be run locally
* google auth uses local json file

Please note that I ran this on a Windows machine only. If some part of this script does not work on Mac/Linux, please let me know.

### 1. Optional create a .env file in the root directory
This will prevent the need to pass in variables to the Terraform script.
The .env file should have the following structure
```bash
TF_VAR_GCP_PROJECT=google_project_name
TF_VAR_GCP_REGION=us-central1
TF_VAR_GCP_BUCKET_LOCATION=US
```

### 2. Add your google account key
Add your google account key under config folder and name it 'account_key.json'.
This is used not only by the Terraform scripts but by DBT and Mage data loaders and exporters.

### 3. Run build.sh
This will run the terraform scripts under the Terraform folder.
```bash
./build.sh
```

### 4. Run start.sh
This will build the docker image and containers and start the same containers.
Once Mage starts up, 2 tasks will kick off to load source data and export to staging tables in Cloud Storage.
```bash
./start.sh
```


### Monitoring
Once you have started the containers, you can navigate to [your local Mage](http://localhost:6789/pipelines?_limit=30) to view the running pipelines, monitor logs and ensure successful completion.


# Stop and destroy
To stop the running containers, run 
```bash
./stop.sh
```
To destroy the Terraform infra, run
```bash
./destroy.sh
```