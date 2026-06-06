import os

# FILE TRIGGER MAP (SINGLE SOURCE OF TRUTH)
DEPLOY_FILES = {
    "dashboard.py",
    "scraper.py",
    "upload_hf.py",
    "run_pipeline.py",
    "requirements.txt",
    "jobs.parquet"
}


def get_changed_files():
    """
    Safe Git diff (works even first commit)
    """
    os.system("git fetch --prune --unshallow 2>/dev/null || true")

    os.system("git diff --name-only HEAD^ HEAD > changes.txt 2>/dev/null || git diff --name-only HEAD > changes.txt")

    try:
        with open("changes.txt", "r") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return []


def should_deploy(files):
    return any(
        any(trigger in f for trigger in DEPLOY_FILES)
        for f in files
    )


def run(cmd):
    print(f"\n▶ {cmd}")
    return os.system(cmd)


# =========================
# MAIN PIPELINE
# =========================
changed_files = get_changed_files()

print("CHANGED FILES:", changed_files)

if should_deploy(changed_files):
    print("\n🚀 DEPLOY TRIGGERED")

    run("python scraper.py")
    run("python upload_hf.py")
    run("python deploy_space.py")

else:
    print("\n🟡 No deploy needed")

print("\nDONE")