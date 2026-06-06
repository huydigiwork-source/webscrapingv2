import os
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = os.getenv("HF_DATASET_ID")

PARQUET_FILE = "jobs.parquet"

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN")

if not DATASET_ID:
    raise RuntimeError("Missing HF_DATASET_ID")

if not os.path.exists(PARQUET_FILE):
    raise FileNotFoundError(PARQUET_FILE)

api = HfApi(token=HF_TOKEN)

api.upload_file(
    path_or_fileobj=PARQUET_FILE,
    path_in_repo="jobs.parquet",
    repo_id=DATASET_ID,
    repo_type="dataset"
)

print("Dataset uploaded")