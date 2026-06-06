import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download

DATASET_ID = "Vincentran/careerviet-accounting-jobs"

@st.cache_data
def load_data():
    file_path = hf_hub_download(
        repo_id=DATASET_ID,
        filename="jobs.parquet",
        repo_type="dataset"
    )

    df = pd.read_parquet(file_path)
    return df


df = load_data()

st.title("CareerViet Job Dashboard (Parquet)")

st.metric("Total Jobs", len(df))

st.dataframe(df)

# FILTERS
st.sidebar.header("Filters")

company = st.sidebar.selectbox(
    "Company",
    sorted(df["company"].unique())
)

filtered = df[df["company"] == company]

st.subheader(f"Jobs at {company}")
st.dataframe(filtered)