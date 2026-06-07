import os
from datetime import datetime
from huggingface_hub import HfApi, login

# =========================
# CONFIG
# =========================
DATASET_ID = "Vincentran/careerviet-job-market"
LOCAL_FILE = "jobs.parquet"
VERSION_FILE = "latest_version.txt"

HF_TOKEN = os.getenv("HF_TOKEN")


# =========================
# AUTH
# =========================
def hf_login():
    if HF_TOKEN:
        login(token=HF_TOKEN)
        print("HF login via token ✔")
    else:
        login()
        print("HF login via CLI ✔")


# =========================
# UPLOAD LOGIC
# =========================
def upload_dataset():
    print("\n🚀 START UPLOADING DATASET TO HUGGINGFACE")

    api = HfApi(token=HF_TOKEN)

    # 1. CHECK FILE EXISTS
    if not os.path.exists(LOCAL_FILE):
        raise FileNotFoundError(f"{LOCAL_FILE} not found")

    # 2. OPTIONAL: DELETE OLD FILE (ignore errors)
    try:
        api.delete_file(
            path_in_repo=LOCAL_FILE,
            repo_id=DATASET_ID,
            repo_type="dataset"
        )
        print("🧹 Old file deleted")
    except Exception as e:
        print(f"⚠️ No old file or already clean: {e}")

    # 3. UPLOAD MAIN PARQUET FILE
    api.upload_file(
        path_or_fileobj=LOCAL_FILE,
        path_in_repo=LOCAL_FILE,
        repo_id=DATASET_ID,
        repo_type="dataset",
        commit_message=f"Update jobs dataset - {datetime.now().isoformat()}"
    )
    print("📦 jobs.parquet uploaded")

    # 4. WRITE VERSION MARKER (optional but useful for debugging HF cache)
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"Last update: {datetime.now().isoformat()}")

    api.upload_file(
        path_or_fileobj=VERSION_FILE,
        path_in_repo=VERSION_FILE,
        repo_id=DATASET_ID,
        repo_type="dataset",
        commit_message="Update version marker"
    )

    # 5. CLEAN LOCAL VERSION FILE
    os.remove(VERSION_FILE)

    print("✅ UPLOAD COMPLETED SUCCESSFULLY")
    print("👉 Dataset:", f"https://huggingface.co/datasets/{DATASET_ID}")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    hf_login()
    upload_dataset()