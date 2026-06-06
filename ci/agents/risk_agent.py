def evaluate_risk(analysis):
    risk_score = 0

    if analysis["has_ci_change"]:
        risk_score += 2

    if analysis["has_path_change"]:
        risk_score += 3

    if analysis["has_deploy_change"]:
        risk_score += 2

    if risk_score >= 5:
        return {"level": "HIGH"}
    if risk_score >= 3:
        return {"level": "MEDIUM"}

    return {"level": "LOW"}