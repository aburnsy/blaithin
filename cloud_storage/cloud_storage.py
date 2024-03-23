import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq


def export_data_to_gcs(table: list[dict], root_path: str) -> None:
    # Easiest to use Polars to convert a list of dictionaries into a DF/Table
    df = pl.DataFrame(table)
    table = df.to_arrow()

    print(f"Storing data to bucket {root_path}")

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["source"],
        filesystem=pa.fs.GcsFileSystem(),
        existing_data_behavior="delete_matching",
    )


def test_export_data_to_gcs(table: list[dict], root_path: str) -> None:
    # Easiest to use Polars to convert a list of dictionaries into a DF/Table
    df = pl.DataFrame(table)
    table = df.to_arrow()

    source = df.select(pl.first("source")).item()

    print(f"Storing data to bucket {root_path}")

    pq.write_table(table, f"test\\{source}.parquet")
