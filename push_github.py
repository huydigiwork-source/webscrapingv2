import git
import os


def push_to_github():
    repo_path = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("🚀 START PUSHING TO GITHUB - ONLY UPDATED FILES")
    print(f"📁 Directory: {repo_path}")
    print("=" * 60)

    # Check if Git repo exists
    try:
        repo = git.Repo(repo_path)
        print("✅ Git repo opened successfully")
    except git.exc.InvalidGitRepositoryError:
        print("❌ Error: No Git repo in this directory!")
        print("\n💡 Solution:")
        print("   1. Open Git Bash in the project folder")
        print("   2. Run: git init")
        print("   3. Place push_smart.py in this folder")
        input("\nPress Enter to exit...")
        return

    # Get list of changed files (modified + untracked)
    changed_files = []

    # Modified files (already tracked)
    for item in repo.index.diff(None):
        changed_files.append(item.a_path)

    # Untracked files (new)
    untracked = repo.untracked_files
    changed_files.extend(untracked)

    if not changed_files:
        print("\nℹ️ No files changed!")
        print("   No need to push.")
        input("\nPress Enter to exit...")
        return

    print(f"\n✅ Found {len(changed_files)} changed files:")
    for i, file in enumerate(changed_files, 1):
        print(f"   {i}. {file}")

    try:
        # Add only changed files
        repo.index.add(changed_files)
        print(f"\n✅ Added {len(changed_files)} files: git add [files]")

        # Commit
        repo.index.commit("fix CI validation")
        print("✅ Committed: git commit -m 'fix CI validation'")

        # Push
        origin = repo.remotes.origin
        push_info = origin.push()

        if push_info[0].success:
            print("✅✅ PUSH SUCCESSFUL!")
            print(f"📊 Branch: {repo.active_branch} → origin/{repo.active_branch}")
            print(f"📦 Pushed {len(changed_files)} files:")
            for file in changed_files:
                print(f"   - {file}")
        else:
            print(f"❌ Push failed: {push_info[0].summary}")
            print("\n💡 Check:")
            print("   - SSH key / GitHub credential")
            print("   - Internet connection")
            print("   - Branch exists on GitHub")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Check:")
        print("   - SSH key / GitHub credential")
        print("   - Internet connection")

    print("=" * 60)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    push_to_github()