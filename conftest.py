import pytest
import pandas as pd


@pytest.fixture
def fake_bucket_name():
    return 'fake_bucket'


@pytest.fixture
def fake_obj_key():
    return 'fake_file_name'


@pytest.fixture
def fake_list_of_files():
    return ['fake_1', 'fake_2']


@pytest.fixture
def fake_filename():
    return 'fake'


@pytest.fixture
def fake_truck_id():
    return 'truck_data_3.parquet'


@pytest.fixture
def fake_truck_id_2():
    return 32546


@pytest.fixture
def fake_dataframe():
    data = {
        "timestamp": ['2023-07-21 11:20:00', '2023-07-21 11:20:00', '2023-07-21 11:20:00', '2023-07-21 11:20:00', '2023-07-21 11:20:00'],
        "type": ['card', 'cash', 'card', 'fake', 'cash'],
        "total": [7.99, 'ERR', 2.50, 4.00, 5.00],
        "truck_id": [1, 2, 3, 4, 5]
    }
    return pd.DataFrame(data)
