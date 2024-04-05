import io
import pandas as pd
import requests
from pandas import DataFrame


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    url = 'https://raw.githubusercontent.com/mage-ai/datasets/master/restaurant_user_transactions.csv'

    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text), sep=',')
    df.columns = ['_'.join(col.split(' ')) for col in df.columns]
    return df
