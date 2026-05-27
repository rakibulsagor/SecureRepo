import json
import os
import re

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


class RiskyFileScanner:
    def __init__(self):
        self.rules = self._load_rules()

    def scan(self, repo_path):
        findings = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
            for filename in files:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                for rule in self.rules:
                    if re.match(rule["pattern"], filename) or re.match(rule["pattern"], relative_path):
                        findings.append({
                            "type": "Risky File",
                            "severity": rule["severity"],
                            "file": relative_path,
                            "line": None,
                            "message": rule["message"],
                            "fix": rule["fix"],
                        })
                        break
        return findings

    def _load_rules(self):
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "risky_files.json")
        with open(rules_path, "r", encoding="utf-8") as file:
            return json.load(file)
