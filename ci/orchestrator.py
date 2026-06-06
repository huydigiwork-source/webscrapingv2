import os


DEPLOY_TRIGGERS = {
    "dashboard.py",
    "scraper.py",
    "upload_hf.py",
    "requirements.txt",
    "run_pipeline.py",
    "jobs.parquet"
}


def get_changed_files():
    os.system("git diff --name-only HEAD~1 HEAD > changes.txt")

    try:
        with open("changes.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []


def should_deploy(changed_files):
    return any(
        any(trigger in file for trigger in DEPLOY_TRIGGERS)
        for file in changed_files
    )


def run(cmd):
    print(f"\n▶ {cmd}")
    return os.system(cmd)


# =========================
# 1. Detect changes
# =========================
changed_files = get_changed_files()

print("CHANGED FILES:", changed_files)

# =========================
# 2. SIMPLE RULE ENGINE
# =========================
if should_deploy(changed_files):
    print("\n🚀 Changes detected → Deploying HF Space")
    run("python deploy_space.py")
else:
    print("\n🟡 No deploy-related changes → skip deploy")

print("\nDONE")