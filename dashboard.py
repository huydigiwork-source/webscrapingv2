import streamlit as st
import pandas as pd
import os
from huggingface_hub import hf_hub_download

# =========================
# HF CONFIG
# =========================
HF_DATASET_ID = os.getenv("HF_DATASET_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

FILE_NAME = "jobs.parquet"
LOCAL_CACHE = "cache_jobs.parquet"

# =========================
# LOAD DATA FROM HF
# =========================
@st.cache_data
def load_data():

    try:
        # Download latest file from HF Dataset
        file_path = hf_hub_download(
            repo_id=HF_DATASET_ID,
            filename=FILE_NAME,
            repo_type="dataset",
            token=HF_TOKEN
        )

        # Read parquet
        df = pd.read_parquet(file_path)

        return df

    except Exception as e:
        st.error(f"Failed to load data from HF: {e}")

        # fallback local
        if os.path.exists(LOCAL_CACHE):
            return pd.read_parquet(LOCAL_CACHE)

        return pd.DataFrame()


df = load_data()

# =========================
# UI
# =========================
st.title("🤖 AI Job Intelligence Dashboard (LIVE HF DATA)")

if df.empty:
    st.warning("No data available")
    st.stop()

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))

if "company" in df:
    col2.metric("Companies", df["company"].nunique())

if "location" in df:
    col3.metric("Locations", df["location"].nunique())

st.divider()

# =========================
# SEARCH
# =========================
keyword = st.text_input("🔎 Search Jobs")

if keyword:
    df = df[df["title"].str.contains(keyword, case=False, na=False)]

# =========================
# TABLE
# =========================
st.dataframe(df, use_container_width=True)

# =========================
# DEBUG INFO
# =========================
st.caption(f"Dataset loaded from HuggingFace: {HF_DATASET_ID}")