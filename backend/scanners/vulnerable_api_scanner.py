import json
import os
import re
from typing import List
from backend.models.issue_models import Issue
from backend.utils.file_filters import is_text_file, should_scan_dir, should_scan_file


class VulnerableApiScanner:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(dir_path, "data", "vulnerable_api_rules.json")
            if os.path.exists(rules_path):
                with open(rules_path, "r", encoding="utf-8") as f:
                    self.rules = json.load(f)
            else:
                print(f"Warning: Vulnerable API rules not found at {rules_path}")
        except Exception as e:
            print(f"Error loading vulnerable API rules: {e}")

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> List[Issue]:
        issues = []
        if not self.rules:
            return issues

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if should_scan_dir(d)]

            for file in files:
                if not should_scan_file(file):
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path).replace("\\", "/")

                if not is_text_file(full_path):
                    continue

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            for rule in self.rules:
                                if re.search(rule["pattern"], line):
                                    issues.append(Issue(
                                        scan_id=scan_id,
                                        user_id=user_id,
                                        type="Vulnerable API",
                                        severity=rule["severity"],
                                        file=rel_path,
                                        line=line_num,
                                        message=rule["message"],
                                        fix=rule["fix"]
                                    ))
                except Exception as e:
                    print(f"Error scanning API usage in {rel_path}: {e}")

        return issues
