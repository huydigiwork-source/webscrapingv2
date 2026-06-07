import streamlit as st
import pandas as pd
import numpy as np

from huggingface_hub import hf_hub_download

import plotly.express as px

from streamlit_option_menu import option_menu
from st_aggrid import AgGrid

from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ==================================================
# CONFIG
# ==================================================

HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

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
# CSS
# ==================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

div[data-testid="stMetric"]{
    background:#111827;
    border-radius:12px;
    padding:12px;
    border:1px solid #1f2937;
}

[data-testid="stSidebar"]{
    background:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA
# ==================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data():

    file_path = hf_hub_download(
        repo_id=HF_DATASET_ID,
        filename=FILE_NAME,
        repo_type="dataset"
    )

    return pd.read_parquet(file_path)

df = load_data()

if df.empty:
    st.error("Dataset empty")
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

colored_header(
    label="Workforce Intelligence Platform",
    description="Interactive Labor Market Analytics",
    color_name="blue-70"
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    page = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Companies",
            "Locations",
            "ML Insights",
            "Explorer"
        ],
        icons=[
            "speedometer2",
            "building",
            "geo-alt",
            "cpu",
            "table"
        ],
        default_index=0
    )

    st.divider()

    search = st.text_input(
        "Search Jobs"
    )

    location = st.selectbox(
        "Location",
        ["All"] + sorted(
            df["location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    company = st.selectbox(
        "Company",
        ["All"] + sorted(
            df["company"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
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
        filtered["location"] == location
    ]

if company != "All":
    filtered = filtered[
        filtered["company"] == company
    ]

# ==================================================
# OVERVIEW
# ==================================================

if page == "Overview":

    c1,c2,c3,c4 = st.columns(4)

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

    coverage = round(
        len(filtered)
        / len(df)
        * 100,
        1
    )

    c4.metric(
        "Coverage",
        f"{coverage}%"
    )

    style_metric_cards()

    st.divider()

    left,right = st.columns(2)

    with left:

        comp = (
            filtered["company"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        comp.columns = [
            "Company",
            "Jobs"
        ]

        fig = px.bar(
            comp,
            x="Jobs",
            y="Company",
            orientation="h",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        loc = (
            filtered["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        loc.columns = [
            "Location",
            "Jobs"
        ]

        fig = px.bar(
            loc,
            x="Jobs",
            y="Location",
            orientation="h",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# COMPANIES
# ==================================================

elif page == "Companies":

    st.subheader(
        "Top Hiring Companies"
    )

    data = (
        filtered["company"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    data.columns = [
        "Company",
        "Jobs"
    ]

    fig = px.treemap(
        data,
        path=["Company"],
        values="Jobs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# LOCATIONS
# ==================================================

elif page == "Locations":

    st.subheader(
        "Location Distribution"
    )

    data = (
        filtered["location"]
        .value_counts()
        .head(20)
        .reset_index()
    )

    data.columns = [
        "Location",
        "Jobs"
    ]

    fig = px.pie(
        data,
        names="Location",
        values="Jobs",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# ML INSIGHTS
# ==================================================

elif page == "ML Insights":

    st.subheader(
        "Job Title Clustering"
    )

    jobs = (
        filtered["title"]
        .fillna("")
        .astype(str)
        .head(3000)
    )

    if len(jobs) > 20:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500
        )

        X = vectorizer.fit_transform(
            jobs
        )

        model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X)

        cluster_df = pd.DataFrame({
            "Job Title": jobs,
            "Cluster": labels
        })

        st.dataframe(
            cluster_df.head(100)
        )

        st.success(
            f"Generated {cluster_df['Cluster'].nunique()} job clusters"
        )

    else:

        st.warning(
            "Not enough data for clustering"
        )

# ==================================================
# EXPLORER
# ==================================================

elif page == "Explorer":

    st.subheader(
        "Interactive Data Explorer"
    )

    AgGrid(
        filtered.head(5000),
        fit_columns_on_grid_load=True
    )

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Powered by Hugging Face • Plotly • Scikit-learn • Streamlit"
)