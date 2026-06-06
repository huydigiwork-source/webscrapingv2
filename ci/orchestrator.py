# ci/orchestrator.py

import os
from ci.propagation_engine import DependencyGraph
from ci.planner import ExecutionPlanner
from ci.env_autobuild import build_env


def get_changed_files():
    os.system("git diff --name-only HEAD~1 HEAD > changes.txt")

    try:
        with open("changes.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except:
        return []


def run_command(cmd):
    print(f"\n▶ {cmd}")
    result = os.system(cmd)
    if result != 0:
        print(f"❌ Command failed: {cmd}")
    return result


# =========================
# 1. DETECT CHANGES
# =========================
changed_files = get_changed_files()

print("\n===== CHANGED FILES =====")
print(changed_files)

# =========================
# 2. PROPAGATION ENGINE
# =========================
graph = DependencyGraph()
impacts = graph.get_impacts(changed_files)

print("\n===== IMPACTS =====")
print(impacts)

# =========================
# 3. EXECUTION PLAN
# =========================
planner = ExecutionPlanner()
plan = planner.build_plan(impacts)

print("\n===== EXECUTION PLAN =====")
print(plan)

# =========================
# 4. ENVIRONMENT LAYER
# =========================
if plan["rebuild_env"]:
    print("\n🧪 Rebuilding environment...")
    build_env(changed_files)
    run_command("pip install -r requirements.auto.txt")

# =========================
# 5. DATA PIPELINE
# =========================
if plan["run_scraper"]:
    run_command("python scraper.py")

if plan["run_pipeline"]:
    run_command("python run_pipeline.py")

if plan["run_upload"]:
    run_command("python upload_hf.py")

# =========================
# 6. UI + DEPLOY LAYER
# =========================
if plan["run_dashboard"]:
    print("\n🎨 Dashboard updated")

# ALWAYS SAFE RULE (CRITICAL FIX)
if plan["run_deploy"] or plan["run_upload"] or plan["run_dashboard"]:
    run_command("python deploy_space.py")

print("\n===== PIPELINE COMPLETE =====")