import os

def deploy():
    print("Pushing to GitHub + Hugging Face...")

    os.system("git add .")
    os.system('git commit -m "auto: swarm deploy" || true')
    os.system("git push origin main || true")

    print("Deploy triggered")