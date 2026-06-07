import subprocess
import sys

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
    # FLAGS DETECTION
    # =========================
    data_related = any(f in files for f in ["scraper.py", "upload_hf.py"])
    ui_related = any(f in files for f in ["dashboard.py", "requirements.txt", "deploy_space.py", "style.css"])

    # =========================
    # NEW: COMBINED CASE
    # =========================
    both_updated = data_related and ui_related

    # =========================
    # PIPELINE LOGIC
    # =========================

    if both_updated:
        print("FULL PIPELINE (DATA + UI)")
        run("python scraper.py")
        run("python upload_hf.py")
        run("python deploy_space.py")
        print("DEPLOY COMPLETE: DATA + UI")

    else:

        if data_related:
            print("DATA PIPELINE")
            run("python scraper.py")
            run("python upload_hf.py")

        if ui_related:
            print("SPACE PIPELINE")
            run("python deploy_space.py")

        if not data_related and not ui_related:
            print("NO ACTION")

    print("DONE PIPELINE")


if __name__ == "__main__":
    main()