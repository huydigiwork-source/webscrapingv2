import streamlit as st
import pandas as pd
import os
from huggingface_hub import hf_hub_download
import plotly.express as px

# streamlit-extras UI enhancer
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

# =========================
# CONFIG
# =========================
HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Workforce Intelligence Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =========================
# MODERN DARK THEME
# =========================
st.markdown("""
<style>
    html, body, [class*="css"] {
        background-color: #0b0f1a;
        color: #e6e6e6;
    }

    .block-container {
        padding: 2rem;
    }

    div[data-testid="stMetric"] {
        background-color: #111827;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA FROM HF
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
    st.error("Dataset is empty")
    st.stop()

# =========================
# HEADER (MODERN)
# =========================
colored_header(
    label="Workforce Intelligence Dashboard",
    description="Real-time labor market analytics • AI insights • interactive exploration",
    color_name="blue-70"
)

# =========================
# SIDEBAR (AI SLICERS)
# =========================
st.sidebar.header("⚙️ Control Panel")

search = st.sidebar.text_input("🔍 Job Search")

location = st.sidebar.selectbox(
    "📍 Location",
    ["All"] + sorted(df["location"].dropna().unique()) if "location" in df else ["All"]
)

company = st.sidebar.selectbox(
    "🏢 Company",
    ["All"] + sorted(df["company"].dropna().unique()) if "company" in df else ["All"]
)

top_n = st.sidebar.slider("📊 Top N Insights", 3, 20, 7)

# =========================
# FILTER ENGINE
# =========================
filtered = df.copy()

if search:
    filtered = filtered[filtered["title"].str.contains(search, case=False, na=False)]

if location != "All":
    filtered = filtered[filtered["location"] == location]

if company != "All":
    filtered = filtered[filtered["company"] == company]

# =========================
# KPI DASHBOARD
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Jobs", len(filtered))
c2.metric("Companies", filtered["company"].nunique())
c3.metric("Locations", filtered["location"].nunique())
c4.metric("Coverage", f"{len(filtered)/len(df)*100:.1f}%")

style_metric_cards()

st.divider()

# =========================
# ANALYTICS CHARTS
# =========================
left, right = st.columns(2)

with left:
    st.subheader("🏢 Top Companies")

    comp = filtered["company"].value_counts().head(top_n)
    fig = px.bar(
        comp,
        x=comp.values,
        y=comp.index,
        orientation="h",
        color=comp.values,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("📍 Top Locations")

    loc = filtered["location"].value_counts().head(top_n)
    fig = px.bar(
        loc,
        x=loc.values,
        y=loc.index,
        orientation="h",
        color=loc.values,
        color_continuous_scale="Purples"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# DISTRIBUTION INSIGHTS
# =========================
st.subheader("📊 Market Distribution")

c1, c2 = st.columns(2)

with c1:
    if "location" in filtered:
        fig = px.pie(
            names=filtered["location"].value_counts().head(8).index,
            values=filtered["location"].value_counts().head(8).values,
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    if "company" in filtered:
        fig = px.pie(
            names=filtered["company"].value_counts().head(8).index,
            values=filtered["company"].value_counts().head(8).values,
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================
# DATA EXPLORER
# =========================
st.subheader("🔎 Data Explorer")
st.dataframe(filtered, use_container_width=True, height=500)

# =========================
# SIMPLE AI ASSISTANT (NO LABEL AI)
# =========================
st.subheader("💬 Assistant")

user_q = st.text_input("Ask about job market")

if user_q:
    if "company" in user_q.lower():
        answer = filtered["company"].value_counts().head(3).to_string()
    elif "location" in user_q.lower():
        answer = filtered["location"].value_counts().head(3).to_string()
    else:
        answer = f"{len(filtered)} jobs found."

    st.info(answer)

# =========================
# FOOTER
# =========================
st.caption("Powered by HuggingFace • Streamlit • Plotly • Analytics Engine")