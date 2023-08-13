'''libraries for my functions'''
import streamlit as st
import altair as alt
from datetime import datetime
from redshift_connector import connect


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


def key_stats(dataframe):
    '''function to display key statistics'''
    currentMonth = datetime.now().month
    current_total = dataframe[dataframe['timestamp'].dt.month == currentMonth]['total'].sum(
    )
    last_month = dataframe[dataframe['timestamp'].dt.month == (
        currentMonth - 1)]['total'].sum()
    delta = (current_total - last_month)/last_month * 100

    st.subheader("Key Statistics")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Total trucks", dataframe['truck_id'].nunique())
    with cols[1]:
        st.metric("Number of transactions", dataframe.shape[0])
    with cols[2]:
        st.metric("Revenue", f"£ {current_total.round(2)}", delta)


def sales_per_truck(dataframe, selected_day):
    '''graph to show sales per truck'''
    data = dataframe

    if len(selected_day) != 0:
        data = dataframe[(dataframe["timestamp"].dt.day).isin(selected_day)]

    ordered_data = data.groupby(['truck_id']).sum('total')
    table = ordered_data.reset_index()

    chart = (
        alt.Chart(
            data=table,
            title="Graph showing total revenue per truck",
        )
        .mark_bar(size=20, color='pink')
        .encode(
            x=alt.X("truck_id", axis=alt.Axis(
                title="Truck Id", format='.0f')),
            y=alt.Y("total", axis=alt.Axis(
                title="Total Revenue, £")),

        )
        .properties(
            width=300,
        )
    )

    st.altair_chart(chart)


def sales_per_day(dataframe):
    '''graph to show sales per day'''
    current_total = dataframe.groupby(
        dataframe['timestamp'].dt.day)['total'].sum()
    data = current_total.reset_index()

    chart = (
        alt.Chart(
            data=data,
            title="Line chart showing sales per day",
        )
        .mark_line(size=5)
        .encode(
            x=alt.X("timestamp", axis=alt.Axis(
                title="Day in August", format='.0f')),
            y=alt.Y("total", axis=alt.Axis(
                title="Total Revenue, £")),
            color=alt.value('pink')
        )
        .properties(
            width=300,
        )
    )

    st.altair_chart(chart)


def type_of_transaction(dataframe, selected_day):
    '''pie chart showing types of transaction'''
    cols = st.columns(2)

    with cols[0]:
        data = dataframe

        if len(selected_day) != 0:
            data = dataframe[(
                dataframe["timestamp"].dt.day).isin(selected_day)]

        transaction = data.groupby(['type']).count()
        type_table = transaction.reset_index()

        domain = ['cash', 'card']
        colour_range = ['lightpink', 'bisque']
        chart = (
            alt.Chart(
                data=type_table,
                title="Pie chart showing proportion of cash/card sales",
            )
            .mark_arc(size=5)
            .encode(
                theta='total',
                color=alt.Color('type').scale(
                    domain=domain, range=colour_range)
            )
            .properties(
                width=300,
            )
        )

    st.altair_chart(chart)
