from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from polars import DataFrame
from os import path, environ
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    bucket_name = environ.get('GCS_BUCKET_NAME')
    table_name = 'products'
    root_path = f'{bucket_name}/{table_name}'

    table = df.to_arrow()

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['source','input_date'],
        #use_deprecated_int96_timestamps=True,
        filesystem=gcs,
        existing_data_behavior='delete_matching',
    )    
