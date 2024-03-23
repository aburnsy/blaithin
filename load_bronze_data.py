import argparse
import bronze.tullys as tullys
import bronze.quickcrop as quickcrop
import cloud_storage


def main(params):
    root_path = f"{params.bucket_name}/bronze"

    match params.sites:
        case "tullys":
            cloud_storage.export_data_locally(
                table=tullys.get_product_data("tullys_test"), root_path=root_path
            )
        case "quickcrop":
            cloud_storage.export_data_locally(
                table=quickcrop.get_product_data("quickcrop_test"),
                root_path=root_path,
            )
        case _:
            cloud_storage.export_data_to_gcs(
                table=tullys.get_product_data(), root_path=root_path
            )
            cloud_storage.export_data_to_gcs(
                table=quickcrop.get_product_data(), root_path=root_path
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape data from sites and store to gcs bronze area"
    )
    parser.add_argument(
        "--bucket_name", help="Bucket name in GCS to store data to.", required=True
    )
    parser.add_argument(
        "--sites",
        help="Name of the site you would like to fetch data for.",
        choices=["tullys", "quickcrop"],
    )
    args = parser.parse_args()
    main(args)

# d:/Development/blaithin/.venv/Scripts/python.exe d:/Development/blaithin/load_bronze_data.py --bucket_name=$(terraform -chdir=Terraform output -raw bucket_name)
