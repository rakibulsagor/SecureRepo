from typing import Dict

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

SEVERITY_PENALTIES: Dict[str, int] = {
    "Critical": 25,
    "High": 15,
    "Medium": 8,
    "Low": 3
}

def get_severity_penalty(severity: str) -> int:
    return SEVERITY_PENALTIES.get(severity, 0)
