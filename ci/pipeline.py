import subprocess

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(cmd)


def main():
    print("START PIPELINE")

    run("python scraper.py")
    run("python upload_hf.py")

    print("DONE PIPELINE")


if __name__ == "__main__":
    main()