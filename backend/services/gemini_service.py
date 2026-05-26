import os
import json
from typing import List, Dict, Any, Optional
from backend.config import settings
from backend.models.issue_models import Issue

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GeminiService:
    def __init__(self):
        self.is_configured = settings.is_gemini_configured and genai is not None
        if self.is_configured:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                # Using gemini-1.5-flash as the fast, standard model
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                print("Gemini API successfully configured.")
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
                self.is_configured = False
        else:
            print("Gemini API Key missing or placeholder. Running in Mock Mode.")

    def explain_issue(self, issue: Issue) -> str:
        """
        Generates a student-friendly explanation of why the issue is a risk and how to fix it.
        Uses Gemini if configured, otherwise falls back to a deterministic educational description.
        """
        if self.is_configured:
            try:
                prompt = (
                    "You are an encouraging, friendly, and clear computer science teacher.\n"
                    f"A student's repository has a security issue of type '{issue.type}' in file '{issue.file}'.\n"
                    f"The raw message is: '{issue.message}'.\n"
                    f"The recommended raw fix is: '{issue.fix}'.\n\n"
                    "In 2 to 3 simple, encouraging sentences, explain to the student:\n"
                    "1. Why this is a security risk in real-world terms.\n"
                    "2. What an attacker could do if they find it.\n"
                    "3. How to fix it in a beginner-friendly way.\n\n"
                    "Keep the explanation under 120 words. Do not use complex security jargon."
                )
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini API call failed for issue explanation: {e}. Falling back to template.")

        # Fallback Mock Explanations
        type_lower = issue.type.lower()
        if "secret" in type_lower:
            return (
                f"Oh no! It looks like a sensitive credential ('{issue.type}') was accidentally left in {issue.file}. "
                "Think of this like leaving your house key sticking in the front door. Anyone who views your GitHub page "
                "can copy this key and gain access to your accounts or charge fees to your subscription! "
                "To fix this, you should immediately invalidate/revoke that key, add this file to your `.gitignore`, "
                "and load the credential at runtime using an environment variable."
            )
        elif "risky file" in type_lower:
            return (
                f"We detected a file ({issue.file}) that usually contains configuration secrets or credentials. "
                "It's a common mistake to commit `.env` or credential files to Git. However, once pushed to a public repository, "
                "they are cached forever in Git history, even if you delete them in a later commit! "
                "Make sure you run `git rm --cached {issue.file}`, add it to your `.gitignore`, and rotate any keys that were inside."
            )
        elif "dependency" in type_lower:
            return (
                f"The package mentioned in {issue.file} is an older version that has known security vulnerabilities. "
                "Just like updating your phone's OS to patch bugs, library packages need updates to patch security holes. "
                "If you keep this version, attackers could exploit documented bugs to crash your application or access data. "
                "Simply run the upgrade command (like `npm install` or `pip install --upgrade`) and update your version references."
            )
        elif "config" in type_lower:
            return (
                f"This configuration setting in {issue.file} makes your app less secure. "
                "Setting permissive configurations (like CORS '*' or running Docker containers as root) is common in early development, "
                "but in production, it leaves the doors wide open for unauthorized sites or container escape vulnerabilities. "
                "Try restricting access to only trusted hosts or configuring a non-root user."
            )
        elif "mistake" in type_lower:
            return (
                f"This is a common beginner mistake in {issue.file} (like leaving debug mode on or hardcoding database passwords). "
                "While helpful during local debugging, these settings leak system logs, passwords, and source code details to the public. "
                "You should disable debug modes in production and store passwords in environment variables."
            )
        
        return (
            f"This setting in {issue.file} is flagged as a security issue. It is important to avoid hardcoded values, "
            "permissive settings, or obsolete dependencies. Restricting permissions and moving settings to environment variables "
            "keeps your code clean, portable, and secure!"
        )

    def generate_scan_summary(self, score: int, risk_level: str, issues: List[Issue]) -> str:
        """
        Generates an overall summary of the scan results, calling out general posture and educational tips.
        """
        if self.is_configured and issues:
            try:
                issues_summary = "\n".join([f"- {i.type} in {i.file}: {i.message}" for i in issues[:5]])
                prompt = (
                    "You are a friendly, encouraging DevOps and Security mentor for students.\n"
                    f"A student scanned their codebase. Score: {score}/100. Risk level: '{risk_level}'.\n"
                    f"The top issues found are:\n{issues_summary}\n\n"
                    "Write a short, highly encouraging summary of their scan (2-3 sentences, max 120 words).\n"
                    "Include:\n"
                    "- An evaluation of their current security posture.\n"
                    "- 1-2 clear, bite-sized next steps they should focus on first.\n"
                    "Make them feel excited to learn and secure their code, not discouraged!"
                )
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini API call failed for scan summary: {e}. Falling back to template.")

        # Fallback Mock Summary
        if score >= 90:
            return (
                f"Outstanding job! Your repository score is {score}/100 ({risk_level}). Your security posture is excellent. "
                "You are following best practices, keeping credentials out of files, and maintaining clean configurations. "
                "Continue using `.gitignore` and review your third-party packages occasionally to stay secure."
            )
        elif score >= 75:
            return (
                f"Great start! Your security score is {score}/100 ({risk_level}). The repository is in relatively good shape, "
                "but there are a few config tweaks or software runtime updates needed. Focus on fixing the medium-severity issues "
                "first, and check that your runtime software is kept up-to-date."
            )
        elif score >= 50:
            return (
                f"Good effort! Your repository scored {score}/100 ({risk_level}). We detected some security concerns like "
                "old software runtimes or general configuration flags. Don't worry—these are very common when learning! "
                "Take a few minutes to upgrade the runtime versions and remove any default debug settings before deploying."
            )
        else:
            return (
                f"Welcome to SecureRepo! Your scan score is {score}/100 ({risk_level}). This is a fantastic learning opportunity! "
                "It looks like some credentials (like API keys) or highly permissive configurations were left in the code. "
                "Your priority should be revoking any hardcoded secrets and deleting `.env` files from Git. Let's secure it together!"
            )
