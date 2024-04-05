from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
import polars as pl
from os import path, environ
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: pl.DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    bucket_name = environ.get('GCS_BUCKET_NAME')
    source = df.select(pl.first("source")).item()
    gcs = pa.fs.GcsFileSystem()

    input_dates = df.select('input_date').to_series(0).unique().to_list()
    for input_date in input_dates:  

        where = f'{bucket_name}/products/{source}/{input_date}'

        table = df.filter(pl.col('input_date') == input_date).to_arrow()

        pq.write_table(
            table,
            where=where,
            filesystem=gcs,
        )