def analyze_changes(diff: str):
    return {
        "summary": "Code changes detected",
        "has_ci_change": "workflow" in diff,
        "has_path_change": "Save Data" in diff,
        "has_deploy_change": "deploy" in diff
    }