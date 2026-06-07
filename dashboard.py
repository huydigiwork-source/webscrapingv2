import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AI Job Intelligence Dashboard",
    layout="wide",
    page_icon="📊"
)

DATA_PATH = "jobs.parquet"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_parquet(DATA_PATH)
    else:
        st.error("jobs.parquet not found")
        return pd.DataFrame()
    return df


df = load_data()

# =========================
# HEADER (AI UX/UI)
# =========================
st.title("🤖 AI Job Intelligence System")
st.caption("AI Agent • Job Search • Insights • Analytics • Chatbot")

# =========================
# SIDEBAR - AI AGENT FILTER
# =========================
st.sidebar.header("🧠 AI Agent Controls")

keyword = st.sidebar.text_input("Search Job (AI Query)", "")
city_filter = st.sidebar.selectbox(
    "Location Filter",
    ["All"] + list(df["location"].dropna().unique()) if not df.empty else ["All"]
)

if keyword:
    df = df[df["title"].str.contains(keyword, case=False, na=False)]

if city_filter != "All":
    df = df[df["location"] == city_filter]

# =========================
# KPI METRICS (AI ANALYTICS)
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Jobs", len(df))

with col2:
    if "company" in df.columns:
        st.metric("Companies", df["company"].nunique())
    else:
        st.metric("Companies", "N/A")

with col3:
    if "location" in df.columns:
        st.metric("Locations", df["location"].nunique())
    else:
        st.metric("Locations", "N/A")

st.divider()

# =========================
# AI INSIGHTS SECTION
# =========================
st.subheader("🧠 AI Insights Engine")

if not df.empty:

    top_company = df["company"].value_counts().head(5) if "company" in df else None

    colA, colB = st.columns(2)

    with colA:
        st.write("🔥 Top Hiring Companies")
        if top_company is not None:
            st.dataframe(top_company)

    with colB:
        st.write("📍 Top Locations")
        if "location" in df:
            st.dataframe(df["location"].value_counts().head(5))

# =========================
# AI CHARTS
# =========================
st.subheader("📊 AI Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:
    if "location" in df:
        fig1 = px.bar(
            df["location"].value_counts().head(10),
            title="Jobs by Location"
        )
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    if "company" in df:
        fig2 = px.pie(
            names=df["company"].value_counts().head(8).index,
            values=df["company"].value_counts().head(8).values,
            title="Top Companies Share"
        )
        st.plotly_chart(fig2, use_container_width=True)

# =========================
# AI JOB SEARCH RESULTS
# =========================
st.subheader("🔎 AI Job Search Results")

st.dataframe(df, use_container_width=True)

# =========================
# AI CHATBOT (SIMPLE VERSION)
# =========================
st.divider()
st.subheader("💬 AI Chatbot Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask AI about jobs:")

if user_input:

    response = "I analyzed your dataset and found relevant job insights."

    if "data" in user_input.lower():
        response = f"Dataset contains {len(df)} jobs."

    elif "company" in user_input.lower():
        response = "Top companies: " + ", ".join(df["company"].value_counts().head(3).index) if "company" in df else "No data"

    st.session_state.chat_history.append((user_input, response))

for q, a in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 AI:** {a}")
    st.markdown("---")

# =========================
# FOOTER (AI UX)
# =========================
st.caption("🚀 Powered by AI Agent • HuggingFace Dataset • Streamlit")