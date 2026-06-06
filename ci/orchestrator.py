from ci.autopilot_engine import AutoPilotCI
from ci.env_autobuild import build_env
import os

ci = AutoPilotCI()

changed = ci.detect_changes()
intent = ci.infer_intent(changed)

print("CHANGED:", changed)
print("INTENT:", intent)

# =====================
# 1. ENV AUTO BUILD
# =====================
if intent["update_env"]:
    build_env(changed)
    os.system("pip install -r requirements.auto.txt")

# =====================
# 2. SCRAPER
# =====================
if intent["run_scraper"]:
    os.system("python scraper.py")

# =====================
# 3. PIPELINE / DAG
# =====================
if intent["run_pipeline"]:
    os.system("python run_pipeline.py")

# =====================
# 4. DASHBOARD
# =====================
if intent["run_dashboard"]:
    print("Dashboard updated → no pipeline rerun needed")

print("CI DONE")