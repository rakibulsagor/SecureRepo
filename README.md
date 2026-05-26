# SecureRepo 🛡️

SecureRepo is a student-friendly GitHub security checker. It scans public GitHub repositories for leaked secrets, unsafe files, outdated software/framework versions, unsafe configs, and beginner security mistakes. It then uses Gemini to explain the results in a beginner-friendly way.

> **Final Product Statement**: SecureRepo helps student developers scan their GitHub projects before teachers, recruiters, or attackers see them. It detects leaked secrets, risky files, old software versions, and beginner security mistakes using rule-based scanners, then uses Gemini only to explain the results in simple language.

---

## 🏗️ Architecture

```text
User
 ↓
React + Vite Frontend (Tailwind CSS)
 ↓
FastAPI Backend
 ↓
GitHub Service (Anonymous Shallow Clone)
 ↓
Rule-Based Scanner Engine
 ├── Secret Scanner
 ├── Risky File Scanner
 ├── Software Version Scanner
 ├── Config Scanner
 └── Beginner Mistake Scanner
 ↓
Score Service (Calculates Security Score 0 - 100)
 ↓
Gemini Explanation Service (Explains findings in simple student-friendly language)
 ↓
Firebase Firestore & Auth (Scans, Users, Reports, Issues)
```

---

## 🛠️ Stack

- **Frontend**: React + Vite + Tailwind CSS + Firebase Client SDK
- **Backend**: Python FastAPI + Uvicorn + Firebase Admin SDK + Google Generative AI (Gemini) SDK
- **Scanners**: Python Rule-Based Regex and AST Modules (not AI-based to ensure determinism and compliance with rules)
- **AI Helper**: Gemini API (explanations, fixes, summaries only)
- **Database**: Firebase Auth + Cloud Firestore

---

## 📁 Repository Structure

```text
securerepo/
│
├── README.md
├── .gitignore
├── .env.example
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   │
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       │
│       ├── api/
│       │   └── scanApi.js
│       │
│       ├── firebase/
│       │   └── firebaseConfig.js
│       │
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Login.jsx
│       │   ├── Dashboard.jsx
│       │   ├── Report.jsx
│       │   ├── History.jsx
│       │   └── Learn.jsx
│       │
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── RepoInput.jsx
│       │   ├── LoadingScan.jsx
│       │   ├── ScoreCard.jsx
│       │   ├── IssueCard.jsx
│       │   ├── SeverityBadge.jsx
│       │   ├── SoftwareVersionTable.jsx
│       │   ├── AiExplanationBox.jsx
│       │   ├── ScanHistoryCard.jsx
│       │   └── EmptyState.jsx
│       │
│       ├── hooks/
│       │   └── useAuth.js
│       │
│       ├── utils/
│       │   ├── formatDate.js
│       │   └── severityHelper.js
│       │
│       └── styles/
│           └── index.css
│
├── backend/
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── firebase_admin_config.py
│   │
│   ├── routes/
│   │   ├── health_routes.py
│   │   ├── scan_routes.py
│   │   └── history_routes.py
│   │
│   ├── services/
│   │   ├── github_service.py
│   │   ├── gemini_service.py
│   │   ├── firebase_service.py
│   │   ├── score_service.py
│   │   └── report_service.py
│   │
│   ├── scanners/
│   │   ├── scanner_engine.py
│   │   ├── secret_scanner.py
│   │   ├── risky_file_scanner.py
│   │   ├── software_version_scanner.py
│   │   ├── config_scanner.py
│   │   └── beginner_mistake_scanner.py
│   │
│   ├── data/
│   │   ├── secret_patterns.json
│   │   ├── risky_files.json
│   │   ├── software_versions.json
│   │   └── beginner_rules.json
│   │
│   ├── models/
│   │   ├── scan_models.py
│   │   ├── issue_models.py
│   │   └── repo_models.py
│   │
│   ├── utils/
│   │   ├── repo_url_parser.py
│   │   ├── file_filters.py
│   │   ├── line_finder.py
│   │   └── severity.py
│   │
│   └── tests/
│       ├── test_secret_scanner.py
│       ├── test_risky_file_scanner.py
│       ├── test_software_version_scanner.py
│       ├── test_config_scanner.py
│       └── test_score_service.py
│
├── demo-vulnerable-repo/
│   ├── README.md
│   ├── .env
│   ├── Dockerfile
│   ├── runtime.txt
│   ├── .python-version
│   ├── .nvmrc
│   └── src/
│       ├── firebase.js
│       ├── app.py
│       └── settings.py
│
└── docs/
    ├── pitch.md
    ├── demo-script.md
    ├── features.md
    └── future-scope.md
```

---

## ⚡ Quick Start (Local Development)

Both frontend and backend are designed to run in **Mock Mode** by default if Firebase or Gemini API credentials are not provided. This ensures instant testing capability!

### 1. Run the Backend
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to test SecureRepo.
You can use `https://github.com/your-username/your-repo` or target the local `demo-vulnerable-repo` path to see the scanners in action!
