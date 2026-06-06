import os
from ci.agents.analyzer import analyze_changes
from ci.agents.risk_agent import evaluate_risk
from ci.agents.fix_agent import generate_fix
from ci.agents.validator import validate_fix
from ci.agents.deployer import deploy


def get_diff():
    os.system("git diff HEAD > diff.txt")
    return open("diff.txt", "r").read()


def run_swarm():
    diff = get_diff()

    print("\n🧠 ANALYZING...")
    analysis = analyze_changes(diff)

    print("\n⚠️ RISK EVALUATION...")
    risk = evaluate_risk(analysis)

    print("\n🔧 GENERATING FIX...")
    fix = generate_fix(risk, diff)

    print("\n🧪 VALIDATING FIX...")
    if not validate_fix(fix):
        print("❌ FIX INVALID → BLOCK DEPLOY")
        return False

    print("\n🚀 DEPLOYING...")
    deploy()

    print("\n✅ SWARM COMPLETE")
    return True


if __name__ == "__main__":
    run_swarm()