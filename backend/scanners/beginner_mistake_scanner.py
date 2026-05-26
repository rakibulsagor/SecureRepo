import os
import json
import re
from typing import List
from backend.models.issue_models import Issue
from backend.utils.file_filters import should_scan_file, is_text_file

class BeginnerMistakeScanner:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(dir_path, "data", "beginner_rules.json")
            if os.path.exists(rules_path):
                with open(rules_path, "r", encoding="utf-8") as f:
                    all_rules = json.load(f)
                # Select only rules categorized under 'Beginner Mistake'
                self.rules = [r for r in all_rules if r.get("category") == "Beginner Mistake"]
            else:
                print(f"Warning: Rules file not found at {rules_path}")
        except Exception as e:
            print(f"Error loading beginner rules: {e}")

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> List[Issue]:
        issues = []

        # 1. Regex rule-based beginner mistake scanning
        for root, dirs, files in os.walk(repo_path):
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
                            pattern = rule["pattern"]
                            if re.search(pattern, line):
                                issues.append(Issue(
                                    scan_id=scan_id,
                                    user_id=user_id,
                                    type="Beginner Mistake",
                                    severity=rule["severity"],
                                    file=rel_path,
                                    line=line_num,
                                    message=rule["message"],
                                    fix=rule["fix"]
                                ))
                                
                        # 2. Custom check: Hardcoded local absolute paths (e.g. C:\Users\ or /home/username/)
                        # We ignore common systems paths like /usr/bin or /tmp, looking specifically for user directories
                        path_match = re.search(r'(?:[cC]:\\Users\\[a-zA-Z0-9_\-]+|/home/[a-zA-Z0-9_\-]+)/[a-zA-Z0-9_\-\./]+', line)
                        if path_match:
                            issues.append(Issue(
                                scan_id=scan_id,
                                user_id=user_id,
                                type="Beginner Mistake",
                                severity="Low",
                                file=rel_path,
                                line=line_num,
                                message=f"Hardcoded absolute local path detected: '{path_match.group(0)}'. This will fail on other systems and leaks system usernames.",
                                fix="Use relative paths relative to the project root, or fetch paths from environment variables (e.g., using `os.path.dirname(__file__)` or `pathlib.Path`)."
                            ))
                except Exception as e:
                    print(f"Error scanning beginner mistake file {rel_path}: {e}")

        return issues
