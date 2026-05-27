# SecureRepo: Python Backend Architecture

SecureRepo is a student-friendly GitHub security scanner built with FastAPI. The backend logic is separated by responsibility so the code stays clean, maintainable, and beginner-friendly.

The frontend is plain HTML, CSS, and JavaScript in `frontend/`. The backend follows the structure below inside `backend/`.

## Directory Structure

```text
backend/
├── main.py
├── routes/
│   └── scan_routes.py
├── services/
│   ├── github_service.py
│   ├── report_service.py
│   └── score_service.py
├── scanners/
│   ├── secret_scanner.py
│   ├── risky_file_scanner.py
│   ├── vulnerable_api_scanner.py
│   ├── software_version_scanner.py
│   ├── config_scanner.py
│   └── beginner_mistake_scanner.py
├── data/
│   ├── secret_patterns.json
│   ├── risky_files.json
│   ├── vulnerable_api_rules.json
│   └── software_versions.json
└── requirements.txt
```

## Component Responsibilities

### Core

- `main.py`: Initializes FastAPI, includes routers, serves the plain frontend, and provides `/health`.

### Routes

- `scan_routes.py`: Defines `POST /api/scan`. It accepts a GitHub URL or local path and returns a structured JSON report.

### Services

- `github_service.py`: Resolves local repository paths or clones public GitHub repositories.
- `report_service.py`: Runs scanners and aggregates findings into the response format.
- `score_service.py`: Calculates the 0-100 score and risk level.

### Scanners

- `secret_scanner.py`: Detects leaked credentials.
- `risky_file_scanner.py`: Detects sensitive files such as `.env`, `.pem`, SQLite databases, and private keys.
- `vulnerable_api_scanner.py`: Detects unsafe API patterns.
- `software_version_scanner.py`: Detects outdated runtime/dependency configuration.
- `config_scanner.py`: Reviews deployment and config weaknesses.
- `beginner_mistake_scanner.py`: Finds common student coding mistakes.

## API Response Format

```json
{
  "repository": "username/repo-name",
  "score": 82,
  "risk_level": "Medium",
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 3,
    "low": 5
  },
  "findings": [
    {
      "type": "Secret Leaked",
      "severity": "High",
      "file": "src/config.js",
      "line": 12,
      "message": "Potential AWS Secret Key found.",
      "fix": "Use environment variables or a secret manager.",
      "beginner_explanation": "A secret is like a digital key. If it is committed to code, anyone who can see the repo may be able to use your account or service."
    }
  ]
}
```

## Run Locally

```bash
cd backend
python -m venv venv
```

On Windows:

```bash
.\venv\Scripts\activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
```

Use `demo-vulnerable-repo` in the scanner input for a local demo scan.
