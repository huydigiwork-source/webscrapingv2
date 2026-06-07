import os
from datetime import datetime
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
DATASET_ID = os.getenv("HF_DATASET_ID")

def upload():
    print("UPLOADING LATEST jobs.parquet → HF Dataset")

    api = HfApi(token=HF_TOKEN)

    api.upload_file(
        path_or_fileobj="jobs.parquet",
        path_in_repo="jobs.parquet",
        repo_id=DATASET_ID,
        repo_type="dataset",
        commit_message=f"update jobs.parquet {datetime.now()}"
    )

    print("UPLOAD DONE ✔")


if __name__ == "__main__":
    upload()