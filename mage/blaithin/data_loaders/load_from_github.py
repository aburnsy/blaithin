if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
import os
import shutil
from dateutil import rrule
from datetime import datetime

BASE_URL = 'https://github.com/aburnsy/blaithin_files/raw/main/data'

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    site = kwargs['site']

    try:
        os.mkdir(site)
    except FileExistsError:
        shutil.rmtree(site)
        os.mkdir(site)

    try:
        kwargs['load_all_flag']
        file_dates = [dt.strftime('%Y-%m-%d') for dt in rrule.rrule(rrule.DAILY, dtstart=datetime(2024, 3, 26), until=datetime.now())]
    except KeyError:
        file_dates = [kwargs['execution_date'].strftime('%Y-%m-%d')]

    print(f'loading files for dates [{file_dates}] from site: {site}')

    for file_date in file_dates:
        parquet_url = f'{BASE_URL}/{site}/{file_date}.parquet'
        base_file = f"{site}/{file_date}.parquet"
        if not os.system(f"curl -sfLo/dev/null -r0-0 {parquet_url}"):
            os.system(f"curl -L {parquet_url} --Output {base_file}")
        else:
            print(f"File does not exist at {parquet_url}")
    
    df = pl.read_parquet(f"{site}/*")

    shutil.rmtree(site)
    return df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
