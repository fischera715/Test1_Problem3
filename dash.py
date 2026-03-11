import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hurricane Maris Relief Operations Dashboard")

infra = pd.read_csv("isla_coralina_infrastructure.csv")
relief = pd.read_csv("isla_coralina_relief_operations.csv")

relief["date"] = pd.to_datetime(relief["date"])
relief["fulfillment_rate"] = relief["quantity_delivered"] / relief["quantity_requested"]

# KPI calculations
total_population_served = relief["population_at_center"].sum()
avg_delay = relief["delivery_delay_hours"].mean()

low_fulfillment = (relief["fulfillment_rate"] < 0.8).mean() * 100

non_operational = infra[infra["operational_status"] == "Non-Operational"].shape[0]

st.subheader("Operational Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Population Served", f"{total_population_served:,}")
col2.metric("Average Delivery Delay (hrs)", f"{avg_delay:.2f}")
col3.metric("% Deliveries < 80% Fulfillment", f"{low_fulfillment:.1f}%")
col4.metric("Non-Operational Facilities", non_operational)

tab1, tab2 = st.tabs(["Infrastructure Status", "Relief Distribution"])

st.sidebar.header("Filters")

municipality_filter = st.sidebar.multiselect(
    "Select Municipality",
    options=relief["municipality"].unique(),
    default=relief["municipality"].unique()
)

supply_filter = st.sidebar.multiselect(
    "Select Supply Type",
    options=relief["supply_type"].unique(),
    default=relief["supply_type"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[pd.to_datetime(relief["date"]).min(), pd.to_datetime(relief["date"]).max()]
)

filtered_relief = relief[
    (relief["municipality"].isin(municipality_filter)) &
    (relief["supply_type"].isin(supply_filter)) &
    (relief["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

with tab1:
    st.header("Infrastructure Status")

    status_counts = infra["operational_status"].value_counts()

    status_fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Infrastructure Operational Status"
    )
    
    st.plotly_chart(status_fig)

    infra_status_by_muni = infra.groupby(["municipality", "operational_status"]).size().reset_index(name="count")
    
    infra_fig = px.bar(
        infra_status_by_muni,
        x="municipality",
        y="count",
        color="operational_status",
        title="Infrastructure Status by Municipality"
    )
    
    st.plotly_chart(infra_fig)

with tab2:
    st.header("Relief Distribution Performance")

    fig = px.box(
        filtered_relief,
        x="transport_mode",
        y="delivery_delay_hours",
        title="Delivery Delays by Transport Mode"
    )

    st.plotly_chart(fig)

    gap_data = filtered_relief.groupby("municipality")[["quantity_requested","quantity_delivered"]].sum()
    
    gap_data["gap"] = gap_data["quantity_requested"] - gap_data["quantity_delivered"]
    
    gap_fig = px.bar(
        gap_data,
        y=gap_data.index,
        x="gap",
        orientation="h",
        title="Supply Gap by Municipality",
        labels={"gap": "Supply Shortage"}
    )    
    st.plotly_chart(gap_fig)
    daily_efficiency = filtered_relief.groupby("date")["fulfillment_rate"].mean().reset_index()
    
    time_fig = px.line(
        daily_efficiency,
        x="date",
        y="fulfillment_rate",
        title="Average Supply Fulfillment Rate Over Time"
    )
    
    st.plotly_chart(time_fig)







