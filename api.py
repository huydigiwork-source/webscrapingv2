from fastapi import FastAPI
from datasets import load_dataset
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

app = FastAPI()

# LOAD DATA
df = pd.DataFrame(load_dataset(
    "Vincentran/careerviet-accounting-jobs",
    split="train"
)).fillna("")

model = SentenceTransformer("all-MiniLM-L6-v2")

corpus = (
    df["job_title"] + " " +
    df["company"] + " " +
    df["location"] + " " +
    df["market_skill"]
).tolist()

embeddings = model.encode(corpus)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

@app.get("/search")
def search(q: str):

    q_emb = model.encode([q])
    D, I = index.search(np.array(q_emb), 5)

    return df.iloc[I[0]].to_dict(orient="records")