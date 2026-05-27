import os
import re

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TEXT_EXTENSIONS = {".js", ".ts", ".py", ".json", ".txt", ".md", ".yml", ".yaml", ".env", ".html", ".css"}

BEGINNER_RULES = [
    {
        "pattern": r"(?i)debug\s*=\s*True|DEBUG\s*=\s*True|debug\s*:\s*true",
        "severity": "High",
        "message": "Debug mode is enabled in application code.",
        "fix": "Disable debug mode in production and control it with environment variables.",
    },
    {
        "pattern": r"^<<<<<<< HEAD|^=======$|^>>>>>>> [0-9a-fA-F]{40}",
        "severity": "Medium",
        "message": "Git merge conflict marker committed.",
        "fix": "Resolve the merge conflict, remove the markers, and commit clean code.",
    },
    {
        "pattern": r"(?i)(?:password|passwd|db_pass|mysql_password|postgres_password)\s*=\s*['\"](?:admin|root|password|123456|pass123|qwerty)['\"]",
        "severity": "High",
        "message": "Common insecure hardcoded password detected.",
        "fix": "Remove the hardcoded credential and load it from environment variables or a vault.",
    },
]


class BeginnerMistakeScanner:
    def scan(self, repo_path):
        findings = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
            for filename in files:
                full_path = os.path.join(root, filename)
                if not self._is_text_file(full_path):
                    continue

                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                        for line_number, line in enumerate(file, 1):
                            findings.extend(self._check_rules(relative_path, line_number, line))
                            findings.extend(self._check_local_paths(relative_path, line_number, line))
                except OSError:
                    continue
        return findings

    def _check_rules(self, relative_path, line_number, line):
        findings = []
        for rule in BEGINNER_RULES:
            if re.search(rule["pattern"], line):
                findings.append({
                    "type": "Beginner Mistake",
                    "severity": rule["severity"],
                    "file": relative_path,
                    "line": line_number,
                    "message": rule["message"],
                    "fix": rule["fix"],
                })
        return findings

    def _check_local_paths(self, relative_path, line_number, line):
        match = re.search(r"(?:[cC]:\\Users\\[a-zA-Z0-9_-]+|/home/[a-zA-Z0-9_-]+)/[a-zA-Z0-9_./-]+", line)
        if not match:
            return []
        return [{
            "type": "Beginner Mistake",
            "severity": "Low",
            "file": relative_path,
            "line": line_number,
            "message": f"Hardcoded local absolute path detected: {match.group(0)}.",
            "fix": "Use relative paths or build paths with pathlib instead of hardcoding machine-specific folders.",
        }]

    def _is_text_file(self, path):
        _, extension = os.path.splitext(path)
        return extension.lower() in TEXT_EXTENSIONS
