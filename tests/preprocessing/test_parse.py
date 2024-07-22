import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal
import pytest

from explorer.preprocessing.parse import extract_value_json_str, extract_all_values_json_str

@pytest.fixture()
def data_jsonstr():
    data = pd.DataFrame({
        'nested_jsonstr': ['[{"id": 1, "name": "category1"}]', '[{"id": 2, "name": "category2"}]', np.nan],
        'jsonstr': ['{"meta": "data", "id": 1}', '{"meta": "data2", "id": 2}', np.nan],
        'jsonstr_lists': ['{"meta": "data", "id": 1, "selected_options": ["a", "b"]}', '{"meta": "data2", "id": 2, "selected_options": ["a", "c"]}', np.nan]

    })

    return data

def test_extract_value_json_str(data_jsonstr):
    data = (
        data_jsonstr
        .assign(nested_jsonstr_id=data_jsonstr['nested_jsonstr'].apply(lambda x: extract_value_json_str(x, key='id')))
        .assign(nested_jsonstr_name=data_jsonstr['nested_jsonstr'].apply(lambda x: extract_value_json_str(x, key='name')))
        .assign(jsonstr_meta=data_jsonstr['jsonstr'].apply(lambda x: extract_value_json_str(x, key='meta')))
    )

    assert np.array_equal(data['nested_jsonstr_id'].values, [1.0, 2.0, np.nan], equal_nan=True)
    # with columns of object type and nan values, we need to use assert_series_equal
    assert_series_equal(data['nested_jsonstr_name'], pd.Series(['category1', 'category2', np.nan], name='nested_jsonstr_name'))
    assert_series_equal(data['jsonstr_meta'], pd.Series(['data', 'data2', np.nan], name='jsonstr_meta'))


def test_extract_all_values_json_str(data_jsonstr):
    df_extracted = data_jsonstr['nested_jsonstr'].apply(extract_all_values_json_str)
    df_expected = pd.DataFrame({
        'id': [1, 2, np.nan],
        'name': ['category1', 'category2', np.nan]
    })
    assert_frame_equal(df_extracted, df_expected, check_dtype=False)

    # check nested list
    df_extracted = data_jsonstr['jsonstr_lists'].apply(extract_all_values_json_str)
    df_expected = pd.DataFrame({
        'meta': ['data', 'data2', np.nan],
        'id': [1, 2, np.nan],
        'selected_options_0': ['a', 'a', np.nan],
        'selected_options_1': ['b', 'c', np.nan]
    })
    assert_frame_equal(df_extracted, df_expected, check_dtype=False)
