import re
from typing import Dict, Optional, Tuple

def parse_repo_url(url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parses a repository URL or local directory path.
    Returns: (owner, name, clean_url_or_path)
    """
    url = url.strip()
    if not url:
        return None, None, None

    # Handle local directories
    if url.startswith("file://") or url.startswith("/") or (len(url) > 1 and url[1] == ":" and (url[0].isalpha() or url[0] in "/\\")):
        # Clean local path
        clean_path = url.replace("file://", "")
        # Find folder name
        parts = [p for p in re.split(r'[\\/]', clean_path) if p]
        name = parts[-1] if parts else "local-repo"
        return "local", name, clean_path

    # Standard GitHub URLs: https://github.com/owner/repo
    # Also handles ssh: git@github.com:owner/repo.git
    github_pattern = r'(https?://github\.com/|git@github\.com:)([^/]+)/([^/\.\?#\s]+)(.*)'
    match = re.match(github_pattern, url)
    if match:
        owner = match.group(2)
        repo_name = match.group(3).replace(".git", "")
        clean_url = f"https://github.com/{owner}/{repo_name}"
        return owner, repo_name, clean_url

    # General HTTP/S URLs (fallback)
    http_pattern = r'https?://([^/]+)/([^/]+)/([^/\.\?#\s]+)'
    match = re.match(http_pattern, url)
    if match:
        owner = match.group(2)
        repo_name = match.group(3).replace(".git", "")
        return owner, repo_name, url

    # Default fallback - treat as raw repo name
    parts = [p for p in url.split("/") if p]
    if len(parts) >= 2:
        return parts[-2], parts[-1], url
        
    return "unknown", url, url
