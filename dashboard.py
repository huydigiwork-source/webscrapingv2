# KPI SECTION

c1,c2,c3,c4 = st.columns(4)

metrics = [
("Jobs",f"{len(filtered):,}"),
("Companies",filtered["company"].nunique()),
("Locations",filtered["location"].nunique()),
("Coverage",f"{coverage}%")
]

for col,(title,value) in zip([c1,c2,c3,c4],metrics):
with col:
st.markdown(
f""" <div class="metric-card"> <h4>{title}</h4> <h2>{value}</h2> </div>
""",
unsafe_allow_html=True
)

st.markdown("<br>",unsafe_allow_html=True)

# TREEMAP

st.subheader("Market Structure")

treemap_data = (
filtered["company"]
.value_counts()
.head(30)
.reset_index()
)

treemap_data.columns=[
"Company",
"Jobs"
]

fig = px.treemap(
treemap_data,
path=["Company"],
values="Jobs",
color="Jobs"
)

fig.update_layout(
height=600
)

st.plotly_chart(
fig,
use_container_width=True
)

# COMPANY + LOCATION

left,right = st.columns(2)

with left:

```
company_data=(
    filtered["company"]
    .value_counts()
    .head(15)
    .reset_index()
)

company_data.columns=[
    "Company",
    "Jobs"
]

fig=px.bar(
    company_data,
    x="Jobs",
    y="Company",
    orientation="h",
    text="Jobs"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

with right:

```
location_data=(
    filtered["location"]
    .value_counts()
    .head(15)
    .reset_index()
)

location_data.columns=[
    "Location",
    "Jobs"
]

fig=px.pie(
    location_data,
    values="Jobs",
    names="Location",
    hole=.55
)

fig.update_traces(
    textinfo="percent+label"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

# SUNBURST

if "job_title" in filtered.columns:

```
tmp=(
    filtered["job_title"]
    .value_counts()
    .head(50)
    .reset_index()
)

tmp.columns=[
    "Job",
    "Count"
]

fig=px.sunburst(
    tmp,
    path=["Job"],
    values="Count"
)

fig.update_layout(
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```
