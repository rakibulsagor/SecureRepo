import os
import re
import shutil
import stat
import subprocess
import tempfile
import uuid
from urllib.parse import urlparse


class GitHubService:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.temp_root = os.path.join(tempfile.gettempdir(), "securerepo_temp_repos")
        os.makedirs(self.temp_root, exist_ok=True)

    def resolve_repository(self, repo_url):
        local_path = self._resolve_local_path(repo_url)
        if local_path:
            name = os.path.basename(os.path.normpath(local_path)) or "local-repo"
            return {
                "path": local_path,
                "repository": f"local/{name}",
                "cleanup": False,
            }

        clone_url, repository = self._parse_github_url(repo_url)
        target_path = os.path.join(self.temp_root, f"scan_{uuid.uuid4().hex}")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", clone_url, target_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            self.cleanup(target_path)
            raise RuntimeError(exc.stderr or exc.stdout or "Failed to clone repository.")

        return {
            "path": target_path,
            "repository": repository,
            "cleanup": True,
        }

    def cleanup(self, repo_path):
        if not repo_path:
            return
        temp_root = os.path.abspath(self.temp_root)
        target = os.path.abspath(repo_path)
        if os.path.commonpath([target, temp_root]) != temp_root:
            return
        if os.path.isdir(target):
            shutil.rmtree(target, onerror=self._remove_readonly)

    def _resolve_local_path(self, repo_url):
        clean_path = repo_url.strip().replace("file://", "")
        candidates = [clean_path]
        if not os.path.isabs(clean_path):
            candidates.append(os.path.join(self.project_root, clean_path))
            candidates.append(os.path.abspath(clean_path))

        for candidate in candidates:
            resolved = os.path.abspath(candidate)
            if os.path.isdir(resolved):
                return resolved
        return None

    def _parse_github_url(self, repo_url):
        value = repo_url.strip()
        if value.endswith(".git"):
            value = value[:-4]

        ssh_match = re.match(r"git@github\.com:([^/]+)/([^/]+)$", value)
        if ssh_match:
            owner, repo = ssh_match.groups()
            return f"https://github.com/{owner}/{repo}.git", f"{owner}/{repo}"

        parsed = urlparse(value)
        if parsed.netloc.lower() != "github.com":
            raise ValueError("Enter a local folder path or a GitHub repository URL.")

        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2:
            raise ValueError("GitHub URL must include owner and repository name.")

        owner, repo = parts[0], parts[1]
        return f"https://github.com/{owner}/{repo}.git", f"{owner}/{repo}"

    def _remove_readonly(self, func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
