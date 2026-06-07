import os
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
SPACE_ID = os.getenv("HF_SPACE_ID")

api = HfApi(token=HF_TOKEN)

FILES = [
    "dashboard.py",
    "requirements.txt",
    "api.py",
    "style.css"
]

for file in FILES:

    if not os.path.exists(file):
        continue

    print(f"Uploading {file}")

    api.upload_file(
        path_or_fileobj=file,
        path_in_repo=file,
        repo_id=SPACE_ID,
        repo_type="space"
    )

print("Space deployed")