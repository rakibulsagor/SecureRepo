import os
import json
import re
from typing import List
from backend.models.issue_models import Issue
from backend.utils.file_filters import should_scan_file, is_text_file

class SecretScanner:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            # Resolve path relative to this file
            dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(dir_path, "data", "secret_patterns.json")
            if os.path.exists(rules_path):
                with open(rules_path, "r", encoding="utf-8") as f:
                    self.rules = json.load(f)
            else:
                print(f"Warning: Secret rules file not found at {rules_path}")
        except Exception as e:
            print(f"Error loading secret rules: {e}")

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> List[Issue]:
        issues = []
        if not self.rules:
            return issues

        # Walk through files in repo_path
        for root, dirs, files in os.walk(repo_path):
            # Prune directories in place (so os.walk skips ignored directories)
            from backend.utils.file_filters import should_scan_dir
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
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):
                        for rule in self.rules:
                            pattern = rule["regex"]
                            match = re.search(pattern, line)
                            if match:
                                matched_text = match.group(0)
                                # Redact the secret in the output for safety
                                redacted = matched_text[:6] + "..." + matched_text[-4:] if len(matched_text) > 10 else "..."
                                message = f"{rule['message']} (Found: '{redacted}')"
                                
                                issue = Issue(
                                    scan_id=scan_id,
                                    user_id=user_id,
                                    type="Secret Leaked",
                                    severity=rule["severity"],
                                    file=rel_path,
                                    line=line_num,
                                    message=message,
                                    fix=rule["fix"]
                                )
                                issues.append(issue)
                except Exception as e:
                    print(f"Error scanning file {rel_path} for secrets: {e}")

        return issues
