'''libraries required to create a report'''
from dotenv import load_dotenv
from os import environ

from summary_queries_func import get_db_connection, total_transaction_val_of_all_trucks, total_and_count_by_truck_id, find_median_and_avg_cost, format_data_into_dict, modify_data_in_dict, create_html_file, format_as_html


def handler(event=None, context=None):

    load_dotenv()
    config = environ

    conn = get_db_connection(config)
    truck_info = {'trucks': []}

    total = total_transaction_val_of_all_trucks(conn)
    total_transaction_value = 0.00
    if total != None:
        total_transaction_value = round(total, 2)

    truck_info['total_revenue'] = total_transaction_value

    truck_information_per_id = total_and_count_by_truck_id(conn)
    truck_updated = format_data_into_dict(truck_information_per_id, truck_info)
    median_avg = find_median_and_avg_cost(conn)
    trucks_info = modify_data_in_dict(median_avg, truck_updated)

    body_data = format_as_html(trucks_info)
    html_data = create_html_file(body_data)

    return {"html_info": html_data}


if __name__ == "__main__":

    handler()
