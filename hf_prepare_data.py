import pandas as pd

def prepare(df: pd.DataFrame):

    # =========================
    # CLEAN BASIC
    # =========================
    df = df.fillna("")
    df = df.reset_index(drop=True)

    # =========================
    # STANDARDIZE COLUMNS
    # =========================
    df.columns = [c.lower().strip() for c in df.columns]

    # =========================
    # FEATURE ENGINEERING (ANALYTICS READY)
    # =========================

    # skill count
    if "market_skill" in df.columns:
        df["skill_count"] = df["market_skill"].apply(
            lambda x: len(str(x).split(",")) if x else 0
        )

    # experience bucket
    if "experience" in df.columns:
        df["exp_level"] = df["experience"].apply(
            lambda x: "Junior" if "1" in str(x)
            else "Mid" if "2" in str(x) or "3" in str(x)
            else "Senior"
        )

    # salary flag
    if "salary" in df.columns:
        df["has_salary"] = df["salary"].apply(
            lambda x: 0 if "Thỏa thuận" in str(x) else 1
        )

    return df