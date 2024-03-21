import argparse
import bronze.tullys as tullys
import cloud_storage


def main(params):
    root_path = f"{params.bucket_name}/bronze"

    match params.sites:
        case "tullys":
            tullys_results = tullys.get_product_data()
            cloud_storage.export_data_to_gcs(table=tullys_results, root_path=root_path)
        case _:
            tullys_results = tullys.get_product_data()
            cloud_storage.export_data_to_gcs(table=tullys_results, root_path=root_path)


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
