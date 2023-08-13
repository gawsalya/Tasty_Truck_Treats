'''libraries needed for function creation'''
import os
import shutil
from datetime import datetime
from boto3 import client
from botocore.client import BaseClient
import pandas as pd
from pytz import timezone
from redshift_connector import connect, Connection


def load_s3(configuration):
    '''function using access information to connect to client and load'''
    s3_data = client("s3", aws_access_key_id=configuration["ACCESS_KEY_ID"],
                     aws_secret_access_key=configuration["SECRET_ACCESS_KEY"])
    return s3_data


def load_correct_bucket(storage: BaseClient, bucket, folder: str) -> list:
    '''function to pull out correct bucket from S3'''
    file_names = []
    for file in storage.list_objects(Bucket=bucket)['Contents']:
        if folder in file["Key"]:
            file_names.append(file["Key"])

    return file_names


def create_directory(filename: str):
    '''creates a directory if it doesn't exist'''
    if not os.path.isdir(filename):
        os.mkdir(filename)
    else:
        raise ValueError("Directory already exists")


def latest_file_name(folder: str) -> str:
    '''get the latest filename to download '''
    date = datetime.now(tz=timezone('Europe/London'))
    month_year = str(date.year) + '-' + str(date.month)
    hour = date.hour
    day = int(date.day)
    download = 0
    if hour >= 12:
        download = 12
    if hour >= 15:
        download = 15
    if hour >= 18:
        download = 18
    if hour >= 21:
        download = 21
    print(f'{folder}/' + month_year + f'/{day}' + f'/{download}')
    return f'{folder}/' + month_year + f'/{day}' + f'/{download}'


def download_truck_files(storage: BaseClient, bucket, object_key: str, folder: str):
    '''downloads the relevant files from S3'''

    filename = object_key.split('-')
    save_name_as = filename[1][-12:]
    storage.download_file(bucket, object_key,
                          f'{folder}/' + save_name_as)


def combine_transaction_data_files(files: list[str]):
    """Loads and combines relevant files from the data/ folder.
    Produces a single combined file in the data/ folder."""

    df_files = []
    for file in files:
        df_temp = pd.read_csv(file)
        df_temp = df_temp.astype({'total': object})

        number = get_truck_id(file)
        df_temp['truck_id'] = number

        df_files.append(df_temp)

    merged_df = pd.merge(
        df_files[0], df_files[1], how="outer", on=["timestamp", "type", "total", "truck_id"])

    for file in range((len(df_files)) - 2):
        merged_df = pd.merge(
            merged_df, df_files[file + 2], how="outer", on=["timestamp", "type", "total", "truck_id"])

    return merged_df


def get_truck_id(filename: str):
    """Returns number in the filename"""
    if not isinstance(filename, str):
        raise TypeError('Filename must be a str')
    id_num = filename.split('_')[1]
    return [int(x) for x in id_num if x.isdigit()][0]


def remove_invalid_data(dataframe):
    '''removes invalid data from the data frame'''
    dataframe['total'] = pd.to_numeric(dataframe['total'], errors='coerce')
    dataframe = dataframe.dropna(subset=['total'])
    dataframe.loc[:, 'total'] = dataframe['total'].apply(
        lambda x: x if x <= 15.0 else 0.00)
    dataframe.loc[:, 'total'] = dataframe['total'].apply(
        lambda x: x if x > 0 else 0.00)
    dataframe = dataframe[~dataframe['total'].isin(
        [0.00])]

    return dataframe


def check_card_type_correct(dataframe):
    '''check that type is either card or cash'''
    dataframe = dataframe[dataframe['type'].isin(
        ["cash", "card"])]

    return dataframe


def change_your_data_format(dataframe):
    '''changes the format of the columns'''
    columns = {'total': float, 'truck_id': int}
    dataframe = dataframe.astype(columns)
    dataframe['timestamp'] = pd.to_datetime(
        dataframe['timestamp'], format="mixed")
    dataframe['timestamp'] = dataframe['timestamp'].dt.tz_localize(None)

    return dataframe


def convert_to_csv(dataframe):
    '''converts dataframe to csv'''
    dataframe = dataframe.reset_index(drop=True)
    dataframe.to_csv('combined.csv')


def delete_directory(filename: str):
    '''deletes directory if it exists'''
    if os.path.isdir(filename):
        shutil.rmtree(filename)


def get_db_connection(config):
    '''connect to redshift database'''
    try:
        return connect(
            user=config['DB_USER'],
            password=config['PASSWORD'],
            host=config['HOST'],
            port=config['PORT'],
            database=config["DB_NAME"])
    except ValueError:
        return "Error connecting to database."


def create_tables(conn: Connection, schema_name: str):
    '''function to create tables in database'''
    with open(schema_name, 'r', encoding='utf-8') as file:
        tables_query = file.read()
        with conn.cursor() as cur:
            rc_multi_command(cur, tables_query)
        conn.commit()
        cur.close()


def rc_multi_command(cursor, commands):
    '''function to split up SQL commands into individual ones'''
    command_split = commands.split(";")
    for command in command_split:
        if not len(command) == 0:
            cursor.execute(command + ';')
            print('command success')


def upload_date(conn: Connection, date_info):
    """Uploads date to the database."""
    day = date_info.strftime('%A')
    date_to_insert = date_info.date()
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO sigma_gawsalya_schema.dim_date(d_date, d_day)
              VALUES (%s, %s)''', [date_to_insert, day])
        conn.commit()
        cur.close()


def upload_transaction_data(conn: Connection, transaction: list):
    """Uploads transaction data to the database."""
    with conn.cursor() as cur:
        cur.execute("""SELECT type_id FROM sigma_gawsalya_schema.dim_type
                    WHERE payment_type = %s""", [
                    transaction[2]])
        type_id = cur.fetchone()[0]
        cur.execute("""SELECT date_id FROM sigma_gawsalya_schema.dim_date
                    WHERE d_date = %s""", [
                    transaction[1].date()])
        date_id = cur.fetchone()[0]
        cur.execute(
            '''INSERT INTO sigma_gawsalya_schema.fact_truck_transaction
            (truck_id, type_id, date_id, cost, f_time) 
            VALUES (%s, %s, %s, %s, %s)''',
            [transaction[4], type_id, date_id, transaction[3], transaction[1]])
        conn.commit()
        cur.close()
