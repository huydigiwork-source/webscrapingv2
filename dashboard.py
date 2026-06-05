import streamlit as st
import pandas as pd
from datasets import load_dataset

st.set_page_config(page_title="CareerViet Analytics", layout="wide")

st.title("📊 CareerViet Job Market Dashboard")

# =========================
# LOAD HF DATASET
# =========================
dataset = load_dataset("Vincentran/careerviet-accounting-jobs", split="train")
df = pd.DataFrame(dataset)

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Companies", df["company"].nunique())
col3.metric("Avg Skills / Job", round(df["skill_count"].mean(), 2))

st.divider()

# =========================
# FILTER
# =========================
st.subheader("🔍 Filter Jobs")

company = st.selectbox("Company", ["All"] + list(df["company"].unique()))

filtered = df if company == "All" else df[df["company"] == company]

st.write(f"Showing: {len(filtered)} jobs")

# =========================
# TABLE
# =========================
st.dataframe(filtered[[
    "job_title",
    "company",
    "location",
    "salary",
    "skill_count",
    "experience"
]])