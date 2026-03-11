import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hurricane Maris Relief Operations Dashboard")

infra = pd.read_csv("isla_coralina_infrastructure.csv")
relief = pd.read_csv("isla_coralina_relief_operations.csv")

relief["fulfillment_rate"] = relief["quantity_delivered"] / relief["quantity_requested"]

# KPI calculations
total_population_served = relief["population_at_center"].sum()
avg_delay = relief["delivery_delay_hours"].mean()

low_fulfillment = (relief["fulfillment_rate"] < 0.8).mean() * 100

non_operational = infra[infra["operational_status"] == "Non-Operational"].shape[0]

tab1, tab2 = st.tabs(["Infrastructure Status", "Relief Distribution"])

with tab1:
    st.header("Infrastructure Status")

with tab2:
    st.header("Relief Distribution Performance")
