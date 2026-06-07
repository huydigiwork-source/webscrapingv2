import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import os

# =========================
# CONFIG
# =========================
DATASET_ID = "Vincentran/careerviet-accounting-jobs"

# =========================
# LOAD DATA (LATEST HF)
# =========================
@st.cache_data(ttl=0)
def load_data():
    file_path = hf_hub_download(
        repo_id=DATASET_ID,
        filename="jobs.parquet",
        repo_type="dataset",
        revision="main",
        force_download=True
    )
    return pd.read_parquet(file_path)

df = load_data()

# =========================
# AI LAYER (SIMULATED AGENTS)
# =========================

def ai_job_search(query):
    if not query:
        return df
    return df[df["job_title"].str.contains(query, case=False, na=False)]

def ai_insights(data):
    insights = []
    insights.append(f"Total jobs: {len(data)}")
    insights.append(f"Top company: {data['company'].value_counts().idxmax()}")
    insights.append(f"Top location: {data['location'].value_counts().idxmax()}")
    return insights

def ai_recommend_jobs():
    return df.sample(min(5, len(df)))

def ai_chatbot(user_input):
    if "salary" in user_input.lower():
        return "Most jobs in dataset are accounting roles with mid-level salary range (estimated)."
    if "company" in user_input.lower():
        return "Top hiring companies are distributed across SME and enterprise sectors."
    return "I can help you analyze jobs, trends, companies, and recommendations."

def ai_analytics(data):
    return {
        "total_jobs": len(data),
        "companies": data["company"].nunique(),
        "locations": data["location"].nunique()
    }

# =========================
# UI CONFIG
# =========================
st.set_page_config(page_title="AI Job Intelligence Platform", layout="wide")

st.title("🚀 AI Job Intelligence Platform")

# =========================
# SIDEBAR - AI JOB SEARCH
# =========================
st.sidebar.header("🔎 AI Job Search")

query = st.sidebar.text_input("Search jobs (AI agent)")

filtered_df = ai_job_search(query)

st.sidebar.subheader("🤖 AI Recommendations")
st.sidebar.dataframe(ai_recommend_jobs())

# =========================
# MAIN DASHBOARD
# =========================

col1, col2, col3 = st.columns(3)

analytics = ai_analytics(filtered_df)

with col1:
    st.metric("Total Jobs", analytics["total_jobs"])

with col2:
    st.metric("Companies", analytics["companies"])

with col3:
    st.metric("Locations", analytics["locations"])

st.divider()

# =========================
# AI INSIGHTS SECTION
# =========================
st.subheader("🧠 AI Insights")

for i in ai_insights(filtered_df):
    st.write("•", i)

st.divider()

# =========================
# DATA TABLE (UX/UI LAYER)
# =========================
st.subheader("📊 Job Data Explorer")
st.dataframe(filtered_df, use_container_width=True)

# =========================
# AI CHATBOT
# =========================
st.subheader("💬 AI Chatbot")

user_input = st.text_input("Ask AI about jobs, salary, companies...")

if user_input:
    response = ai_chatbot(user_input)
    st.success(response)

st.divider()

# =========================
# AI CHARTS
# =========================
st.subheader("📈 AI Charts")

chart_data = filtered_df["company"].value_counts().head(10)

chart_df = pd.DataFrame({
    "company": chart_data.index,
    "count": chart_data.values
})

st.bar_chart(chart_df.set_index("company"))

# =========================
# FOOTER
# =========================
st.caption("AI-powered Job Intelligence Dashboard (HF + Streamlit + AI Layer)")