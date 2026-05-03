import pandas as pd

def build_report_dataframe(analysis: dict, scores: dict, ai_names: list) -> pd.DataFrame:
    """Build a pandas DataFrame for display."""
    rows = []
    for brand, data in analysis.items():
        row = {"Brand": brand, "Score": scores.get(brand, 0)}
        for ai in ai_names:
            if ai in data["mentioned_by"]:
                pos = data["positions"].get(ai, "✅")
                row[ai] = f"✅ {pos}"
            else:
                row[ai] = "❌"
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)
    df.index += 1  # Rank starts at 1
    return df


def get_score_color(score: int) -> str:
    if score >= 70:
        return "green"
    elif score >= 40:
        return "orange"
    else:
        return "red"