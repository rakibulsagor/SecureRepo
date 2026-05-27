import json
import os
import re

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TEXT_EXTENSIONS = {".js", ".jsx", ".ts", ".py", ".json", ".txt", ".md", ".yml", ".yaml", ".html", ".env"}


class VulnerableApiScanner:
    def __init__(self):
        self.rules = self._load_rules()

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
                            for rule in self.rules:
                                if re.search(rule["pattern"], line):
                                    findings.append({
                                        "type": "Vulnerable API",
                                        "severity": rule["severity"],
                                        "file": relative_path,
                                        "line": line_number,
                                        "message": rule["message"],
                                        "fix": rule["fix"],
                                    })
                except OSError:
                    continue
        return findings

    def _load_rules(self):
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vulnerable_api_rules.json")
        with open(rules_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _is_text_file(self, path):
        _, extension = os.path.splitext(path)
        return extension.lower() in TEXT_EXTENSIONS
