# ci/planner.py

class ExecutionPlanner:
    """
    Convert system impacts → execution plan
    """

    def build_plan(self, impacts):
        plan = {
            "run_scraper": False,
            "run_pipeline": False,
            "run_upload": False,
            "run_dashboard": False,
            "run_deploy": False,
            "rebuild_env": False
        }

        # =========================
        # DATA LAYER
        # =========================
        if "data" in impacts:
            plan["run_scraper"] = True
            plan["run_pipeline"] = True
            plan["run_upload"] = True

        # =========================
        # UI LAYER
        # =========================
        if "ui" in impacts:
            plan["run_dashboard"] = True
            plan["run_deploy"] = True

        # =========================
        # ENV LAYER
        # =========================
        if "env" in impacts:
            plan["rebuild_env"] = True
            plan["run_deploy"] = True

        # =========================
        # PIPELINE LAYER
        # =========================
        if "pipeline" in impacts:
            plan["run_scraper"] = True
            plan["run_pipeline"] = True

        # =========================
        # DEPLOY IS GLOBAL SAFE RULE
        # =========================
        if "deploy" in impacts:
            plan["run_deploy"] = True

        return plan