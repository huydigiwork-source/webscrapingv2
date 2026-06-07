import pandas as pd
import numpy as np

from huggingface_hub import hf_hub_download

from dash import Dash
from dash import html
from dash import dcc

import dash_ag_grid as dag
import dash_mantine_components as dmc

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import plotly.express as px

# =====================================================

# CONFIG

# =====================================================

HF_DATASET_ID = "Vincentran/careerviet-job-market"
FILE_NAME = "jobs.parquet"

# =====================================================

# LOAD DATA

# =====================================================

file_path = hf_hub_download(
repo_id=HF_DATASET_ID,
filename=FILE_NAME,
repo_type="dataset"
)

df = pd.read_parquet(file_path)

for col in ["title", "company", "location"]:
if col not in df.columns:
df[col] = ""

# =====================================================

# ML CLUSTERING

# =====================================================

try:

```
titles = (
    df["title"]
    .fillna("")
    .astype(str)
)

tfidf = TfidfVectorizer(
    max_features=100
)

X = tfidf.fit_transform(titles)

n_clusters = min(
    5,
    max(2, len(df) // 100)
)

km = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init=10
)

df["cluster"] = km.fit_predict(X)
```

except Exception:

```
df["cluster"] = 0
```

# =====================================================

# KPIs

# =====================================================

total_jobs = len(df)
total_companies = df["company"].nunique()
total_locations = df["location"].nunique()

# =====================================================

# CHARTS

# =====================================================

company_chart = px.bar(
df["company"]
.value_counts()
.head(10)
.reset_index(),
x="count",
y="company",
orientation="h",
template="plotly_dark",
title="Top Hiring Companies"
)

location_chart = px.bar(
df["location"]
.value_counts()
.head(10)
.reset_index(),
x="count",
y="location",
orientation="h",
template="plotly_dark",
title="Top Hiring Locations"
)

cluster_chart = px.pie(
df["cluster"]
.value_counts()
.reset_index(),
names="cluster",
values="count",
template="plotly_dark",
title="Job Market Segments"
)

# =====================================================

# GRID

# =====================================================

column_defs = []

for c in df.columns:
column_defs.append(
{
"field": c,
"filter": True,
"sortable": True
}
)

# =====================================================

# APP

# =====================================================

app = Dash(**name**)

app.layout = dmc.MantineProvider(

```
children=[

    dmc.Container(

        fluid=True,

        children=[

            dmc.Space(h=20),

            dmc.Title(
                "Workforce Intelligence Platform",
                order=1
            ),

            dmc.Text(
                "AI-driven labor market analytics"
            ),

            dmc.Space(h=20),

            dmc.Grid(

                children=[

                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text("Jobs"),
                                dmc.Title(
                                    f"{total_jobs:,}",
                                    order=2
                                )
                            ],
                            p="md",
                            shadow="md"
                        ),
                        span=4
                    ),

                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text("Companies"),
                                dmc.Title(
                                    f"{total_companies:,}",
                                    order=2
                                )
                            ],
                            p="md",
                            shadow="md"
                        ),
                        span=4
                    ),

                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text("Locations"),
                                dmc.Title(
                                    f"{total_locations:,}",
                                    order=2
                                )
                            ],
                            p="md",
                            shadow="md"
                        ),
                        span=4
                    )

                ]

            ),

            dmc.Space(h=20),

            dmc.Grid(

                children=[

                    dmc.GridCol(
                        dcc.Graph(
                            figure=company_chart
                        ),
                        span=6
                    ),

                    dmc.GridCol(
                        dcc.Graph(
                            figure=location_chart
                        ),
                        span=6
                    )

                ]

            ),

            dmc.Space(h=20),

            dcc.Graph(
                figure=cluster_chart
            ),

            dmc.Space(h=20),

            dmc.Title(
                "Data Explorer",
                order=2
            ),

            dag.AgGrid(
                rowData=df.head(5000).to_dict("records"),
                columnDefs=column_defs,
                defaultColDef={
                    "resizable": True,
                    "filter": True,
                    "sortable": True
                },
                style={
                    "height": "700px"
                }
            )

        ]

    )

]
```

)

server = app.server

if **name** == "**main**":
app.run(
host="0.0.0.0",
port=7860,
debug=False
)
