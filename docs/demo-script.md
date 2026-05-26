# SecureRepo Demo Script 🎬

This walkthrough script details how to demonstrate SecureRepo's scanning capabilities using the included `demo-vulnerable-repo`.

---

## 🏗️ 1. Setup & Launch
First, start both the backend server and frontend dev environment.

### Start the Backend
1. Open a terminal and navigate to the backend:
   ```bash
   cd backend
   ```
2. Activate your virtual environment and install packages:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
3. Run the uvicorn server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Verify server is running by visiting `http://localhost:8000/health`.

### Start the Frontend
1. Open a second terminal and navigate to the frontend:
   ```bash
   cd frontend
   ```
2. Install npm dependencies and launch the dev server:
   ```bash
   npm install
   npm run dev
   ```
3. Open a browser and load `http://localhost:5173`.

---

## 🔑 2. Authentication Walkthrough
1. On the landing page, click **Sign Up** in the top right.
2. In the registration form, enter a student name (e.g., `Alex Mercer`), email, and password. 
   *(Note: If Firebase environment variables are not loaded, SecureRepo runs in **Demo Mode**, allowing instant login with mock credentials!)*
3. Submit the registration. You are redirected to your personal **Dashboard**.

---

## 🔍 3. Scanning the Demo Repo
1. On your dashboard, locate the **Scan a New Repository** panel.
2. Under the examples, click the **Local Demo Repo** button. This automatically populates the input with `demo-vulnerable-repo`.
3. Keep the **Enable Gemini AI explanations** checked.
4. Click the **Scan Repo** button.
5. The **Security Console Output** terminal triggers:
   - Watch the logs output in real-time as git processes files and each of the six rule-based scanners executes.
   - The scanner completes in seconds and redirects to the detailed **Report** page.

---

## 📊 4. Reviewing Findings on the Report Page
On the report page, highlight these sections to the viewer:

### A. The Score and Summary Card
- Observe the security score of **27/100** indicating **High Risk** due to severe leaks.
- Look at the breakdown counters: **3 Critical**, **3 High**, **4 Medium**, **1 Low**.

### B. The Security Mentor's Summary
- Read the AI-generated paragraph in the top right. Gemini summarizes the student's codebase, calling out the priority fixes (revoking API keys, editing Docker root users) in encouraging, teacher-like language.

### C. The Vulnerabilities Tab
Expand the findings cards to show:
- **Secret Leaked (AWS API Key)**: Found in `.env` (Line 7). Shows how SecureRepo redacts the secret (`AKIAIO...MPLE`) for privacy and outlines how to rotate the key.
- **Risky File (.env)**: Committed env file. Explains why git history retains this even if deleted in a later commit.
- **Config Weakness (Wildcard CORS)**: Found in `src/app.py`. Explains how it allows arbitrary sites to trigger APIs.
- **Beginner Mistake (Git conflict marker)**: Found in `src/app.py`. Shows the unmerged conflict tags.
- **Beginner Mistake (Hardcoded developer path)**: Found in `src/app.py` showing `C:\\Users\\D4rkman...`.

### D. Runtimes and Dependencies Tabs
- Switch to the **Software Runtimes** tab: Observe that **Python** is flagged as **Outdated** because the Dockerfile pins `python:3.8-slim` (minimum secure is `3.9.0`).
- Switch to the **Package Dependencies** tab: Observe that packages like `express (v4.16.0)` and `requests (v2.18.4)` are flagged as **Vulnerable/Outdated** with their CVE reasons and upgrade commands.

---

## 🗑️ 5. Clean Up & History
1. Click **Back to Dashboard** (or click **History** in the navigation bar).
2. Notice your average score and total scan statistics are updated.
3. The demo scan is stored in your personal list.
4. Click the **Delete** (Trash) icon on the scan card to remove it, demonstrating complete Firestore CRUD capability.
