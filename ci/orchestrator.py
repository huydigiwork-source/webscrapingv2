import os
from ci.propagation_engine import DependencyGraph
from ci.planner import ExecutionPlanner
from ci.env_autobuild import build_env

def get_changed_files():
    os.system("git diff --name-only HEAD~1 HEAD > changes.txt")

    with open("changes.txt") as f:
        return f.read().splitlines()


changed_files = get_changed_files()

# 1. IMPACT DETECTION
graph = DependencyGraph()
impacts = graph.get_impacts(changed_files)

# 2. PLAN GENERATION
planner = ExecutionPlanner()
plan = planner.build_plan(impacts)

print("CHANGED:", changed_files)
print("IMPACTS:", impacts)
print("PLAN:", plan)

# 3. ENV AUTO SYNC
if plan["rebuild_env"]:
    build_env(changed_files)
    os.system("pip install -r requirements.auto.txt")

# 4. EXECUTION FLOW
if plan["run_scraper"]:
    os.system("python scraper.py")

if plan["run_pipeline"]:
    os.system("python run_pipeline.py")

if plan["run_upload"]:
    os.system("python upload_hf.py")

# 5. CRITICAL FIX: ALWAYS SYNC UI + DATA DEPLOY
if plan["run_dashboard"] or plan["run_upload"]:
    plan["run_deploy"] = True

if plan["run_deploy"]:
    os.system("python deploy_space.py")

print("PIPELINE COMPLETE")