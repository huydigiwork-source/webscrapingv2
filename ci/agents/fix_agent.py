def generate_fix(risk, diff):
    if risk["level"] == "HIGH":
        return "auto_fix_required: normalize paths + fix CI entrypoint"

    if risk["level"] == "MEDIUM":
        return "warn_only_no_auto_fix"

    return "no_fix_needed"