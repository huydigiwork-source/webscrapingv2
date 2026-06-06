import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import os

DATASET_ID = os.getenv("HF_DATASET_ID")

st.set_page_config(
    page_title="Job Intelligence Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():

    file = hf_hub_download(
        repo_id=DATASET_ID,
        filename="jobs.parquet",
        repo_type="dataset"
    )

    return pd.read_parquet(file)

df = load_data()

st.title("🚀 Job Intelligence Dashboard")

st.metric("Jobs", len(df))

st.dataframe(
    df,
    use_container_width=True
)