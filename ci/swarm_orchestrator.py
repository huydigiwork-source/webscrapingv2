import subprocess


def run(cmd):

    print(f"\n▶ {cmd}")

    result = subprocess.run(
        cmd,
        shell=True
    )

    if result.returncode != 0:
        raise RuntimeError(cmd)


def get_commit_message():

    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


def auto_mode():

    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True
    )

    files = result.stdout.splitlines()

    print("\nChanged Files:")
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
            "requirements.txt",
            "deploy_space.py"
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


def main():

    commit_msg = get_commit_message()

    print("\nCommit:")
    print(commit_msg)

    if "[dashboard]" in commit_msg:

        print("\nMODE = DASHBOARD")

        run("python deploy_space.py")

        return

    if "[scrape]" in commit_msg:

        print("\nMODE = SCRAPE")

        run("python scraper.py")
        run("python upload_hf.py")

        return

    if "[full]" in commit_msg:

        print("\nMODE = FULL")

        run("python scraper.py")
        run("python upload_hf.py")
        run("python deploy_space.py")

        return

    print("\nMODE = AUTO")

    auto_mode()


if __name__ == "__main__":
    main()