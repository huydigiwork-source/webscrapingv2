import os
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
SPACE_ID = os.getenv("HF_SPACE_ID")

if not HF_TOKEN:
    raise RuntimeError("Missing HF_TOKEN")

if not SPACE_ID:
    raise RuntimeError("Missing HF_SPACE_ID")

api = HfApi(token=HF_TOKEN)


def deploy_space():
    print("🚀 Deploying Hugging Face Space...")

    api.upload_folder(
        folder_path=".",
        repo_id=SPACE_ID,
        repo_type="space"
    )

    print("✅ Space uploaded")

    # VERIFY DEPLOY
    info = api.space_info(SPACE_ID)
    print(f"🔎 Space status: {info.id}")


if __name__ == "__main__":
    deploy_space()