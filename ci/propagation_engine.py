# ci/propagation_engine.py

class DependencyGraph:
    """
    Maps file changes → system impacts
    Used by CI/CD orchestrator to decide what to run
    """

    def __init__(self):
        # file → impacted components
        self.map = {
            "dashboard.py": ["ui", "deploy"],
            "requirements.txt": ["env", "deploy"],
            "scraper.py": ["data", "pipeline", "deploy"],
            "upload_hf.py": ["data", "deploy"],
            "jobs.parquet": ["data", "ui", "deploy"],
            "ci/": ["pipeline", "deploy"]
        }

    def get_impacts(self, changed_files):
        """
        Convert changed files → impacted systems
        """
        impacts = set()

        for file in changed_files:
            for key in self.map.keys():

                # match exact file or folder prefix
                if file == key or file.startswith(key):
                    for impact in self.map[key]:
                        impacts.add(impact)

        return list(impacts)