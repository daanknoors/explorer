"""Preprocess raw data"""
import pandas as pd

from explorer import config
from explorer.preprocessing.parse import extract_value_json_str

def preprocess_places_data():
    """Preprocess places data from Overture"""
    df_places = pd.read_csv(config.DATA_DIR / 'raw/places.csv')

    # extract nested JSON string



    df_places.head()
    print("Preprocessing places data")

if __name__ == '__main__':
    preprocess_places_data()