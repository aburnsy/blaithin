if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
from urllib.parse import urlparse
import os

BASE_URL = 'https://github.com/aburnsy/blaithin_files/tree/main/data'

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # date_format = kwargs['plant_type']
    site = 'arboretum' 
    # //kwargs['site'] or 
    file_date = "2024-03-27"

    parquet_url = f'https://github.com/aburnsy/blaithin_files/blob/main/data/{site}/{file_date}.parquet'
    base_file = f"/files/{site}/{file_date}.parquet"
    os.system(f"curl -L0 {parquet_url} --Output /{file_date}{site}.parquet")
    path = urlparse(parquet_url).path
    parquet_file_path = f"./{os.path.basename(path)}"
    print(f"{path}")
    print(parquet_file_path)
    df = pl.read_parquet(base_file)
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
