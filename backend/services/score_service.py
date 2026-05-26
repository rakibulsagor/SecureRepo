from typing import List
from backend.models.issue_models import Issue

def calculate_score(issues: List[Issue]) -> int:
    score = 100

    penalties = {
        "Critical": 25,
        "High": 15,
        "Medium": 8,
        "Low": 3
    }

    for issue in issues:
        score -= penalties.get(issue.severity, 0)

    return max(score, 0)

def get_risk_level(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Medium Risk"
    if score >= 25:
        return "High Risk"
    return "Critical Risk"
