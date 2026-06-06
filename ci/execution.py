import os

WATCH = {
    "scraper.py",
    "dashboard.py",
    "upload_hf.py",
    "deploy_space.py",
    "requirements.txt",
    "data/jobs.parquet"
}


def get_changes():
    os.system("git fetch --prune --unshallow 2>/dev/null || true")
    os.system("git diff --name-only HEAD^ HEAD > changes.txt 2>/dev/null || git diff --name-only HEAD > changes.txt")

    with open("changes.txt", "r") as f:
        return [x.strip() for x in f if x.strip()]


def run(cmd):
    print(f"\n▶ {cmd}")
    code = os.system(cmd)
    if code != 0:
        raise RuntimeError(f"❌ Failed: {cmd}")


def should_run(files):
    return any(any(w in f for w in WATCH) for f in files)


files = get_changes()

print("CHANGED:", files)

if should_run(files):
    print("🚀 START PIPELINE")

    run("python scraper.py")
    run("python upload_hf.py")
    run("python deploy_space.py")

    print("🎉 PIPELINE SUCCESS (REAL DEPLOY DONE)")
else:
    print("🟡 No deploy needed")