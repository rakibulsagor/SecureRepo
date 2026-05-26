import os
import json
import re
from typing import List
from backend.models.issue_models import Issue
from backend.utils.file_filters import should_scan_file, is_text_file

class ConfigScanner:
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
                # Select only rules categorized under 'Config'
                self.rules = [r for r in all_rules if r.get("category") == "Config"]
            else:
                print(f"Warning: Rules file not found at {rules_path}")
        except Exception as e:
            print(f"Error loading config rules: {e}")

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> List[Issue]:
        issues = []

        # 1. Regex rule-based config scanning
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
                                    type="Config Weakness",
                                    severity=rule["severity"],
                                    file=rel_path,
                                    line=line_num,
                                    message=rule["message"],
                                    fix=rule["fix"]
                                ))
                except Exception as e:
                    print(f"Error scanning config file {rel_path}: {e}")

        # 2. Custom Dockerfile user check (no USER instruction = runs as root)
        dockerfile_path = os.path.join(repo_path, "Dockerfile")
        if os.path.exists(dockerfile_path):
            try:
                with open(dockerfile_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if "USER " instruction is present
                if not re.search(r'^\s*USER\s+\w+', content, re.MULTILINE | re.IGNORECASE):
                    issues.append(Issue(
                        scan_id=scan_id,
                        user_id=user_id,
                        type="Config Weakness",
                        severity="High",
                        file="Dockerfile",
                        line=None,
                        message="Dockerfile does not specify a non-root USER instruction. The container will default to running as root, increasing vulnerability to host-takeover attacks.",
                        fix="Create a non-privileged user and switch to it using the `USER` directive in your Dockerfile (e.g. `RUN useradd -m myuser && USER myuser`)."
                    ))
            except Exception as e:
                print(f"Error checking Dockerfile USER: {e}")

        return issues
