import streamlit as st
import pandas as pd
import os
from huggingface_hub import hf_hub_download

# =========================
# CONFIG
# =========================
HF_DATASET_ID = "Vincentran/careerviet-accounting-jobs"
HF_TOKEN = os.getenv("HF_TOKEN")
FILE_NAME = "jobs.parquet"

# =========================
# PAGE CONFIG (UI UPGRADE)
# =========================
st.set_page_config(
    page_title="AI Job Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM UI STYLE (CLEAN MODERN LOOK)
# =========================
st.markdown("""
    <style>
        .main {background-color: #0f1117;}
        h1, h2, h3 {color: #00d4ff;}
        .stMetric {background-color: #1a1d25; padding: 10px; border-radius: 10px;}
        .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA FROM HF
# =========================
@st.cache_data
def load_data():
    try:
        file_path = hf_hub_download(
            repo_id=HF_DATASET_ID,
            filename=FILE_NAME,
            repo_type="dataset",
            token=HF_TOKEN
        )
        return pd.read_parquet(file_path)

    except Exception as e:
        st.error(f"❌ Failed to load HF dataset: {e}")
        return pd.DataFrame()


df = load_data()

# =========================
# HEADER (AI UX/UI)
# =========================
st.title("🤖 AI Job Intelligence System")
st.caption("AI Agent • Job Search • Insights • Analytics • Chatbot")

if df.empty:
    st.warning("No data available")
    st.stop()

# =========================
# AI AGENT SIDEBAR
# =========================
st.sidebar.header("🧠 AI Agent Control Center")

query = st.sidebar.text_input("🔎 AI Job Search")

location_filter = st.sidebar.selectbox(
    "📍 Location Filter",
    ["All"] + sorted(df["location"].dropna().unique().tolist()) if "location" in df else ["All"]
)

company_filter = st.sidebar.selectbox(
    "🏢 Company Filter",
    ["All"] + sorted(df["company"].dropna().unique().tolist()) if "company" in df else ["All"]
)

# =========================
# FILTER ENGINE (AI JOB SEARCH LOGIC)
# =========================
filtered_df = df.copy()

if query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(query, case=False, na=False)
    ]

if location_filter != "All":
    filtered_df = filtered_df[filtered_df["location"] == location_filter]

if company_filter != "All":
    filtered_df = filtered_df[filtered_df["company"] == company_filter]

# =========================
# KPI DASHBOARD (AI ANALYTICS)
# =========================
st.subheader("📊 AI Analytics Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Companies", filtered_df["company"].nunique() if "company" in df else 0)
col3.metric("Locations", filtered_df["location"].nunique() if "location" in df else 0)
col4.metric("Active Filters", 2)

st.divider()

# =========================
# AI INSIGHTS ENGINE
# =========================
st.subheader("🧠 AI Insights Engine")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.write("🔥 Top Companies Hiring")
    if "company" in filtered_df:
        st.dataframe(filtered_df["company"].value_counts().head(5))

with insight_col2:
    st.write("📍 Top Locations")
    if "location" in filtered_df:
        st.dataframe(filtered_df["location"].value_counts().head(5))

# =========================
# AI CHARTS (MODERN VISUALS)
# =========================
st.subheader("📈 AI Charts")

if "location" in filtered_df:
    loc_data = filtered_df["location"].value_counts().head(7).reset_index()
    loc_data.columns = ["location", "count"]

    st.bar_chart(loc_data.set_index("location"))

if "company" in filtered_df:
    comp_data = filtered_df["company"].value_counts().head(7).reset_index()
    comp_data.columns = ["company", "count"]

    st.bar_chart(comp_data.set_index("company"))

# =========================
# AI JOB TABLE
# =========================
st.subheader("🔎 AI Job Search Results")

st.dataframe(filtered_df, use_container_width=True)

# =========================
# AI CHATBOT (LIGHTWEIGHT)
# =========================
st.subheader("💬 AI Chat Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask AI about jobs")

if user_input:
    if "company" in user_input.lower():
        answer = f"Top companies: {', '.join(filtered_df['company'].value_counts().head(3).index)}"
    elif "location" in user_input.lower():
        answer = f"Top locations: {', '.join(filtered_df['location'].value_counts().head(3).index)}"
    else:
        answer = f"I found {len(filtered_df)} relevant jobs for your query."

    st.session_state.chat.append((user_input, answer))

for q, a in reversed(st.session_state.chat):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 AI:** {a}")
    st.markdown("---")

# =========================
# FOOTER
# =========================
st.caption("🚀 Powered by AI Agent • HuggingFace Dataset • Streamlit • Analytics Engine")