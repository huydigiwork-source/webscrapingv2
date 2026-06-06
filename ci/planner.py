# ci/planner.py

class ExecutionPlanner:

    def build_plan(self, impacts):

        plan = {
            "run_scraper": False,
            "run_pipeline": False,
            "run_upload": False,
            "run_dashboard": False,
            "run_deploy": False
        }

        # ======================
        # DATA LAYER
        # ======================
        if "data" in impacts:
            plan["run_scraper"] = True
            plan["run_pipeline"] = True
            plan["run_upload"] = True

        # ======================
        # UI LAYER
        # ======================
        if "ui" in impacts:
            plan["run_dashboard"] = True
            plan["run_deploy"] = True

        # ======================
        # PIPELINE LAYER
        # ======================
        if "pipeline" in impacts:
            plan["run_scraper"] = True
            plan["run_pipeline"] = True

        # ======================
        # DEPLOY ALWAYS SAFE RULE
        # ======================
        if "deploy" in impacts:
            plan["run_deploy"] = True

        return plan