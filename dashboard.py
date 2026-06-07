import os
import streamlit as st
import pandas as pd

from pathlib import Path

from huggingface_hub import (
    hf_hub_download,
    HfApi
)

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
# HF CONFIG
# ==================================================

HF_TOKEN = os.getenv("HF_TOKEN")

HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

api = HfApi(
    token=HF_TOKEN
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
# DATA LOADER
# ==================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data():

    file_path = hf_hub_download(
        repo_id=HF_DATASET_ID,
        filename=FILE_NAME,
        repo_type="dataset",
        token=HF_TOKEN
    )

    return pd.read_parquet(
        file_path
    )

# ==================================================
# LOAD DATA
# ==================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Failed to load dataset: {e}"
    )

    st.stop()

if df.empty:

    st.warning(
        "Dataset is empty."
    )

    st.stop()

# ==================================================
# SAFE COLUMNS
# ==================================================

for col in [
    "title",
    "company",
    "location"
]:
    if col not in df.columns:
        df[col] = ""

# ==================================================
# HEADER
# ==================================================

st.title(
    "📊 Workforce Intelligence Dashboard"
)

st.caption(
    "Powered by Hugging Face Dataset"
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header(
        "Filters"
    )

    search = st.text_input(
        "Search Jobs"
    )

    locations = (
        ["All"]
        +
        sorted(
            df["location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    companies = (
        ["All"]
        +
        sorted(
            df["company"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    location = st.selectbox(
        "Location",
        locations
    )

    company = st.selectbox(
        "Company",
        companies
    )

# ==================================================
# FILTER
# ==================================================

filtered = df.copy()

if search:

    filtered = filtered[
        filtered["title"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if location != "All":

    filtered = filtered[
        filtered["location"]
        == location
    ]

if company != "All":

    filtered = filtered[
        filtered["company"]
        == company
    ]

# ==================================================
# KPI
# ==================================================

coverage = round(
    len(filtered)
    / len(df)
    * 100,
    1
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Jobs",
    f"{len(filtered):,}"
)

c2.metric(
    "Companies",
    filtered["company"].nunique()
)

c3.metric(
    "Locations",
    filtered["location"].nunique()
)

c4.metric(
    "Coverage",
    f"{coverage}%"
)

st.divider()

# ==================================================
# TOP COMPANIES
# ==================================================

left, right = st.columns(2)

with left:

    st.subheader(
        "Top Companies"
    )

    company_data = (
        filtered["company"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    company_data.columns = [
        "Company",
        "Jobs"
    ]

    fig = px.bar(
        company_data,
        x="Jobs",
        y="Company",
        orientation="h"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader(
        "Top Locations"
    )

    location_data = (
        filtered["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    location_data.columns = [
        "Location",
        "Jobs"
    ]

    fig = px.bar(
        location_data,
        x="Jobs",
        y="Location",
        orientation="h"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TABLE
# ==================================================

st.subheader(
    "Data Explorer"
)

st.dataframe(
    filtered.head(1000),
    use_container_width=True
)

# ==================================================
# STATUS
# ==================================================

with st.expander(
    "System Status"
):

    st.write(
        "HF Token Loaded:",
        bool(HF_TOKEN)
    )

    st.write(
        "Dataset:",
        HF_DATASET_ID
    )

    st.write(
        "Rows:",
        len(df)
    )

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "Hugging Face • Streamlit • Plotly"
)