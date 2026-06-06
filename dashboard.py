import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Job Dashboard", layout="wide")

st.title("🚀 Job Intelligence Dashboard")


def load():
    paths = [
        "data/jobs.parquet",
        "jobs.parquet"
    ]

    for p in paths:
        if os.path.exists(p):
            return pd.read_parquet(p)

    raise FileNotFoundError("jobs.parquet not found")


df = load()

st.metric("Jobs", len(df))
st.dataframe(df)