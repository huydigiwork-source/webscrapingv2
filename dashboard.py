import os
import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download

# =========================
# CONFIG (FIXED - USE YOUR DATASET)
# =========================
HF_DATASET_ID = "Vincentran/careerviet-accounting-jobs"
HF_TOKEN = os.getenv("HF_TOKEN")

FILE_NAME = "jobs.parquet"   # nếu lỗi thì đổi thành "data/jobs.parquet"


# =========================
# LOAD DATA FROM HF
# =========================
@st.cache_data
def load_data():

    try:
        # Try root file first
        try:
            file_path = hf_hub_download(
                repo_id=HF_DATASET_ID,
                filename="jobs.parquet",
                repo_type="dataset",
                token=HF_TOKEN
            )
        except:
            # fallback (rất quan trọng)
            file_path = hf_hub_download(
                repo_id=HF_DATASET_ID,
                filename="data/jobs.parquet",
                repo_type="dataset",
                token=HF_TOKEN
            )

        df = pd.read_parquet(file_path)
        return df

    except Exception as e:
        st.error(f"❌ Failed to load HF dataset: {e}")
        return pd.DataFrame()


df = load_data()

st.title("🤖 AI Job Dashboard (HF LIVE)")

if df.empty:
    st.warning("Dataset empty or not loaded")
    st.stop()

st.dataframe(df, use_container_width=True)