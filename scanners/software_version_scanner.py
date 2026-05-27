import json
import os
import re


class SoftwareVersionScanner:
    def __init__(self):
        self.rules = self._load_rules()

    def scan(self, repo_path):
        findings = []
        python_rule = self._rule_for("Python")
        node_rule = self._rule_for("Node")
        docker_rule = self._rule_for("Docker")

        findings.extend(self._scan_python_version(repo_path, python_rule))
        findings.extend(self._scan_package_json(repo_path, node_rule))
        findings.extend(self._scan_dockerfile(repo_path, python_rule, node_rule, docker_rule))
        return findings

    def _scan_python_version(self, repo_path, rule):
        findings = []
        for filename in [".python-version", "runtime.txt"]:
            path = os.path.join(repo_path, filename)
            if not os.path.exists(path) or not rule:
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read().strip()
            match = re.search(r"([0-9]+(?:\.[0-9]+){0,2})", content)
            if match and self._is_outdated(match.group(1), rule["min_secure_version"]):
                findings.append(self._finding(rule, filename, None, f"Outdated Python runtime detected: {content}. {rule['reason']}"))
        return findings

    def _scan_package_json(self, repo_path, rule):
        path = os.path.join(repo_path, "package.json")
        if not os.path.exists(path) or not rule:
            return []
        try:
            with open(path, "r", encoding="utf-8") as file:
                package_data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        engine = package_data.get("engines", {}).get("node")
        if not engine:
            return []
        match = re.search(r"([0-9]+(?:\.[0-9]+){0,2})", engine)
        if match and self._is_outdated(match.group(1), rule["min_secure_version"]):
            return [self._finding(rule, "package.json", None, f"Outdated Node.js engine target detected: {engine}. {rule['reason']}")]
        return []

    def _scan_dockerfile(self, repo_path, python_rule, node_rule, docker_rule):
        path = os.path.join(repo_path, "Dockerfile")
        if not os.path.exists(path):
            return []

        findings = []
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            for line_number, line in enumerate(file, 1):
                match = re.match(r"^\s*FROM\s+([a-zA-Z0-9_\-./]+)(?::([a-zA-Z0-9_.\-]+))?", line)
                if not match:
                    continue
                image, tag = match.group(1), match.group(2) or "latest"
                if tag == "latest" and docker_rule:
                    findings.append(self._finding(docker_rule, "Dockerfile", line_number, f"Docker image {image} uses the latest tag. {docker_rule['reason']}"))
                if "python" in image.lower() and python_rule and self._is_outdated(tag, python_rule["min_secure_version"]):
                    findings.append(self._finding(python_rule, "Dockerfile", line_number, f"Outdated Python Docker image detected: python:{tag}. {python_rule['reason']}"))
                if "node" in image.lower() and node_rule and self._is_outdated(tag, node_rule["min_secure_version"]):
                    findings.append(self._finding(node_rule, "Dockerfile", line_number, f"Outdated Node Docker image detected: node:{tag}. {node_rule['reason']}"))
        return findings

    def _finding(self, rule, file_path, line, message):
        return {
            "type": "Outdated Software",
            "severity": rule["severity"],
            "file": file_path,
            "line": line,
            "message": message,
            "fix": rule["fix"],
        }

    def _rule_for(self, rule_type):
        return next((rule for rule in self.rules if rule["type"] == rule_type), None)

    def _load_rules(self):
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "software_versions.json")
        with open(rules_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _is_outdated(self, current, minimum):
        current_parts = self._version_parts(current)
        minimum_parts = self._version_parts(minimum)
        return current_parts < minimum_parts

    def _version_parts(self, version):
        match = re.search(r"([0-9]+(?:\.[0-9]+){0,2})", str(version))
        if not match:
            return [0, 0, 0]
        parts = [int(part) for part in match.group(1).split(".")]
        while len(parts) < 3:
            parts.append(0)
        return parts[:3]
