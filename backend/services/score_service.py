SEVERITY_WEIGHTS = {
    "Critical": 25,
    "High": 15,
    "Medium": 8,
    "Low": 3,
}


class ScoreService:
    def calculate_score(self, findings):
        penalty = 0
        for finding in findings:
            penalty += SEVERITY_WEIGHTS.get(finding.get("severity", "Low"), 3)
        return max(0, 100 - penalty)

    def risk_level(self, score):
        if score >= 90:
            return "Low"
        if score >= 75:
            return "Medium"
        if score >= 50:
            return "High"
        return "Critical"

    def summarize(self, findings):
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for finding in findings:
            severity = finding.get("severity", "Low").lower()
            if severity in summary:
                summary[severity] += 1
        return summary
