"""Parsing function to extract the data from the raw data files."""
import numpy as np
import pandas as pd
import json



def extract_value_json_str(json_str, key):
    """Extract a value from a JSON string.
    
    Args:
        json_str (str): JSON string to extract a dictionary from.
        key (str): key to extract from the dictionary.
    """
    json_dict = _convert_json_str_to_dict(json_str)

    # extract values form dictionary
    extracted_value = json_dict.get(key, np.nan)
    return extracted_value


def extract_all_values_json_str(json_str):
    """Convert all values in JSON string to a pandas Series.

    Args:
        json_str (str): JSON string to convert to a pandas Series.
    """
    json_dict = _convert_json_str_to_dict(json_str)

    # convert dictionary to pandas Series
    series = pd.Series(json_dict)
    return series


def extract_all_values_column(df, column, unpack_lists=True, prefix=None, suffix=None):
    """Extract all values from a column containing JSON strings.

    Args:
        df (pd.DataFrame): DataFrame containing the column to extract values from.
        column (str): Column name containing JSON strings.
        unpack_lists (bool): Unpack lists into separate columns
        prefix (str): Prefix to add to the column names.
        suffix (str): Suffix to add to the column names.
    """
    df_extracted = df[column].apply(extract_all_values_json_str)

    # unpack columns which has value that contains a list into separate columns
    if unpack_lists:
        for col in df_extracted.columns:
            if df_extracted[col].apply(lambda x: isinstance(x, list)).any():
                df_extracted = df_extracted.join(unpack_series_with_lists(df_extracted, col))
                df_extracted.drop(columns=col, inplace=True)

    # add prefix and/or suffix to column names
    if prefix:
        df_extracted.columns = [f"{prefix}_{col}" for col in df_extracted.columns]
    if suffix:
        df_extracted.columns = [f"{col}_{suffix}" for col in df_extracted.columns]

    return df_extracted


def _convert_json_str_to_dict(json_str):
    """Convert JSON string to a dictionary."""

    # check if string is not empty
    if pd.isnull(json_str):
        return {}

    # load json string to dictionary
    json_dict = json.loads(json_str)

    # check if dictionary is a list, then get the first element
    if isinstance(json_dict, list):
        json_dict = json_dict[0]
        assert isinstance(json_dict, dict), f"Expected a dictionary but got {type(json_dict)}"
    return json_dict


def unpack_dict_with_lists(dict_with_lists):
    """Unpack dictionary containing lists into separate keys."""
    dict_out = dict_with_lists.copy()

    unpacked_dict = {}
    remove_keys = []

    # iterate over dictionary and unpack lists
    for key, value in dict_out.items():
        if isinstance(value, list):
            for i, item in enumerate(value):
                unpacked_dict[f"{key}_{i}"] = item
            remove_keys.append(key)

    # update dictionary with unpacked keys and values
    dict_out.update(unpacked_dict)

    # remove keys that were unpacked
    for key in remove_keys:
        dict_out.pop(key)
    return dict_out


def unpack_series_with_lists(df, column):
    """Unpack pd.Series column containing lists into Dataframe with separate columns."""
    unpacked = df[column].apply(pd.Series)
    unpacked.rename(columns=lambda x: f'{column}_{x}', inplace=True)
    return unpacked
