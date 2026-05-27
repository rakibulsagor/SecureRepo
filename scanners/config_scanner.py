import os
import re

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TEXT_EXTENSIONS = {".js", ".ts", ".py", ".json", ".txt", ".yml", ".yaml", ".env"}

CONFIG_RULES = [
    {
        "pattern": r"(?i)allow_origins\s*=\s*\[\s*['\"]\*['\"]\s*\]|cors_allowed_origins\s*=\s*['\"]\*['\"]|allow_origin\s*:\s*['\"]\*['\"]",
        "severity": "Medium",
        "message": "Wildcard CORS origin '*' detected. This can let untrusted websites call your API from a browser.",
        "fix": "Replace '*' with a short allowlist of trusted frontend domains.",
    },
    {
        "pattern": r"secure\s*=\s*False|secureCookie\s*:\s*false",
        "severity": "Medium",
        "message": "Cookie secure flag is disabled. Sensitive cookies may travel over unencrypted HTTP.",
        "fix": "Set secure cookies to true in production and serve the app over HTTPS.",
    },
]


class ConfigScanner:
    def scan(self, repo_path):
        findings = []
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
            for filename in files:
                full_path = os.path.join(root, filename)
                if not self._is_text_file(full_path):
                    continue
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                findings.extend(self._scan_file(full_path, relative_path))

        findings.extend(self._scan_docker_user(repo_path))
        return findings

    def _scan_file(self, full_path, relative_path):
        findings = []
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                for line_number, line in enumerate(file, 1):
                    for rule in CONFIG_RULES:
                        if re.search(rule["pattern"], line):
                            findings.append({
                                "type": "Config Weakness",
                                "severity": rule["severity"],
                                "file": relative_path,
                                "line": line_number,
                                "message": rule["message"],
                                "fix": rule["fix"],
                            })
        except OSError:
            pass
        return findings

    def _scan_docker_user(self, repo_path):
        dockerfile = os.path.join(repo_path, "Dockerfile")
        if not os.path.exists(dockerfile):
            return []
        with open(dockerfile, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
        if re.search(r"^\s*USER\s+\w+", content, re.MULTILINE | re.IGNORECASE):
            return []
        return [{
            "type": "Config Weakness",
            "severity": "High",
            "file": "Dockerfile",
            "line": None,
            "message": "Dockerfile does not specify a non-root USER instruction.",
            "fix": "Create a non-privileged user and switch to it with the USER directive.",
        }]

    def _is_text_file(self, path):
        _, extension = os.path.splitext(path)
        return extension.lower() in TEXT_EXTENSIONS or os.path.basename(path) == "Dockerfile"
