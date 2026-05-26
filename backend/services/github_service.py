import os
import shutil
import subprocess
import tempfile
import stat
from typing import Tuple, Optional
from backend.utils.repo_url_parser import parse_repo_url

class GitHubService:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.base_temp_dir = os.path.join(tempfile.gettempdir(), "securerepo_temp_repos")
        os.makedirs(self.base_temp_dir, exist_ok=True)

    def _remove_readonly(self, func, path, excinfo):
        """Helper to force-delete read-only files (common in git checkouts on Windows)."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def download_repo(self, repo_url: str, scan_id: str) -> Tuple[Optional[str], str, str, str]:
        """
        Downloads a repository.
        If the url is a local directory path, scans it directly.
        Otherwise, clones the repository into a unique temporary directory.
        Returns: (local_path, owner, name, clean_url)
        """
        local_path = self._resolve_local_path(repo_url)
        if local_path:
            name = os.path.basename(os.path.normpath(local_path)) or "local-repo"
            return local_path, "local", name, local_path

        owner, name, clean_path = parse_repo_url(repo_url)
        if not owner or not name:
            raise ValueError(f"Invalid repository URL or path: {repo_url}")

        # Check if it is a local path
        if owner == "local":
            # If path is relative, resolve it relative to the project root
            resolved_path = clean_path
            if not os.path.isabs(resolved_path):
                resolved_path = os.path.abspath(os.path.join(self.project_root, clean_path))
                
            if os.path.exists(resolved_path) and os.path.isdir(resolved_path):
                return resolved_path, "local", name, resolved_path
            else:
                raise ValueError(f"Local repository path does not exist or is not a directory: {resolved_path}")

        # Create temporary directory for this scan
        target_path = os.path.join(self.base_temp_dir, f"scan_{scan_id}")
        
        try:
            print(f"Cloning public repository: {clean_path} into {target_path}")
            # Run shallow git clone
            result = subprocess.run(
                ["git", "clone", "--depth", "1", clean_path, target_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return target_path, owner, name, clean_path
        except subprocess.CalledProcessError as e:
            # If git clone failed, let's clean up and raise
            self.cleanup(target_path)
            raise RuntimeError(f"Failed to clone repository: {e.stderr or e.stdout}")
        except Exception as e:
            self.cleanup(target_path)
            raise RuntimeError(f"Error cloning repository: {str(e)}")

    def _resolve_local_path(self, repo_url: str) -> Optional[str]:
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

    def cleanup(self, path: str):
        """Cleans up the temporary directory."""
        if not path:
            return
            
        # Ensure we only delete folders inside our temp directory
        if os.path.commonpath([os.path.abspath(path), self.base_temp_dir]) != self.base_temp_dir:
            return

        if os.path.exists(path):
            try:
                shutil.rmtree(path, onerror=self._remove_readonly)
                print(f"Cleaned up temp directory: {path}")
            except Exception as e:
                print(f"Warning: Failed to clean up temp directory {path}: {e}")
                # Try a command line fallback on Windows
                if os.name == 'nt':
                    try:
                        subprocess.run(f'rmdir /s /q "{path}"', shell=True)
                    except:
                        pass
