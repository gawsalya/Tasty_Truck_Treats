'''libraries needed to create the main script for ETL'''
import glob
import csv
import sys
from os import environ
from datetime import datetime
from dotenv import load_dotenv

from functions_for_etl import load_s3, load_correct_bucket, create_directory, latest_file_name, download_truck_files, combine_transaction_data_files, remove_invalid_data, check_card_type_correct, change_your_data_format, convert_to_csv, delete_directory, get_db_connection, upload_date, upload_transaction_data

if __name__ == "__main__":

    load_dotenv()
    config = environ

    data_source = load_s3(config)
    DATA = config["BUCKET_NAME"]
    TRUCK_FILE = config["TRUCK_FOLDER"]
    FOLDER = latest_file_name(TRUCK_FILE)

    files = load_correct_bucket(data_source, DATA, FOLDER)

    create_directory(TRUCK_FILE)
    for file in files:
        download_truck_files(data_source, DATA, file, TRUCK_FILE)

    if len(files) == 0:
        delete_directory(TRUCK_FILE)
        print("No data to download")
        sys.exit(0)

    files = glob.glob(f'{TRUCK_FILE}/*.csv')
    for file in files:
        truck_dataframe = combine_transaction_data_files(files)

    df = remove_invalid_data(truck_dataframe)
    truck_dataframe = check_card_type_correct(df)
    df = change_your_data_format(truck_dataframe)

    convert_to_csv(df)
    delete_directory(TRUCK_FILE)

    conn = get_db_connection(config)
    with open('combined.csv', 'r', encoding="utf-8") as transactions:
        reader = csv.reader(transactions)
        next(reader)

        for line in reader:
            if isinstance(line[1], str):
                line[1] = datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S")
            upload_date(conn, line[1])
            upload_transaction_data(conn, line)
