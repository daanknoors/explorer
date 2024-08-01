"""Preprocess raw data"""
import pandas as pd

from explorer import config
from explorer.preprocessing import parse

JSON_COLUMNS = ['sources', 'names', 'categories', 'addresses']


def preprocess_places_data(df_places, save_path=None):
    """Preprocess places data from Overture"""
    df = df_places.copy()

    # extract info JSON string columns and separate them into separate columns
    for col in JSON_COLUMNS:
        if col not in df.columns:
            continue
        df_extracted = parse.extract_all_values_column(df, col, unpack_lists=True, prefix=col)
        df = df.join(df_extracted)
        df.drop(columns=col, inplace=True)

    if save_path:
        df.to_csv(save_path, index=False)

    return df





    df_places.head()
    print("Preprocessing places data")

if __name__ == '__main__':
    preprocess_places_data()