import os

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("❌ Missing HF_TOKEN (GitHub Secret not injected)")


def upload():
    print("Uploading dataset to Hugging Face...")
    # TODO: add real upload logic here
    print("Upload done")


if __name__ == "__main__":
    upload()