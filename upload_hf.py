import os
from datetime import datetime
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = "Vincentran/careerviet-accounting-jobs"  # FIX cứng để tránh sai env

def upload():
    print("UPLOADING LATEST jobs.parquet → HF Dataset")

    api = HfApi(token=HF_TOKEN)

    # =========================
    # 1. FORCE OVERWRITE SINGLE SOURCE FILE
    # =========================
    api.upload_file(
        path_or_fileobj="jobs.parquet",
        path_in_repo="jobs.parquet",   # IMPORTANT: ONLY ONE SOURCE
        repo_id=DATASET_ID,
        repo_type="dataset",
        commit_message=f"FORCE LATEST DATA {datetime.now()}"
    )

    # =========================
    # 2. CREATE FORCE VERSION FILE (NOT DATA, JUST SIGNAL)
    # =========================
    with open("force_latest.txt", "w") as f:
        f.write("jobs.parquet")

    api.upload_file(
        path_or_fileobj="force_latest.txt",
        path_in_repo="force_latest.txt",
        repo_id=DATASET_ID,
        repo_type="dataset",
        commit_message="FORCE POINTER UPDATE"
    )

    print("UPLOAD DONE ✔")


if __name__ == "__main__":
    upload()