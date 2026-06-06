# ci/propagation_engine.py

class DependencyGraph:

    def __init__(self):
        self.map = {
            "dashboard.py": ["ui", "deploy"],
            "requirements.txt": ["deploy"],
            "scraper.py": ["data", "pipeline", "deploy"],
            "upload_hf.py": ["data", "deploy"],
            "run_pipeline.py": ["pipeline", "deploy"],
            "jobs.parquet": ["data", "ui", "deploy"]
        }

    def get_impacts(self, changed_files):
        impacts = set()

        for f in changed_files:
            for key in self.map:
                if f == key or f.startswith(key):
                    impacts.update(self.map[key])

        return list(impacts)