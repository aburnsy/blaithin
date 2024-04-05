if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from polars import DataFrame
from os import path, environ
import pyarrow as pa
import pyarrow.parquet as pq

@data_exporter
def export_data(df, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    bucket_name = environ.get('GCS_BUCKET_NAME')
    where = f'{bucket_name}/matches/matches.parquet'

    table = df.to_arrow()

    gcs = pa.fs.GcsFileSystem()

    pq.write_table(
        table,
        where=where,
        filesystem=gcs,
        # existing_data_behavior='delete_matching',
    )    


