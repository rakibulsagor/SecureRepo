# SecureRepo

SecureRepo is a student-friendly repository security scanner. It uses a simple Flask backend, Jinja2 HTML templates, plain CSS, plain JavaScript, and Python scanner modules.

## File Structure

```text
securerepo/
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html
├─ static/
│  ├─ css/
│  │  └─ styles.css
│  ├─ js/
│  │  └─ main.js
│  └─ images/
├─ routes/
│  └─ scan_routes.py
├─ services/
│  ├─ github_service.py
│  ├─ report_service.py
│  └─ score_service.py
├─ scanners/
│  ├─ secret_scanner.py
│  ├─ risky_file_scanner.py
│  ├─ vulnerable_api_scanner.py
│  ├─ software_version_scanner.py
│  ├─ config_scanner.py
│  └─ beginner_mistake_scanner.py
├─ data/
│  ├─ secret_patterns.json
│  ├─ risky_files.json
│  ├─ vulnerable_api_rules.json
│  └─ software_versions.json
├─ demo-vulnerable-repo/
├─ docs/
└─ README.md
```

## Run Locally

```bash
python -m venv venv
```

On Windows:

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

## API

- `GET /health`
- `POST /api/scan`

Example scan body:

```json
{
  "repo_url": "demo-vulnerable-repo",
  "use_ai_explanation": true
}
```

The response includes `repository`, `score`, `risk_level`, `summary`, and `findings`.
