from huggingface_hub import HfApi, login
import os

# =========================
# TOKEN
# =========================
HF_TOKEN = os.environ["HF_TOKEN"]
login(token=HF_TOKEN)

api = HfApi(token=HF_TOKEN)

# =========================
# CONFIG
# =========================
SPACE_ID = "Vincentran/careerviet-dashboard"

# ⚠️ FIX: MUST USE docker (không dùng streamlit)
SDK = "docker"

print("🚀 Creating HF Space (Docker mode)...")

# =========================
# 1. CREATE SPACE
# =========================
api.create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk=SDK,
    exist_ok=True
)

print("✅ Space ready:", SPACE_ID)

# =========================
# 2. FILE LIST (PRODUCTION)
# =========================
files = [
    "app.py",
    "api.py",
    "requirements.txt",
    "Dockerfile"
]

# optional: chỉ upload nếu file tồn tại
for f in files:
    if os.path.exists(f):
        api.upload_file(
            path_or_fileobj=f,
            path_in_repo=f,
            repo_id=SPACE_ID,
            repo_type="space"
        )
        print(f"📤 Uploaded: {f}")
    else:
        print(f"⚠️ Skipped (not found): {f}")

# =========================
# 3. RESULT
# =========================
print("\n🚀 SPACE DEPLOYED SUCCESSFULLY (DOCKER MODE)")
print("👉 URL:", f"https://huggingface.co/spaces/{SPACE_ID}")