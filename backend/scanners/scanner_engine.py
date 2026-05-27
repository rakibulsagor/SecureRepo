import uuid
from typing import List, Dict, Any, Tuple
from backend.models.issue_models import Issue
from backend.models.scan_models import ScanResponse, RepoDetails, ScanSummary, DetectedSoftware
from backend.scanners.secret_scanner import SecretScanner
from backend.scanners.risky_file_scanner import RiskyFileScanner
from backend.scanners.software_version_scanner import SoftwareVersionScanner
from backend.scanners.config_scanner import ConfigScanner
from backend.scanners.vulnerable_api_scanner import VulnerableApiScanner
from backend.scanners.beginner_mistake_scanner import BeginnerMistakeScanner
from backend.services.score_service import calculate_score, get_risk_level

class ScannerEngine:
    def __init__(self):
        self.secret_scanner = SecretScanner()
        self.risky_file_scanner = RiskyFileScanner()
        self.software_version_scanner = SoftwareVersionScanner()
        self.config_scanner = ConfigScanner()
        self.vulnerable_api_scanner = VulnerableApiScanner()
        self.beginner_mistake_scanner = BeginnerMistakeScanner()

    def run_scan(self, repo_path: str, repo_owner: str, repo_name: str, repo_url: str, user_id: str = None) -> Tuple[List[Issue], List[DetectedSoftware], int, str, ScanSummary]:
        scan_id = str(uuid.uuid4())

        # Collect issues
        issues: List[Issue] = []
        detected_software: List[DetectedSoftware] = []

        # 1. Run secret scanner
        issues.extend(self.secret_scanner.scan(repo_path, scan_id, user_id))

        # 2. Run risky file scanner
        issues.extend(self.risky_file_scanner.scan(repo_path, scan_id, user_id))



        # 3. Run vulnerable API scanner
        issues.extend(self.vulnerable_api_scanner.scan(repo_path, scan_id, user_id))

        # 4. Run software version scanner
        soft_issues, soft_software = self.software_version_scanner.scan(repo_path, scan_id, user_id)
        issues.extend(soft_issues)
        detected_software.extend(soft_software)

        # 5. Run config scanner
        issues.extend(self.config_scanner.scan(repo_path, scan_id, user_id))

        # 6. Run beginner mistake scanner
        issues.extend(self.beginner_mistake_scanner.scan(repo_path, scan_id, user_id))

        # Attach auto-generated uuid as issue_id if missing
        for issue in issues:
            if not issue.issue_id:
                issue.issue_id = str(uuid.uuid4())
            issue.scan_id = scan_id

        # Calculate metrics
        score = calculate_score(issues)
        risk_level = get_risk_level(score)

        # Build summary
        summary = ScanSummary(critical=0, high=0, medium=0, low=0)
        for issue in issues:
            sev = issue.severity.lower()
            if sev == "critical":
                summary.critical += 1
            elif sev == "high":
                summary.high += 1
            elif sev == "medium":
                summary.medium += 1
            elif sev == "low":
                summary.low += 1

        # Deduplicate detected software list by name
        seen_software = {}
        for ds in detected_software:
            # Prefer 'Outdated' or 'Warning' statuses over 'Secure' if duplicate exists
            if ds.name not in seen_software:
                seen_software[ds.name] = ds
            else:
                if ds.status in ["Outdated", "Warning"] and seen_software[ds.name].status == "Secure":
                    seen_software[ds.name] = ds
        
        deduped_software = list(seen_software.values())

        return issues, deduped_software, score, risk_level, summary
