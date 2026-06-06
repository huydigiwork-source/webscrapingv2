import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download

DATASET_ID = "Vincentran/careerviet-accounting-jobs"

st.set_page_config(
    page_title="Job Intelligence Dashboard",
    layout="wide"
)

@st.cache_data(ttl=300)
def load_data():

    parquet_file = hf_hub_download(
        repo_id=DATASET_ID,
        filename="jobs.parquet",
        repo_type="dataset"
    )

    return pd.read_parquet(parquet_file)

df = load_data()

st.title("🚀 CareerViet Accounting Jobs Intelligence")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Jobs", len(df))

with col2:
    st.metric("Columns", len(df.columns))

st.dataframe(
    df,
    use_container_width=True
)