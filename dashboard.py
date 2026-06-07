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

# ==================================================
# SAFE COLUMNS
# ==================================================

for col in ["title", "company", "location"]:
    if col not in df.columns:
        df[col] = ""

# ==================================================
# HERO
# ==================================================

st.markdown("""
<div class="hero">
    <h1>Workforce Intelligence Dashboard</h1>
    <p>Interactive Labor Market Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# FILTERS
# ==================================================

with st.sidebar:

    st.header("Filters")

    search = st.text_input(
        "Search Job"
    )

    locations = ["All"] + sorted(
        df["location"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    companies = ["All"] + sorted(
        df["company"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
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
# FILTER ENGINE
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
        filtered["location"] == location
    ]

if company != "All":

    filtered = filtered[
        filtered["company"] == company
    ]

# ==================================================
# KPI
# ==================================================

coverage = round(
    len(filtered) / len(df) * 100,
    1
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Jobs",
        f"{len(filtered):,}"
    )

with c2:
    st.metric(
        "Companies",
        filtered["company"].nunique()
    )

with c3:
    st.metric(
        "Locations",
        filtered["location"].nunique()
    )

with c4:
    st.metric(
        "Coverage",
        f"{coverage}%"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# CHARTS
# ==================================================

left, right = st.columns(2)

with left:

    st.subheader("Top Companies")

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
        orientation="h",
        template="plotly_white"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top Locations")

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
        orientation="h",
        template="plotly_white"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# DISTRIBUTION
# ==================================================

st.subheader("Market Distribution")

col1, col2 = st.columns(2)

with col1:

    pie_data = (
        filtered["location"]
        .value_counts()
        .head(8)
    )

    fig = px.pie(
        names=pie_data.index,
        values=pie_data.values,
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    pie_data = (
        filtered["company"]
        .value_counts()
        .head(8)
    )

    fig = px.pie(
        names=pie_data.index,
        values=pie_data.values,
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# DATA EXPLORER
# ==================================================

st.subheader("Data Explorer")

st.dataframe(
    filtered.head(1000),
    use_container_width=True,
    height=500
)

st.caption(
    f"Showing {min(len(filtered),1000):,} / {len(filtered):,} rows"
)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Powered by Hugging Face • Plotly • Streamlit"
)