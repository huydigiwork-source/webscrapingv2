import os

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("❌ Missing HF_TOKEN (GitHub Secret not injected)")


def deploy():
    print("Deploying to Hugging Face Space...")

    # placeholder deploy logic
    # (you can later replace with huggingface_hub API)
    print("Deploy success")


if __name__ == "__main__":
    deploy()