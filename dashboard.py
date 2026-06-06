import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Dashboard", layout="wide")

st.title("🚀 Job Intelligence Dashboard")

@st.cache_data
def load():
    return pd.read_parquet("jobs.parquet")

df = load()

st.sidebar.header("Filters")

platform = st.sidebar.multiselect("Platform", df["platform"].unique(), df["platform"].unique())
location = st.sidebar.multiselect("Location", df["location"].unique(), df["location"].unique())

df = df[(df["platform"].isin(platform)) & (df["location"].isin(location))]

st.metric("Jobs", len(df))

fig = px.bar(df["platform"].value_counts())
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)