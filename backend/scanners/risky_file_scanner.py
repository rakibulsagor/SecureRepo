import os
import json
import re
from typing import List
from backend.models.issue_models import Issue
from backend.utils.file_filters import should_scan_dir

class RiskyFileScanner:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(dir_path, "data", "risky_files.json")
            if os.path.exists(rules_path):
                with open(rules_path, "r", encoding="utf-8") as f:
                    self.rules = json.load(f)
            else:
                print(f"Warning: Risky files rules not found at {rules_path}")
        except Exception as e:
            print(f"Error loading risky files rules: {e}")

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> List[Issue]:
        issues = []
        if not self.rules:
            return issues

        for root, dirs, files in os.walk(repo_path):
            # Prune directories in place
            dirs[:] = [d for d in dirs if should_scan_dir(d)]

            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path).replace("\\", "/")

                for rule in self.rules:
                    pattern = rule["pattern"]
                    # We can match on the basename, or on the relative path
                    # Let's match on the basename for patterns like ^\.env$ or on the relative path for paths
                    # Let's check both or support standard regex matching on file name
                    if re.match(pattern, file) or re.match(pattern, rel_path):
                        issue = Issue(
                            scan_id=scan_id,
                            user_id=user_id,
                            type="Risky File",
                            severity=rule["severity"],
                            file=rel_path,
                            line=None,
                            message=rule["message"],
                            fix=rule["fix"]
                        )
                        issues.append(issue)
                        # Avoid reporting multiple issues for the same file under this category
                        break

        return issues
