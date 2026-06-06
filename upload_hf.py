import os
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = os.getenv("HF_DATASET_ID")

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN")

if not DATASET_ID:
    raise RuntimeError("Missing HF_DATASET_ID")

api = HfApi(token=HF_TOKEN)


def upload():
    print("Uploading dataset...")

    api.upload_file(
        path_or_fileobj="data/jobs.parquet",
        path_in_repo="jobs.parquet",
        repo_id=DATASET_ID,
        repo_type="dataset"
    )

    print("Dataset uploaded OK")


if __name__ == "__main__":
    upload()