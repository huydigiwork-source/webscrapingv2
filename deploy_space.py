from huggingface_hub import HfApi, login
import os

HF_TOKEN = os.environ["HF_TOKEN"]

# =========================
# CONFIG
# =========================
SPACE_ID = "Vincentran/careerviet-dashboard"
SDK = "streamlit"

login(token=HF_TOKEN)

api = HfApi(token=HF_TOKEN)

print("🚀 Creating HF Space...")

# =========================
# 1. CREATE SPACE (AUTO)
# =========================
api.create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk=SDK,
    exist_ok=True
)

print("✅ Space ready:", SPACE_ID)

# =========================
# 2. UPLOAD APP FILES
# =========================
files = [
    "app.py",
    "requirements.txt"
]

for f in files:
    api.upload_file(
        path_or_fileobj=f,
        path_in_repo=f,
        repo_id=SPACE_ID,
        repo_type="space"
    )
    print(f"📤 Uploaded: {f}")

print("\n🚀 SPACE DEPLOYED SUCCESSFULLY")
print("👉 URL:", f"https://huggingface.co/spaces/{SPACE_ID}")