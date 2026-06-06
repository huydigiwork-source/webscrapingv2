# ci/orchestrator.py

import os
from ci.propagation_engine import DependencyGraph
from ci.planner import ExecutionPlanner


def get_changed_files():
    os.system("git diff --name-only HEAD~1 HEAD > changes.txt")

    try:
        with open("changes.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []


def run(cmd):
    print(f"\n▶ {cmd}")
    return os.system(cmd)


# =========================
# 1. GET CHANGES
# =========================
changed_files = get_changed_files()
print("CHANGED FILES:", changed_files)

# =========================
# 2. PROPAGATION ENGINE
# =========================
graph = DependencyGraph()
impacts = graph.get_impacts(changed_files)

print("IMPACTS:", impacts)

# =========================
# 3. PLANNER
# =========================
planner = ExecutionPlanner()
plan = planner.build_plan(impacts)

print("PLAN:", plan)

# =========================
# 4. EXECUTION LAYER
# =========================
if plan["run_scraper"]:
    run("python scraper.py")

if plan["run_pipeline"]:
    run("python run_pipeline.py")

if plan["run_upload"]:
    run("python upload_hf.py")

if plan["run_dashboard"]:
    print("Dashboard updated")

# =========================
# 5. DEPLOY RULE (UNIFIED)
# =========================
if plan["run_deploy"] or plan["run_upload"] or plan["run_dashboard"]:
    run("python deploy_space.py")

print("\nPIPELINE COMPLETE")