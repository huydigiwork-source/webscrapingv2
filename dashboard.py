import streamlit as st
import pandas as pd
import numpy as np
from datasets import load_dataset

from sentence_transformers import SentenceTransformer
import faiss

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="HR AI SaaS v7",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 HR AI SaaS Platform v7 (Startup Ready)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    ds = load_dataset(
        "Vincentran/careerviet-accounting-jobs",
        split="train"
    )
    return pd.DataFrame(ds)

df = load_data().fillna("")
df.columns = [c.lower() for c in df.columns]

# =========================
# EMBEDDING + VECTOR DB
# =========================
@st.cache_resource
def build_vector_db(dataframe):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    corpus = (
        dataframe["job_title"].astype(str) + " " +
        dataframe["company"].astype(str) + " " +
        dataframe["location"].astype(str) + " " +
        dataframe["market_skill"].astype(str) + " " +
        dataframe["requirements"].astype(str)
    ).tolist()

    embeddings = model.encode(corpus, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return model, index

model, index = build_vector_db(df)

# =========================
# SEARCH ENGINE
# =========================
def search(query, k=5):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k)
    return df.iloc[I[0]]

# =========================
# RESUME MATCHING ENGINE
# =========================
def match_resume(resume_text):

    q_emb = model.encode([resume_text])
    D, I = index.search(np.array(q_emb), 5)

    return df.iloc[I[0]]

# =========================
# AGENTS
# =========================
def recruiter_agent(results):
    return f"""
🧑‍💼 RECRUITER AI

Top candidate job:
- {results.iloc[0]['job_title']}

Required skills:
- {results.iloc[0]['market_skill']}

Hiring advice:
- Target mid-level accounting talent
- Focus Excel + ERP + Audit skills
"""

def analyst_agent(results):
    return f"""
📊 ANALYST AI

Market insight:
- Top role: {results.iloc[0]['job_title']}
- Company: {results.iloc[0]['company']}

Insight:
- Demand concentrated in accounting & finance roles
- Skill cluster: Excel, Audit, Tax, ERP
"""

def matcher_agent(results):
    return f"""
🎯 MATCHING AI

Best match:
- {results.iloc[0]['job_title']}
- Location: {results.iloc[0]['location']}

Match confidence:
- High semantic similarity via embeddings
"""

# =========================
# UI: SIDEBAR
# =========================
st.sidebar.title("🤖 AI SaaS Engine")

mode = st.sidebar.selectbox(
    "Mode",
    ["Job Search", "Resume Matcher", "Recruiter Agent", "Analyst Agent"]
)

query = st.sidebar.text_input("Enter query")

resume = st.sidebar.text_area("Resume (for matching only)")

# =========================
# EXECUTION
# =========================
if mode == "Job Search" and query:
    results = search(query)

elif mode == "Resume Matcher" and resume:
    results = match_resume(resume)

elif mode in ["Recruiter Agent", "Analyst Agent"] and query:
    results = search(query)

else:
    results = None

# =========================
# MAIN DASHBOARD
# =========================
c1, c2, c3 = st.columns(3)

c1.metric("Jobs", len(df))
c2.metric("Companies", df["company"].nunique())
c3.metric("Locations", df["location"].nunique())

st.divider()

# =========================
# RESULTS VIEW
# =========================
if results is not None:

    st.subheader("🔎 Top Matches")

    st.dataframe(
        results[[
            "job_title",
            "company",
            "location",
            "salary",
            "market_skill"
        ]]
    )

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        st.info(recruiter_agent(results))

    with colB:
        st.info(analyst_agent(results))

else:
    st.warning("Enter query or resume to activate AI SaaS engine")