import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Career Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}
    h1 {color: #4F8BF9;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 Career Intelligence Platform")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("jobs.parquet")
    except:
        df = pd.DataFrame({
            "title": ["Data Analyst", "Backend Dev", "AI Engineer", "Business Analyst"],
            "company": ["A", "B", "C", "D"],
            "platform": ["linkedin", "itviec", "linkedin", "career"],
            "location": ["Vietnam", "HCM", "HN", "Vietnam"],
            "skills": [["SQL"], ["Java"], ["AI"], ["Excel"]],
            "url": [
                "https://job1.com",
                "https://job2.com",
                "https://job3.com",
                "https://job4.com"
            ]
        })
    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🎛 Filters")

platform = st.sidebar.multiselect(
    "Platform",
    df["platform"].unique(),
    default=df["platform"].unique()
)

location = st.sidebar.multiselect(
    "Location",
    df["location"].unique(),
    default=df["location"].unique()
)

filtered = df[
    (df["platform"].isin(platform)) &
    (df["location"].isin(location))
]

# =========================
# KPI CARDS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📊 Jobs", len(filtered))
col2.metric("🏢 Companies", filtered["company"].nunique())
col3.metric("🌐 Platforms", filtered["platform"].nunique())

st.markdown("---")

# =========================
# CHARTS SECTION
# =========================
c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        filtered["platform"].value_counts().reset_index(),
        x="index",
        y="platform",
        title="Jobs by Platform"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        filtered,
        names="location",
        title="Jobs by Location"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TREND (SIMPLE INSIGHT)
# =========================
st.subheader("📈 Market Trend Snapshot")

trend = filtered.groupby("platform").size().reset_index(name="count")
fig3 = px.line(trend, x="platform", y="count", markers=True)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# INSIGHT BOX
# =========================
st.subheader("🧠 AI Insight (Static Module)")

st.info("""
- Data & AI roles đang tăng trưởng mạnh
- LinkedIn chiếm phần lớn job postings
- SQL + Python là core skill phổ biến nhất
""")

# =========================
# JOB TABLE
# =========================
st.subheader("📄 Job Listings")

table = filtered.copy()
table["apply"] = table["url"].apply(lambda x: f"[Apply]({x})")

st.dataframe(
    table[["title", "company", "platform", "location", "apply"]],
    use_container_width=True
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built for Career Intelligence System 🚀")