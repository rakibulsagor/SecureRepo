import os
from typing import List

# List of directories to ignore
IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "ENV",
    "dist",
    "build",
    "out",
    ".next",
    ".cache",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "bower_components",
}

# List of binary or lockfile extensions to ignore for scanning
IGNORED_EXTENSIONS = {
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".pdf",
    # Audio/Video
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    # Archives
    ".zip", ".tar", ".gz", ".rar", ".7z",
    # Binaries/Compiled
    ".exe", ".dll", ".so", ".dylib", ".pyc", ".class", ".jar",
    # Databases/Store
    ".sqlite", ".db", ".sqlite3", ".ds_store",
    # Big Lockfiles (to prevent high processing time and fake positives)
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "pipfile.lock", "cargo.lock"
}

def should_scan_dir(dir_name: str) -> bool:
    """Returns True if the directory should be scanned."""
    return dir_name not in IGNORED_DIRS

def should_scan_file(file_name: str) -> bool:
    """Returns True if the file should be scanned."""
    # Check exact match for lockfiles (lowercased)
    if file_name.lower() in IGNORED_EXTENSIONS:
        return False
        
    _, ext = os.path.splitext(file_name.lower())
    if ext in IGNORED_EXTENSIONS:
        return False
        
    return True

def is_text_file(file_path: str) -> bool:
    """
    Checks if a file is a text file by reading the first block of bytes.
    Avoids reading large binary files completely.
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # Null byte check (typical of binary files)
                return False
        return True
    except IOError:
        return False
