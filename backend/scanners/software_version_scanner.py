import os
import json
import re
from typing import List, Tuple
from backend.models.issue_models import Issue
from backend.models.scan_models import DetectedSoftware

class SoftwareVersionScanner:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(dir_path, "data", "software_versions.json")
            if os.path.exists(rules_path):
                with open(rules_path, "r", encoding="utf-8") as f:
                    self.rules = json.load(f)
            else:
                print(f"Warning: Software version rules not found at {rules_path}")
        except Exception as e:
            print(f"Error loading software version rules: {e}")

    def parse_version(self, version_str: str) -> List[int]:
        cleaned = re.sub(r'^[^\d]+', '', version_str).strip()
        cleaned = re.split(r'[-+\s]', cleaned)[0]
        parts = []
        for part in cleaned.split('.'):
            try:
                parts.append(int(part))
            except ValueError:
                parts.append(0)
        # Pad with zeros to ensure at least [major, minor, patch]
        while len(parts) < 3:
            parts.append(0)
        return parts[:3]

    def is_outdated(self, current: str, secure_min: str) -> bool:
        p_current = self.parse_version(current)
        p_secure = self.parse_version(secure_min)
        for val1, val2 in zip(p_current, p_secure):
            if val1 < val2:
                return True
            elif val1 > val2:
                return False
        return False

    def scan(self, repo_path: str, scan_id: str = None, user_id: str = None) -> Tuple[List[Issue], List[DetectedSoftware]]:
        issues = []
        detected_software = []

        # Find rules
        python_rule = next((r for r in self.rules if r["type"] == "Python"), None)
        node_rule = next((r for r in self.rules if r["type"] == "Node"), None)
        docker_rule = next((r for r in self.rules if r["type"] == "Docker"), None)

        # 1. Check Python version files (.python-version, runtime.txt)
        python_version_path = os.path.join(repo_path, ".python-version")
        if os.path.exists(python_version_path):
            try:
                with open(python_version_path, "r", encoding="utf-8") as f:
                    version = f.read().strip()
                if version:
                    clean_version = version.lstrip("python-")
                    status = "Secure"
                    if python_rule and self.is_outdated(clean_version, python_rule["min_secure_version"]):
                        status = "Outdated"
                        issues.append(Issue(
                            scan_id=scan_id,
                            user_id=user_id,
                            type="Outdated Software",
                            severity=python_rule["severity"],
                            file=".python-version",
                            line=None,
                            message=f"Outdated Python runtime version detected: {version}. {python_rule['reason']}",
                            fix=python_rule["fix"]
                        ))
                    detected_software.append(DetectedSoftware(
                        name="Python",
                        version=clean_version,
                        status=status,
                        type="Python",
                        latest_stable=python_rule["min_secure_version"] if python_rule else None
                    ))
            except Exception as e:
                print(f"Error scanning .python-version: {e}")

        runtime_path = os.path.join(repo_path, "runtime.txt")
        if os.path.exists(runtime_path):
            try:
                with open(runtime_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                match = re.search(r'python-([0-9\.]+)', content)
                if match:
                    version = match.group(1)
                    status = "Secure"
                    if python_rule and self.is_outdated(version, python_rule["min_secure_version"]):
                        status = "Outdated"
                        issues.append(Issue(
                            scan_id=scan_id,
                            user_id=user_id,
                            type="Outdated Software",
                            severity=python_rule["severity"],
                            file="runtime.txt",
                            line=None,
                            message=f"Outdated Python runtime version defined in runtime.txt: {content}. {python_rule['reason']}",
                            fix=python_rule["fix"]
                        ))
                    detected_software.append(DetectedSoftware(
                        name="Python (runtime.txt)",
                        version=version,
                        status=status,
                        type="Python",
                        latest_stable=python_rule["min_secure_version"] if python_rule else None
                    ))
            except Exception as e:
                print(f"Error scanning runtime.txt: {e}")

        # 2. Check Node engines version in package.json
        package_json_path = os.path.join(repo_path, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                node_engine = data.get("engines", {}).get("node")
                if node_engine:
                    # Clean engine version strings like ">=14.0.0" to a base number "14.0.0"
                    clean_version = re.sub(r'^[^\d]+', '', node_engine).strip()
                    status = "Secure"
                    if node_rule and self.is_outdated(clean_version, node_rule["min_secure_version"]):
                        status = "Outdated"
                        issues.append(Issue(
                            scan_id=scan_id,
                            user_id=user_id,
                            type="Outdated Software",
                            severity=node_rule["severity"],
                            file="package.json",
                            line=None,
                            message=f"Outdated Node.js engine target in package.json: '{node_engine}'. {node_rule['reason']}",
                            fix=node_rule["fix"]
                        ))
                    detected_software.append(DetectedSoftware(
                        name="Node.js Engine",
                        version=clean_version,
                        status=status,
                        type="Node",
                        latest_stable=node_rule["min_secure_version"] if node_rule else None
                    ))
            except Exception as e:
                print(f"Error scanning package.json node engine: {e}")

        # 3. Check Dockerfile base images
        dockerfile_path = os.path.join(repo_path, "Dockerfile")
        if os.path.exists(dockerfile_path):
            try:
                with open(dockerfile_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if line.startswith("#") or not line:
                        continue
                    
                    # Look for FROM instruction
                    # FROM image:tag or FROM image
                    match = re.match(r'^FROM\s+([a-zA-Z0-9_\-\./]+)(?::([a-zA-Z0-9_\-\.]+))?(?:\s+AS\s+\w+)?', line, re.IGNORECASE)
                    if match:
                        image = match.group(1)
                        tag = match.group(2) or ""
                        
                        # A. Check for forbidden tags (latest, or empty tag)
                        is_tag_unsafe = not tag or tag.lower() == "latest"
                        if is_tag_unsafe and docker_rule:
                            issues.append(Issue(
                                scan_id=scan_id,
                                user_id=user_id,
                                type="Config Weakness",
                                severity=docker_rule["severity"],
                                file="Dockerfile",
                                line=line_num,
                                message=f"Docker base image '{image}' is using '{tag or 'implicit latest'}' tag. {docker_rule['reason']}",
                                fix=docker_rule["fix"]
                            ))
                            detected_software.append(DetectedSoftware(
                                name=f"Docker Image: {image}",
                                version="latest (implicit)",
                                status="Warning",
                                type="Docker",
                                latest_stable="Pin specific tag"
                            ))
                        else:
                            # B. Check image specific EOL runtimes (python/node base images)
                            if "python" in image.lower() and python_rule:
                                clean_version = re.sub(r'^[^\d]+', '', tag).split("-")[0]  # e.g., 3.8-slim -> 3.8
                                status = "Secure"
                                if self.is_outdated(clean_version, python_rule["min_secure_version"]):
                                    status = "Outdated"
                                    issues.append(Issue(
                                        scan_id=scan_id,
                                        user_id=user_id,
                                        type="Outdated Software",
                                        severity=python_rule["severity"],
                                        file="Dockerfile",
                                        line=line_num,
                                        message=f"Outdated Python Docker base image version: python:{tag}. {python_rule['reason']}",
                                        fix=python_rule["fix"]
                                    ))
                                detected_software.append(DetectedSoftware(
                                    name="Docker Base: Python",
                                    version=clean_version,
                                    status=status,
                                    type="Docker",
                                    latest_stable=python_rule["min_secure_version"]
                                ))
                            elif "node" in image.lower() and node_rule:
                                clean_version = re.sub(r'^[^\d]+', '', tag).split("-")[0]  # e.g., 16-alpine -> 16
                                status = "Secure"
                                if self.is_outdated(clean_version, node_rule["min_secure_version"]):
                                    status = "Outdated"
                                    issues.append(Issue(
                                        scan_id=scan_id,
                                        user_id=user_id,
                                        type="Outdated Software",
                                        severity=node_rule["severity"],
                                        file="Dockerfile",
                                        line=line_num,
                                        message=f"Outdated Node Docker base image version: node:{tag}. {node_rule['reason']}",
                                        fix=node_rule["fix"]
                                    ))
                                detected_software.append(DetectedSoftware(
                                    name="Docker Base: Node",
                                    version=clean_version,
                                    status=status,
                                    type="Docker",
                                    latest_stable=node_rule["min_secure_version"]
                                ))
                            else:
                                # Generic safe tag
                                detected_software.append(DetectedSoftware(
                                    name=f"Docker Image: {image}",
                                    version=tag,
                                    status="Secure",
                                    type="Docker",
                                    latest_stable=None
                                ))
            except Exception as e:
                print(f"Error scanning Dockerfile base image: {e}")

        return issues, detected_software
