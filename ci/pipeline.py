import subprocess

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(cmd)


def get_changed_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True
    )
    return result.stdout.splitlines()


def main():
    print("START SMART PIPELINE")

    files = get_changed_files()
    print("Changed files:", files)

    # =========================
    # DEFINE CHANGE GROUPS
    # =========================
    data_files = ["scraper.py", "upload_hf.py", "hf_prepare_data.py"]
    ui_files = ["dashboard.py", "requirements.txt", "deploy_space.py"]

    data_related = any(f in files for f in data_files)
    ui_related = any(f in files for f in ui_files)

    # =========================
    # CASE 1: BOTH DATA + UI
    # =========================
    if data_related and ui_related:
        print("\n🔥 FULL PIPELINE (DATA + UI CHANGED)")

        run("python scraper.py")
        run("python upload_hf.py")
        run("python deploy_space.py")

    # =========================
    # CASE 2: ONLY DATA
    # =========================
    elif data_related:
        print("\n📦 DATA PIPELINE")

        run("python scraper.py")
        run("python upload_hf.py")

    # =========================
    # CASE 3: ONLY UI
    # =========================
    elif ui_related:
        print("\n🎨 UI PIPELINE")

        run("python deploy_space.py")

    # =========================
    # CASE 4: NOTHING
    # =========================
    else:
        print("\nNO ACTION - NOTHING CHANGED")

    print("\nDONE PIPELINE")


if __name__ == "__main__":
    main()