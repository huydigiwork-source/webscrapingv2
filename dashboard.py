import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import plotly.express as px

# =========================
# CONFIG
# =========================
HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

st.set_page_config(
    page_title="Workforce Intelligence",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    path = hf_hub_download(
        repo_id=HF_DATASET_ID,
        filename=FILE_NAME,
        repo_type="dataset"
    )
    return pd.read_parquet(path)

df = load_data()

if df.empty:
    st.error("Empty dataset")
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Control Panel")

search = st.sidebar.text_input("Search Job")

location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(df["location"].dropna().unique().tolist())
)

company = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(df["company"].dropna().unique().tolist())
)

top_n = st.sidebar.slider("Top N", 3, 20, 7)

# =========================
# FILTER SAFE ENGINE
# =========================
filtered = df.copy()

if search and "title" in df.columns:
    filtered = filtered[filtered["title"].str.contains(search, case=False, na=False)]

if location != "All":
    filtered = filtered[filtered["location"] == location]

if company != "All":
    filtered = filtered[filtered["company"] == company]

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Jobs", len(filtered))
c2.metric("Companies", filtered["company"].nunique())
c3.metric("Locations", filtered["location"].nunique())
c4.metric("Coverage", f"{len(filtered)/len(df)*100:.1f}%")

st.divider()

# =========================
# CHARTS
# =========================
left, right = st.columns(2)

with left:
    st.subheader("Top Companies")

    comp = filtered["company"].value_counts().head(top_n)
    fig = px.bar(
        x=comp.values,
        y=comp.index,
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top Locations")

    loc = filtered["location"].value_counts().head(top_n)
    fig = px.bar(
        x=loc.values,
        y=loc.index,
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# PIE SECTION
# =========================
c1, c2 = st.columns(2)

with c1:
    if "location" in df.columns:
        loc_pie = filtered["location"].value_counts().head(8)
        fig = px.pie(
            names=loc_pie.index,
            values=loc_pie.values,
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    if "company" in df.columns:
        comp_pie = filtered["company"].value_counts().head(8)
        fig = px.pie(
            names=comp_pie.index,
            values=comp_pie.values,
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("Data Explorer")
st.dataframe(filtered, use_container_width=True, height=500)

# =========================
# SIMPLE INSIGHT BOT
# =========================
st.subheader("Assistant")

q = st.text_input("Ask something")

if q:
    if "company" in q.lower():
        st.info(filtered["company"].value_counts().head(3).to_string())
    elif "location" in q.lower():
        st.info(filtered["location"].value_counts().head(3).to_string())
    else:
        st.info(f"{len(filtered)} jobs found")