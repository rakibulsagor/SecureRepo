import os
import uuid
import datetime
from typing import List, Dict, Any, Optional, Tuple
from backend.models.scan_models import ScanResponse, RepoDetails, ScanSummary, DetectedSoftware
from backend.models.issue_models import Issue
from backend.services.github_service import GitHubService
from backend.services.gemini_service import GeminiService
from backend.services.firebase_service import FirebaseService
from backend.scanners.scanner_engine import ScannerEngine

class ReportService:
    def __init__(self):
        self.github_service = GitHubService()
        self.gemini_service = GeminiService()
        self.firebase_service = FirebaseService()
        self.scanner_engine = ScannerEngine()

    def generate_report(self, repo_url: str, user_id: Optional[str] = None, use_ai: bool = True) -> ScanResponse:
        scan_id = str(uuid.uuid4())
        local_path = None
        
        try:
            # 1. Download/clone repo
            local_path, owner, repo_name, clean_url = self.github_service.download_repo(repo_url, scan_id)

            # 2. Execute scanning engine
            issues, software_list, score, risk_level, summary = self.scanner_engine.run_scan(
                local_path, owner, repo_name, clean_url, user_id
            )

            # 3. Add student explanations
            for issue in issues:
                if use_ai:
                    issue.studentExplanation = self.gemini_service.explain_issue(issue)
                else:
                    # Generic explanation if AI is disabled
                    issue.studentExplanation = issue.fix

            # 4. Generate overall scan summary
            ai_summary = self.gemini_service.generate_scan_summary(score, risk_level, issues)

            # 5. Persist to Firestore / Mock DB
            # A. Save scan metadata
            scan_payload = {
                "scanId": scan_id,
                "userId": user_id or "anonymous",
                "repoUrl": clean_url,
                "repoName": repo_name,
                "owner": owner,
                "score": score,
                "riskLevel": risk_level,
                "createdAt": datetime.datetime.utcnow().isoformat(),
                "issueCounts": {
                    "critical": summary.critical,
                    "high": summary.high,
                    "medium": summary.medium,
                    "low": summary.low
                },
                "detectedSoftware": [
                    {
                        "name": sw.name,
                        "version": sw.version,
                        "status": sw.status,
                        "type": sw.type,
                        "latestStable": sw.latest_stable
                    } for sw in software_list
                ]
            }
            self.firebase_service.save_scan(scan_payload)

            # B. Save issues
            issue_payloads = []
            for issue in issues:
                issue_payloads.append({
                    "issueId": issue.issue_id,
                    "scanId": scan_id,
                    "userId": user_id or "anonymous",
                    "type": issue.type,
                    "severity": issue.severity,
                    "file": issue.file,
                    "line": issue.line,
                    "message": issue.message,
                    "fix": issue.fix,
                    "studentExplanation": issue.studentExplanation
                })
            if issue_payloads:
                self.firebase_service.save_issues(issue_payloads)

            # C. Save report details
            report_id = str(uuid.uuid4())
            report_payload = {
                "reportId": report_id,
                "scanId": scan_id,
                "userId": user_id or "anonymous",
                "summary": f"Scan completed with score {score}/100. Found {len(issues)} issues.",
                "aiExplanation": ai_summary,
                "createdAt": datetime.datetime.utcnow().isoformat()
            }
            self.firebase_service.save_report(report_payload)

            # Assemble response model
            return ScanResponse(
                scan_id=scan_id,
                repo=RepoDetails(owner=owner, name=repo_name, url=clean_url),
                score=score,
                risk_level=risk_level,
                summary=summary,
                issues=issues,
                detected_software=software_list,
                ai_summary=ai_summary
            )

        except Exception as e:
            print(f"Error executing scan: {e}")
            raise e
        finally:
            # Always clean up cloned repository directory to free space
            if local_path and owner != "local":
                self.github_service.cleanup(local_path)
                
    def get_existing_report(self, scan_id: str) -> Optional[ScanResponse]:
        """Retrieves an existing scan and issues from database."""
        scan_data = self.firebase_service.get_scan(scan_id)
        if not scan_data:
            return None
            
        issues_data = self.firebase_service.get_scan_issues(scan_id)
        report_data = self.firebase_service.get_scan_report(scan_id)
        
        # Format issues
        issues = [
            Issue(
                issue_id=i["issueId"],
                scan_id=i["scanId"],
                user_id=i["userId"],
                type=i["type"],
                severity=i["severity"],
                file=i["file"],
                line=i["line"],
                message=i["message"],
                fix=i["fix"],
                studentExplanation=i.get("studentExplanation")
            ) for i in issues_data
        ]
        
        # Format detected software
        software = [
            DetectedSoftware(
                name=sw["name"],
                version=sw["version"],
                status=sw["status"],
                type=sw["type"],
                latest_stable=sw.get("latestStable")
            ) for sw in scan_data.get("detectedSoftware", [])
        ]
        
        # Re-calc counts
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
                
        return ScanResponse(
            scan_id=scan_id,
            repo=RepoDetails(
                owner=scan_data.get("owner", "unknown"),
                name=scan_data.get("repoName", "unknown"),
                url=scan_data.get("repoUrl", "")
            ),
            score=scan_data.get("score", 100),
            risk_level=scan_data.get("riskLevel", "Excellent"),
            summary=summary,
            issues=issues,
            detected_software=software,
            ai_summary=report_data.get("aiExplanation") if report_data else "No summary available."
        )
