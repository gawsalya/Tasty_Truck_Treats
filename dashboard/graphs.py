"""
libraries to create graphs
"""
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os import environ

from graph_func import get_db_connection, key_stats, sales_per_truck, sales_per_day, type_of_transaction
if __name__ == "__main__":

    load_dotenv()
    config = environ
    conn = get_db_connection(config)

    cursor = conn.cursor()
    cursor.execute(
        '''SELECT sigma_gawsalya_schema.fact_truck_transaction.truck_id, 
        sigma_gawsalya_schema.fact_truck_transaction.cost AS total, 
        sigma_gawsalya_schema.fact_truck_transaction.f_time AS timestamp, 
        sigma_gawsalya_schema.dim_type.payment_type AS type 
        FROM sigma_gawsalya_schema.fact_truck_transaction
        JOIN sigma_gawsalya_schema.dim_type ON sigma_gawsalya_schema.dim_type.type_id = 
        sigma_gawsalya_schema.fact_truck_transaction.type_id;''')
    result: pd.DataFrame = cursor.fetch_dataframe()
    df = result

    st.title("Dashboard for food truck data")
    st.markdown(
        "_Graphs analysing relationships between data from trucks_")

    key_stats(df)

    selected_day = st.sidebar.multiselect(
        "Day", options=df["timestamp"].dt.day.unique())

    sales_per_truck(df, selected_day)
    sales_per_day(df)
    type_of_transaction(df, selected_day)
