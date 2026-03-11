import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hurricane Maris Relief Operations Dashboard")

infra = pd.read_csv("isla_coralina_infrastructure.csv")
relief = pd.read_csv("isla_coralina_relief_operations.csv")

tab1, tab2 = st.tabs(["Infrastructure Status", "Relief Distribution"])

with tab1:
    st.header("Infrastructure Status")

with tab2:
    st.header("Relief Distribution Performance")
