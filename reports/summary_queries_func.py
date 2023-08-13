import json
from redshift_connector import connect, Connection
from datetime import datetime


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


def total_transaction_val_of_all_trucks(conn: Connection) -> int:
    '''sql query to find the total transaction value of all trucks'''
    with conn.cursor() as cur:
        cur.execute("""SELECT SUM(cost) AS total FROM sigma_gawsalya_schema.fact_truck_transaction 
                    WHERE f_time BETWEEN 'yesterday' and 'today';""")
        total = cur.fetchone()[0]
        cur.close()
        return total


def total_and_count_by_truck_id(conn: Connection) -> list[list]:
    '''sql query to find the number of transactions and total cost by each truck'''
    with conn.cursor() as cur:
        cur.execute("""SELECT truck_id, COUNT(*), SUM(cost) FROM sigma_gawsalya_schema.fact_truck_transaction 
                    WHERE f_time BETWEEN 'yesterday' and 'today'
                GROUP BY truck_id ORDER BY truck_id ASC;""")
        all_data = cur.fetchall()
        cur.close()
        return all_data


def find_median_and_avg_cost(conn: Connection) -> list[list]:
    '''sql query to find the median and avg cost per truck'''
    with conn.cursor() as cur:
        cur.execute("""SELECT truck_id, MEDIAN(cost), AVG(cost) 
                    FROM sigma_gawsalya_schema.fact_truck_transaction 
                    WHERE f_time BETWEEN 'yesterday' and 'today'
                    GROUP BY truck_id ORDER BY truck_id ASC;""")

        median_avg = cur.fetchall()
        cur.close()
        return median_avg


def format_data_into_dict(data: list[list], json_data: dict) -> dict:
    '''function to format database data into json format'''
    for truck in data:
        truck_dict = {}
        truck_dict['truck_id'] = truck[0]
        truck_dict['transaction_in_day'] = truck[1]
        truck_dict['total_revenue'] = round(truck[2], 2)
        json_data['trucks'].append(truck_dict)

    return json_data


def modify_data_in_dict(data: list[list], json_data: dict) -> dict:
    '''function to modify existing dictionary'''

    for truck in json_data['trucks']:
        for truck_truck in data:
            if truck['truck_id'] == truck_truck[0]:
                truck['median_transaction_value'] = round(truck_truck[1], 2)
                truck['average_transaction_value'] = round(truck_truck[2], 2)

    return json_data


def format_as_html(data: dict) -> str:
    body = f'<h1 style="color:IndianRed">Tasty Truck Treats</h1> <h3 style="color:IndianRed">Total Truck Transaction  £{data["total_revenue"]}</h3>'
    for truck in data['trucks']:
        data_to_add = f'<h3 style="color:IndianRed" >Truck ID: {truck["truck_id"]} </h3><ul><li style="color:LightCoral">Transaction in a day: £{truck["transaction_in_day"]} <li style="color:LightCoral">Total revenue: £{truck["total_revenue"]} <li style="color:LightCoral"">Median Transactional Value: £{truck["median_transaction_value"]} <li style="color:LightCoral">Average Transaction Value: £{truck["average_transaction_value"]} </ul>'
        body += data_to_add
    return body


def export_as_json(date: datetime, data: dict):
    with open(f"report_data_{date}.json", "w") as f_obj:
        json.dump(data, f_obj)


def create_html_file(data: str):
    start = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Trucks Data</title>
    </head>
    <body>'''

    end = '''</body>
    </html>'''

    return start + data + end


def export_as_html(date: datetime, data: str):
    with open(f"report_data_{date.today()}.html", "w") as f_obj:
        f_obj.write(data)
        f_obj.close()
