import os
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = os.getenv("HF_DATASET_ID")

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN")

if not DATASET_ID:
    raise RuntimeError("Missing HF_DATASET_ID")

api = HfApi(token=HF_TOKEN)


def upload_dataset():
    print("📦 Uploading dataset to Hugging Face...")

    api.upload_file(
        path_or_fileobj="data/jobs.parquet",
        path_in_repo="jobs.parquet",
        repo_id=DATASET_ID,
        repo_type="dataset"
    )

    print("✅ Dataset uploaded successfully")

    # VERIFY
    info = api.dataset_info(DATASET_ID)
    print(f"🔎 Dataset verified: {info.id}")


if __name__ == "__main__":
    upload_dataset()