import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq


def add_defaults_to_fields(
    df: pl.DataFrame, field_name: str, default_value
) -> pl.DataFrame:
    if field_name not in df.columns:
        print(f"Adding column {field_name} with default value {default_value}")
        return df.with_columns((pl.lit(default_value)).alias(field_name))
    else:
        return df


def export_data_to_gcs(table: list[dict], root_path: str) -> None:
    # Easiest to use Polars to convert a list of dictionaries into a DF/Table
    df = pl.DataFrame(table)

    df = add_defaults_to_fields(df, field_name="product_code", default_value=None)
    df = add_defaults_to_fields(df, field_name="quantity", default_value=1)

    table = df.to_arrow()

    print(f"Storing data to bucket {root_path}")

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["source"],
        filesystem=pa.fs.GcsFileSystem(),
        existing_data_behavior="delete_matching",
    )


def export_data_locally(table: list[dict], root_path: str) -> None:
    # Easiest to use Polars to convert a list of dictionaries into a DF/Table
    df = pl.DataFrame(table)
    table = df.to_arrow()

    source = df.select(pl.first("source")).item()
    print(f"Storing data to file 'test\\{source}.parquet'")
    pq.write_table(table, f"test\\{source}.parquet")
