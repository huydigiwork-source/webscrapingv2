import streamlit as st
import pandas as pd
import plotly.express as px
from huggingface_hub import hf_hub_download

from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

# ==================================================
# CONFIG
# ==================================================
HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

# ==================================================
# PAGE
# ==================================================
st.set_page_config(
    page_title="Workforce Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}

div[data-testid="stMetric"]{
    background:#111827;
    border-radius:12px;
    padding:12px;
    border:1px solid #1f2937;
}

[data-testid="stSidebar"]{
    background:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA LOADER
# ==================================================
@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data():

    file_path = hf_hub_download(
        repo_id=HF_DATASET_ID,
        filename=FILE_NAME,
        repo_type="dataset"
    )

    return pd.read_parquet(file_path)

# ==================================================
# SESSION CACHE
# ==================================================
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

if df.empty:
    st.error("Dataset is empty")
    st.stop()

# ==================================================
# ENSURE COLUMNS EXIST
# ==================================================
for col in ["title", "company", "location"]:
    if col not in df.columns:
        df[col] = ""

# ==================================================
# HEADER
# ==================================================
colored_header(
    label="Workforce Intelligence Dashboard",
    description="Real-time labor market analytics • interactive exploration",
    color_name="blue-70"
)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:

    st.header("Control Panel")

    search = st.text_input(
        "Search Jobs",
        placeholder="Accountant, Data Analyst..."
    )

    locations = (
        ["All"]
        + sorted(
            df["location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    companies = (
        ["All"]
        + sorted(
            df["company"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    location = st.selectbox(
        "Location",
        locations
    )

    company = st.selectbox(
        "Company",
        companies
    )

    top_n = st.slider(
        "Top N Insights",
        min_value=5,
        max_value=20,
        value=10
    )

# ==================================================
# FILTER ENGINE
# ==================================================
filtered = df.copy()

if search.strip():

    filtered = filtered[
        filtered["title"]
        .fillna("")
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
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
coverage = round(
    len(filtered) / len(df) * 100,
    1
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Jobs",
    f"{len(filtered):,}"
)

c2.metric(
    "Companies",
    filtered["company"].nunique()
)

c3.metric(
    "Locations",
    filtered["location"].nunique()
)

c4.metric(
    "Coverage",
    f"{coverage}%"
)

style_metric_cards()

st.divider()

# ==================================================
# CHARTS
# ==================================================
left, right = st.columns(2)

with left:

    st.subheader("🏢 Top Companies")

    company_count = (
        filtered["company"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    company_count.columns = [
        "Company",
        "Jobs"
    ]

    fig = px.bar(
        company_count,
        x="Jobs",
        y="Company",
        orientation="h",
        color="Jobs"
    )

    fig.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("📍 Top Locations")

    location_count = (
        filtered["location"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    location_count.columns = [
        "Location",
        "Jobs"
    ]

    fig = px.bar(
        location_count,
        x="Jobs",
        y="Location",
        orientation="h",
        color="Jobs"
    )

    fig.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# DISTRIBUTION
# ==================================================
st.subheader("Market Distribution")

col1, col2 = st.columns(2)

with col1:

    pie_loc = (
        filtered["location"]
        .value_counts()
        .head(8)
    )

    fig = px.pie(
        names=pie_loc.index,
        values=pie_loc.values,
        hole=0.55
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    pie_comp = (
        filtered["company"]
        .value_counts()
        .head(8)
    )

    fig = px.pie(
        names=pie_comp.index,
        values=pie_comp.values,
        hole=0.55
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# DATA EXPLORER
# ==================================================
st.subheader("Data Explorer")

st.dataframe(
    filtered.head(1000),
    use_container_width=True,
    height=500
)

st.caption(
    f"Showing {min(len(filtered),1000):,} / {len(filtered):,} rows"
)

# ==================================================
# ASSISTANT
# ==================================================
st.subheader("Assistant")

question = st.text_input(
    "Ask about the job market"
)

if question:

    q = question.lower()

    if "company" in q:

        answer = (
            filtered["company"]
            .value_counts()
            .head(5)
            .to_string()
        )

    elif "location" in q:

        answer = (
            filtered["location"]
            .value_counts()
            .head(5)
            .to_string()
        )

    else:

        answer = (
            f"Current result set contains "
            f"{len(filtered):,} jobs."
        )

    st.info(answer)

# ==================================================
# SYSTEM STATUS
# ==================================================
with st.expander("System Status"):

    st.write(
        "Dataset Rows:",
        len(df)
    )

    st.write(
        "Cache TTL:",
        "3600 seconds"
    )

    st.write(
        "Dataset:",
        HF_DATASET_ID
    )

# ==================================================
# FOOTER
# ==================================================
st.caption(
    "Powered by Hugging Face • Streamlit • Plotly"
)