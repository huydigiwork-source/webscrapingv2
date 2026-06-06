import subprocess


def changed_files():

    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True
    )

    return result.stdout.splitlines()


def run(cmd):

    print(f"\n▶ {cmd}")

    result = subprocess.run(
        cmd,
        shell=True
    )

    if result.returncode != 0:
        raise RuntimeError(cmd)


def main():

    files = changed_files()

    print("Changed Files:")
    print(files)

    scraper_changed = any(
        x in files
        for x in [
            "scraper.py",
            "skills.py",
            "hf_prepare_data.py"
        ]
    )

    dashboard_changed = any(
        x in files
        for x in [
            "dashboard.py",
            "requirements.txt"
        ]
    )

    if scraper_changed:

        print("\nDATA PIPELINE")

        run("python scraper.py")
        run("python upload_hf.py")

    if dashboard_changed:

        print("\nSPACE DEPLOY")

        run("python deploy_space.py")

    if not scraper_changed and not dashboard_changed:

        print("\nNothing to deploy")


if __name__ == "__main__":
    main()