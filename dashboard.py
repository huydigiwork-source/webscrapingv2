import streamlit as st
import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Workforce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# LOAD CSS
# ==================================================

css_file = Path("style.css")

if css_file.exists():
    with open(css_file, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==================================================
# CONFIG
# ==================================================

HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

# ==================================================
# DATA
# ==================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_data():

    file_path = hf_hub_download(
        repo_id=HF_DATASET_ID,
        filename=FILE_NAME,
        repo_type="dataset"
    )

    return pd.read_parquet(file_path)

df = load_data()

if df.empty:
    st.error("Dataset is empty")
    st.stop()