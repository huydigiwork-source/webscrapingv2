import subprocess


def run(cmd):

    result = subprocess.run(
        cmd,
        shell=True
    )

    if result.returncode != 0:
        raise RuntimeError(cmd)


def deploy_dataset():

    run("python upload_hf.py")


def deploy_space():

    run("python deploy_space.py")