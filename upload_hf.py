from huggingface_hub import HfApi, login
from datasets import Dataset
import pandas as pd
import os
from hf_prepare_data import prepare

HF_TOKEN = os.environ["HF_TOKEN"]
REPO_ID = "Vincentran/careerviet-accounting-jobs"

login(token=HF_TOKEN)
api = HfApi(token=HF_TOKEN)

print("🚀 HF DATA PLATFORM V2 START")

# =========================
# LOAD + PREPARE DATA
# =========================
df = pd.read_parquet("jobs.parquet")

df = prepare(df)

# convert safe type
df = df.fillna("").astype(str)

print(f"📦 Ready dataset: {len(df)} rows")

# =========================
# CREATE HF DATASET
# =========================
api.create_repo(
    repo_id=REPO_ID,
    repo_type="dataset",
    exist_ok=True
)

dataset = Dataset.from_pandas(df, preserve_index=False)

dataset.push_to_hub(
    REPO_ID,
    token=HF_TOKEN
)

print("✅ HF V2 DATA UPLOADED")