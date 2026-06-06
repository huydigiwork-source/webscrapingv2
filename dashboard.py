import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# CONFIG UI
# =========================
st.set_page_config(
    page_title="Career Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Career Intelligence Dashboard")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("jobs.parquet")
    except:
        # fallback demo data
        df = pd.DataFrame({
            "title": ["Data Analyst", "Backend Dev", "AI Engineer", "Business Analyst"],
            "company": ["A", "B", "C", "D"],
            "platform": ["linkedin", "career", "linkedin", "career"],
            "location": ["Vietnam", "HCM", "HN", "Vietnam"],
            "skills": [["SQL", "Python"], ["Java"], ["AI", "Python"], ["Excel"]],
            "url": ["https://job1.com", "https://job2.com", "https://job3.com", "https://job4.com"]
        })
    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🎛 Filters")

platform_filter = st.sidebar.multiselect(
    "Platform",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)

location_filter = st.sidebar.multiselect(
    "Location",
    options=df["location"].unique(),
    default=df["location"].unique()
)

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["location"].isin(location_filter))
]

# =========================
# KPI SECTION
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Jobs", len(filtered_df))
col2.metric("🏢 Companies", filtered_df["company"].nunique())
col3.metric("🌐 Platforms", filtered_df["platform"].nunique())

st.markdown("---")

# =========================
# CHART 1: JOBS BY PLATFORM
# =========================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        filtered_df["platform"].value_counts().reset_index(),
        x="index",
        y="platform",
        title="Jobs by Platform",
        labels={"index": "Platform", "platform": "Count"}
    )
    st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2: JOBS BY LOCATION
# =========================
with col2:
    fig2 = px.pie(
        filtered_df,
        names="location",
        title="Jobs by Location"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# FORECASTING SIMPLE MODEL
# =========================
st.subheader("📈 Simple Job Trend Forecast (Demo)")

trend = np.arange(len(filtered_df))
forecast = trend * 1.5 + np.random.randint(0, 3, len(filtered_df))

fig3 = px.line(
    x=trend,
    y=forecast,
    title="Forecasted Job Growth Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# AI INSIGHT PLACEHOLDER
# =========================
st.subheader("🧠 AI Market Insight")

st.info("""
- Demand cao nhất: Data-related roles
- LinkedIn chiếm phần lớn job postings
- Python + SQL là skill xuất hiện nhiều nhất
""")

st.caption("⚡ AI module can be connected later (LLM / API)")

# =========================
# JOB TABLE
# =========================
st.subheader("📄 Job Listings")

def make_clickable(url):
    return f"[Apply]({url})"

display_df = filtered_df.copy()
display_df["apply"] = display_df["url"].apply(make_clickable)

st.dataframe(
    display_df[["title", "company", "platform", "location", "apply"]],
    use_container_width=True
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built for Career Intelligence System 🚀")