# blaithin
My submission for the Data Engineering Zoomcamp 2024


# Goal of Blaithin
The motivation behind this project was to provide gardeners and aspiring gardeners in Ireland with a simplified tool for facilitating plant selection for their gardens. 

Gardening is a fantastic hobby which comes with a wealth of benefits. However, it can be daunting for beginners to understand where to start. They may not select plants which are ideal for their space. They may purchase a plant which requires a very specific type of soil (ericaceous etc) or which is invasive and will take over their space. 

There is also a vast differential in prices across the main nurseries in Ireland. The same product in 1 nursery may be over twice the price in another nursery for comparable quality and size. Give examples. 

As someone who is passionate about gardening, I find the process of buying new plants very frustrating. I research new plants/ideas on a number of different websites. With my selections in mind, I then have search through many known nurseries which deliver to my location to determine which has the best pricing including delivery fees (which can be up to €60 in some cases).

# Build Instructions

# Assumptions
* terraform cli is installed
* 
* 
Please note that I ran this on a Windows machine only. If some part of this script does not work on Mac/Linux, please let me know.

### 1. Optional create a .env file in the root directory
This will prevent the need to pass in variables to the Terraform script.
The .env file should have the following structure
```bash
TF_VAR_GCP_PROJECT=google_project_name # This is used in the Terraform scripts to create new assets in GCP
```

### 2. Setting permissions in Google 
Add role to the default engine account

### 2. Run build.sh
This will run x, y , z
> [!NOTE]  
> Creating the Composer environment 
```bash
./build.sh
```

### 3. Backfill historical data
As the data for the project is scraped from the web using BS4, no historic data is available. As such, without backfilling, the temporal charts will not have anything to show. 

I have collected historical data for a number of weeks which can be used.
The volume of data per day is approx 10m, 
```bash
./backfill.sh -days 28
```









# Destroy Instructions
The easiest way to remove everything in GCP is to run terraform destroy from within the Terraform directory.
```bash
terraform destroy -chdir=Terraform
```