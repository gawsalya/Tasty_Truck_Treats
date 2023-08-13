'''libraries I will be using for testing'''
import os
from unittest.mock import MagicMock, patch, mock_open
import pytest

from functions_for_etl import load_correct_bucket, create_directory, download_truck_data_files, get_truck_id, create_tables, remove_invalid_data, check_card_type_correct, delete_directory


def test_load_correct_bucket_call_correctly(fake_bucket_name):
    '''function that tests functions are called appropriately'''
    folder = 'fake_folder'
    fake_storage = MagicMock()
    fake_storage.list_objects.return_value = {
        'Contents': [{'Key': 'fake_folder'}]}
    result = load_correct_bucket(fake_storage, fake_bucket_name, folder)

    assert result == ['fake_folder']
    assert fake_storage.list_objects.call_count == 1


def test_load_correct_bucket_call_returns_empty(fake_bucket_name):
    '''function that tests functions are called appropriately and if no matching folder returns empty list'''
    folder = 'does_not_exist'
    fake_storage = MagicMock()
    fake_storage.list_objects.return_value = {
        'Contents': [{'Key': 'fake_folder'}]}
    result = load_correct_bucket(fake_storage, fake_bucket_name, folder)

    assert not result
    assert fake_storage.list_objects.call_count == 1


def test_create_directory_works(fake_filename):
    '''check that directory is created'''
    assert os.path.isdir(fake_filename) is False
    create_directory(fake_filename)
    assert os.path.isdir(fake_filename) is True


def tests_download_file_from_bucket(fake_bucket_name, fake_obj_key):
    '''test to see if files are downloaded from s3'''
    fake_storage = MagicMock()
    fake_download = fake_storage.download_file

    download_truck_data_files(
        fake_storage, fake_bucket_name, fake_obj_key)

    assert fake_download.call_count == 1
    assert fake_download.called_with(
        fake_bucket_name, fake_obj_key, "fake_directory")


def test_truck_id_is_returned(fake_truck_id):
    '''checks that a number is returned for truck id'''
    result = get_truck_id(fake_truck_id)

    assert result == 3


def test_truck_id_error(fake_truck_id_2):
    '''checks that error is raised with a string'''
    with pytest.raises(TypeError) as err:
        get_truck_id(fake_truck_id_2)

    assert str(err.value) == 'Filename must be a str'


def test_invalid_total_data_is_removed(fake_dataframe):
    '''test to check invalid data is removed from the dataframe'''
    assert 'ERR' in fake_dataframe.total.unique()
    result = remove_invalid_data(fake_dataframe)

    assert 'ERR' not in result.total.unique()


def test_card_type_is_checked(fake_dataframe):
    '''test to check invalid type is removed from the dataframe'''
    assert 'fake' in fake_dataframe.type.unique()
    result = check_card_type_correct(fake_dataframe)

    assert 'fake' not in result.type.unique()


def check_directory_deleted(fake_filename):
    assert os.path.isdir(fake_filename) is True
    delete_directory(fake_filename)
    assert os.path.isdir(fake_filename) is False


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_create_tables(mock_file):
    '''test that the create tables function is running'''

    fake_conn = MagicMock()
    fake_execute = fake_conn.cursor().__enter__().execute

    create_tables(fake_conn, 'schema.sql')

    assert fake_execute.call_count == 1
    assert open("path/to/open").read() == "data"
    mock_file.assert_called_with("path/to/open")
