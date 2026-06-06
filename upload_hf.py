import os

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = os.getenv("HF_DATASET_ID")

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN")

if not DATASET_ID:
    raise RuntimeError(
        "Missing HF_DATASET_ID. Add it in GitHub Secrets → Actions"
    )