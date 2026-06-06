import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import ast
from collections import Counter
from sklearn.linear_model import LinearRegression
import datetime as dt

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AI Job Intelligence Platform",
    layout="wide"
)

# =========================
# AUTO REFRESH (REAL-TIME SIMULATION)
# =========================
st.sidebar.title("⚙️ Controls")
auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=True)

if auto_refresh:
    st.autorefresh = st.sidebar.empty()
    st.experimental_rerun()

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_parquet("jobs.parquet")
    return df

df = load_data()

# =========================
# DATA CLEANING + NORMALIZATION
# =========================
def clean_skills(x):
    try:
        if isinstance(x, list):
            return x
        return ast.literal_eval(x)
    except:
        return []

df = df.drop_duplicates()

df["skills"] = df["skills"].apply(clean_skills)

# normalize missing values
df["location"] = df["location"].fillna("Unknown")
df["company"] = df["company"].fillna("Unknown")
df["platform"] = df["platform"].fillna("Unknown")

# =========================
# FEATURE ENGINEERING
# =========================
df["job_age"] = np.random.randint(1, 30, len(df))  # simulate (replace with real date later)

all_skills = [s for sub in df["skills"] for s in sub]
skill_counts = Counter(all_skills)

# =========================
# SIDEBAR FILTER (SLICERS)
# =========================
platform_filter = st.sidebar.multiselect(
    "Platform",
    df["platform"].unique(),
    default=list(df["platform"].unique())
)

company_filter = st.sidebar.multiselect(
    "Company",
    df["company"].unique()
)

df_filtered = df[df["platform"].isin(platform_filter)]

if company_filter:
    df_filtered = df_filtered[df_filtered["company"].isin(company_filter)]

# search
search = st.sidebar.text_input("Search Job")

if search:
    df_filtered = df_filtered[df_filtered["title"].str.contains(search, case=False, na=False)]

# =========================
# HEADER
# =========================
st.title("🚀 AI Job Market Intelligence Dashboard")
st.caption("Real-time analytics + AI insights + forecasting engine")

st.markdown("---")

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", len(df_filtered))
col2.metric("Companies", df_filtered["company"].nunique())
col3.metric("Skills Found", len(skill_counts))
col4.metric("Platforms", df_filtered["platform"].nunique())

st.markdown("---")

# =========================
# AI MARKET INSIGHT ENGINE (RULE-BASED + LLM READY)
# =========================
st.subheader("🧠 AI Market Insight Engine")

top_skill = skill_counts.most_common(1)[0][0] if skill_counts else "N/A"
top_company = df_filtered["company"].value_counts().index[0] if len(df_filtered) > 0 else "N/A"

insight = f"""
📊 Market Insight:
- Most demanded skill: **{top_skill}**
- Top hiring company: **{top_company}**
- Market is dominated by {df_filtered['platform'].mode()[0] if len(df_filtered)>0 else 'N/A'}

💡 Recommendation:
Focus on {top_skill}, combine with SQL + data visualization skills.
"""

st.info(insight)

# =========================
# CHARTS (ADVANCED + DYNAMIC)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Platform Distribution")
    fig = px.pie(df_filtered, names="platform", title="Jobs by Platform")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔥 Top Skills (AI Extracted)")
    top_skills = pd.DataFrame(skill_counts.most_common(10), columns=["Skill", "Count"])
    fig = px.bar(top_skills, x="Skill", y="Count")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# COMPANY ANALYTICS
# =========================
st.subheader("🏢 Hiring Companies Intelligence")

company_df = df_filtered["company"].value_counts().head(10).reset_index()
company_df.columns = ["Company", "Jobs"]

fig = px.bar(company_df, x="Company", y="Jobs")
st.plotly_chart(fig, use_container_width=True)

# =========================
# FORECASTING ENGINE (SIMPLE ML MODEL)
# =========================
st.subheader("📈 Job Market Forecasting (ML)")

trend_data = df_filtered.groupby("platform").size().reset_index(name="count")
trend_data["time"] = np.arange(len(trend_data))

if len(trend_data) > 1:
    model = LinearRegression()
    model.fit(trend_data[["time"]], trend_data["count"])
    future = model.predict([[len(trend_data) + 1]])

    st.success(f"📊 Predicted job volume next period: {int(future[0])}")

# =========================
# JOB TABLE (WITH URL COLUMN)
# =========================
st.subheader("🔍 Job Explorer (Advanced Table)")

table_df = df_filtered[[
    "title",
    "company",
    "platform",
    "location",
    "skills",
    "url"   # URL JOB COLUMN (IMPORTANT)
]]

st.dataframe(table_df, use_container_width=True)

# =========================
# VISUAL HEATMAP (SKILL INTENSITY)
# =========================
st.subheader("🧬 Skill Intelligence Heatmap")

if skill_counts:
    heat_df = pd.DataFrame(skill_counts.most_common(15), columns=["Skill", "Count"])
    heat_df["Intensity"] = heat_df["Count"] / heat_df["Count"].max()

    fig = go.Figure(data=go.Heatmap(
        z=[heat_df["Intensity"]],
        x=heat_df["Skill"],
        colorscale="Viridis"
    ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# AI AGENT CHAT (SIMPLE LLM PLACEHOLDER)
# =========================
st.subheader("🤖 AI Agent (Ask Market Questions)")

user_q = st.text_input("Ask AI (e.g. 'What skill should I learn?')")

if user_q:
    # simple rule-based AI (replace with OpenAI API later)
    if "skill" in user_q.lower():
        st.write(f"👉 You should focus on: {top_skill} + SQL + Power BI")
    elif "market" in user_q.lower():
        st.write(f"👉 Market is trending towards {top_skill} jobs")
    else:
        st.write("👉 AI Agent: I recommend focusing on data + analytics skills")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("AI Dashboard v1 | Upgrade ready for LLM API + real-time ci")