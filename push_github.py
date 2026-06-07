import git
import os

# Đường dẫn thư mục project (tự động lấy thư mục đang chạy)
repo_path = os.path.dirname(os.path.abspath(__file__))

try:
    # Mở repo Git
    repo = git.Repo(repo_path)

    # Add tất cả file
    repo.index.add(['*'])
    print("✅ Đã add tất cả file")

    # Commit
    repo.index.commit("fix CI validation")
    print("✅ Đã commit")

    # Push lên origin/main
    origin = repo.remotes.origin
    origin.push()
    print("✅✅ Push thành công lên GitHub!")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    input("Nhấn Enter để thoát...")