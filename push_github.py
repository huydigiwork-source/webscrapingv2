import git
import os


def push_to_github():
    repo_path = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("🚀 BẮT ĐẦU PUSH LÊN GITHUB - CHỈ FILE UPDATE")
    print(f"📁 Thư mục: {repo_path}")
    print("=" * 60)

    # Check có Git repo không
    try:
        repo = git.Repo(repo_path)
        print("✅ Đã mở Git repo")
    except git.exc.InvalidGitRepositoryError:
        print("❌ Lỗi: Chưa có Git repo trong folder này!")
        print("\n💡 Giải pháp:")
        print("   1. Mở Git Bash trong folder project")
        print("   2. Chạy: git init")
        print("   3. Đặt file push_smart.py trong folder này")
        input("\nNhấn Enter để thoát...")
        return

    # Lấy danh sách file đã thay đổi (modified + untracked)
    changed_files = []

    # File đã modified (đã tracked)
    for item in repo.index.diff(None):
        changed_files.append(item.a_path)

    # File untracked (mới)
    untracked = repo.untracked_files
    changed_files.extend(untracked)

    if not changed_files:
        print("\nℹ️ Không có file nào thay đổi!")
        print("   Không cần push.")
        input("\nNhấn Enter để thoát...")
        return

    print(f"\n✅ Có {len(changed_files)} file thay đổi:")
    for i, file in enumerate(changed_files, 1):
        print(f"   {i}. {file}")

    try:
        # Add chỉ các file thay đổi
        repo.index.add(changed_files)
        print(f"\n✅ Đã add {len(changed_files)} file: git add [files]")

        # Commit
        repo.index.commit("fix CI validation")
        print("✅ Đã commit: git commit -m 'fix CI validation'")

        # Push
        origin = repo.remotes.origin
        push_info = origin.push()

        if push_info[0].success:
            print("✅✅ PUSH THÀNH CÔNG!")
            print(f"📊 Branch: {repo.active_branch} → origin/{repo.active_branch}")
            print(f"📦 Đã push {len(changed_files)} file:")
            for file in changed_files:
                print(f"   - {file}")
        else:
            print(f"❌ Push failed: {push_info[0].summary}")
            print("\n💡 Kiểm tra:")
            print("   - SSH key / GitHub credential")
            print("   - Internet connection")
            print("   - Branch tồn tại trên GitHub")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("\n💡 Kiểm tra:")
        print("   - SSH key / GitHub credential")
        print("   - Internet connection")

    print("=" * 60)
    input("\nNhấn Enter để thoát...")


if __name__ == "__main__":
    push_to_github()