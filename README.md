# SecureRepo 🛡️

SecureRepo is a student-friendly GitHub security checker. It scans public GitHub repositories for leaked secrets, unsafe files, weak dependencies, outdated software/framework versions, unsafe configs, and beginner security mistakes. It then uses Gemini to explain the results in a beginner-friendly way.

> **Final Product Statement**: SecureRepo helps student developers scan their GitHub projects before teachers, recruiters, or attackers see them. It detects leaked secrets, risky files, outdated dependencies, old software versions, and beginner security mistakes using rule-based scanners, then uses Gemini only to explain the results in simple language.

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
 ├── Dependency Scanner
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
├── README.md
├── .gitignore
├── .env.example
├── frontend/             # React Frontend
├── backend/              # FastAPI Backend
├── demo-vulnerable-repo/ # Mock vulnerable repo for local scanning
└── docs/                 # Documentation & Pitch materials
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
