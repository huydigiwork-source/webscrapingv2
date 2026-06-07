import streamlit as st
import pandas as pd
import json
from pathlib import Path
from huggingface_hub import hf_hub_download
import plotly.express as px

# ==================================================

# PAGE CONFIG

# ==================================================

st.set_page_config(
page_title="Workforce Intelligence",
page_icon="📊",
layout="wide",
initial_sidebar_state="expanded"
)

# ==================================================

# LOAD STYLE

# ==================================================

def load_css():
css_file = Path("style.css")
if css_file.exists():
with open(css_file, encoding="utf-8") as f:
st.markdown(
f"<style>{f.read()}</style>",
unsafe_allow_html=True
)

load_css()

# ==================================================

# CONFIG

# ==================================================

HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

# ==================================================

# DATA

# ==================================================

@st.cache_data(ttl=3600)
def load_data():

```
file_path = hf_hub_download(
    repo_id=HF_DATASET_ID,
    filename=FILE_NAME,
    repo_type="dataset"
)

return pd.read_parquet(file_path)
```

df = load_data()

if df.empty:
st.error("Dataset is empty")
st.stop()

for col in ["title", "company", "location"]:
if col not in df.columns:
df[col] = ""

# ==================================================

# HERO

# ==================================================

st.markdown("""

<div class="hero-card">
<h1>Workforce Intelligence Platform</h1>
<p>Interactive Labor Market Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ==================================================

# FILTERS

# ==================================================

with st.sidebar:

```
st.markdown("## Filters")

search = st.text_input("Search Jobs")

location = st.selectbox(
    "Location",
    ["All"] + sorted(
        df["location"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
)

company = st.selectbox(
    "Company",
    ["All"] + sorted(
        df["company"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
)
```

filtered = df.copy()

if search:
filtered = filtered[
filtered["title"]
.astype(str)
.str.contains(search, case=False, na=False)
]

if location != "All":
filtered = filtered[
filtered["location"] == location
]

if company != "All":
filtered = filtered[
filtered["company"] == company
]

# ==================================================

# KPI

# ==================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric("Jobs", f"{len(filtered):,}")
c2.metric("Companies", filtered["company"].nunique())
c3.metric("Locations", filtered["location"].nunique())

coverage = round(
len(filtered) / len(df) * 100,
1
)

c4.metric("Coverage", f"{coverage}%")

st.divider()

# ==================================================

# CHARTS

# ==================================================

left,right = st.columns(2)

with left:

```
st.subheader("Top Companies")

comp = (
    filtered["company"]
    .value_counts()
    .head(10)
    .reset_index()
)

comp.columns = [
    "Company",
    "Jobs"
]

fig = px.bar(
    comp,
    x="Jobs",
    y="Company",
    orientation="h",
    template="plotly_dark"
)

fig.update_layout(
    height=450,
    margin=dict(l=20,r=20,t=20,b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

with right:

```
st.subheader("Top Locations")

loc = (
    filtered["location"]
    .value_counts()
    .head(10)
    .reset_index()
)

loc.columns = [
    "Location",
    "Jobs"
]

fig = px.bar(
    loc,
    x="Jobs",
    y="Location",
    orientation="h",
    template="plotly_dark"
)

fig.update_layout(
    height=450,
    margin=dict(l=20,r=20,t=20,b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

# ==================================================

# TABLE

# ==================================================

st.subheader("Data Explorer")

st.dataframe(
filtered.head(1000),
use_container_width=True,
height=550
)

st.caption(
f"Showing {min(len(filtered),1000):,} / {len(filtered):,} rows"
)

st.divider()

st.caption(
"Powered by Hugging Face • Plotly • Streamlit"
)
