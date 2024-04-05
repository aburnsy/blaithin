if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
import os
import shutil


BASE_URL = 'https://github.com/aburnsy/blaithin_files/raw/main/data'

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    try:
        os.mkdir('rhs')
    except FileExistsError:
        shutil.rmtree('rhs')
        os.mkdir('rhs')


    parquet_url = f'{BASE_URL}/rhs.parquet'
    base_file = f"rhs/rhs.parquet"
    if not os.system(f"curl -sfLo/dev/null -r0-0 {parquet_url}"):
        os.system(f"curl -L {parquet_url} --Output {base_file}")
    else:
        print(f"File does not exist at {parquet_url}")
    
    df = pl.read_parquet(base_file)

    shutil.rmtree('rhs')
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
