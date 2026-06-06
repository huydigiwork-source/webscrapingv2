import os
import ast
from collections import defaultdict

class AutoPilotCI:

    def __init__(self):
        self.change_map = {
            "scraper": ["scraper.py"],
            "data": ["jobs.parquet", "pipeline/", "upload_hf.py"],
            "dashboard": ["dashboard.py", "requirements.txt"],
            "env": ["*.py"]
        }

    def detect_changes(self):
        os.system("git diff --name-only HEAD~1 HEAD > changes.txt")

        with open("changes.txt", "r") as f:
            changed = f.read().splitlines()

        return changed

    def infer_intent(self, changed_files):
        intent = {
            "run_scraper": False,
            "run_pipeline": False,
            "run_dashboard": False,
            "update_env": False
        }

        for f in changed_files:

            if "scraper.py" in f:
                intent["run_scraper"] = True
                intent["run_pipeline"] = True

            if "upload_hf.py" in f or "jobs.parquet" in f:
                intent["run_pipeline"] = True

            if "dashboard.py" in f:
                intent["run_dashboard"] = True

            if f.endswith(".py"):
                intent["update_env"] = True

        return intent