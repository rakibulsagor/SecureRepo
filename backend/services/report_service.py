from scanners.beginner_mistake_scanner import BeginnerMistakeScanner
from scanners.config_scanner import ConfigScanner
from scanners.risky_file_scanner import RiskyFileScanner
from scanners.secret_scanner import SecretScanner
from scanners.software_version_scanner import SoftwareVersionScanner
from scanners.vulnerable_api_scanner import VulnerableApiScanner
from services.github_service import GitHubService
from services.score_service import ScoreService


class ReportService:
    def __init__(self):
        self.github_service = GitHubService()
        self.score_service = ScoreService()
        self.scanners = [
            SecretScanner(),
            RiskyFileScanner(),
            VulnerableApiScanner(),
            SoftwareVersionScanner(),
            ConfigScanner(),
            BeginnerMistakeScanner(),
        ]

    def generate_report(self, repo_url, use_ai_explanation=True):
        repo_info = self.github_service.resolve_repository(repo_url)
        findings = []

        try:
            for scanner in self.scanners:
                findings.extend(scanner.scan(repo_info["path"]))
        finally:
            if repo_info["cleanup"]:
                self.github_service.cleanup(repo_info["path"])

        if use_ai_explanation:
            for finding in findings:
                finding["beginner_explanation"] = self._beginner_explanation(finding)

        score = self.score_service.calculate_score(findings)
        return {
            "repository": repo_info["repository"],
            "score": score,
            "risk_level": self.score_service.risk_level(score),
            "summary": self.score_service.summarize(findings),
            "findings": findings,
        }

    def _beginner_explanation(self, finding):
        issue_type = finding.get("type", "Security Issue")
        if issue_type == "Secret Leaked":
            return "A secret is like a digital key. If it is committed to code, anyone who can see the repo may be able to use your account or service."
        if issue_type == "Risky File":
            return "Some files are safe on your computer but unsafe in a public repository because they often contain private settings or credentials."
        if issue_type == "Vulnerable API":
            return "APIs are doors into your app. If they are too open or send secrets in unsafe places, other people can abuse them."
        if issue_type == "Outdated Software":
            return "Old software may no longer receive security fixes. Upgrading reduces known vulnerabilities attackers can reuse."
        if issue_type == "Config Weakness":
            return "Configuration controls how your app behaves in real environments. Unsafe defaults can accidentally expose private data or admin behavior."
        return "This is a common beginner mistake that can make code unreliable or unsafe when someone else runs it."
