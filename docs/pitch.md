# SecureRepo Pitch 🛡️

**SecureRepo helps student developers scan their GitHub projects before teachers, recruiters, or attackers see them. It detects leaked secrets, risky files, outdated dependencies, old software versions, and beginner security mistakes using rule-based scanners, then uses Gemini only to explain the results in simple language.**

---

## 💡 The Problem
When learning computer science, students are taught how to code, but rarely how to keep their code secure. They often commit `.env` files with database passwords, upload cloud service credentials, or use outdated libraries. When they push these repositories to public GitHub pages to show recruiters, they expose themselves to security risks, server charges, and poor grading.
Existing tools like Snyk, SonarQube, or GitHub Advanced Security are made for large enterprise dev teams. They show complex CVE codes, raw scanner logs, and dry, jargon-filled warnings that overwhelm and confuse student developers.

## 🚀 The Solution: SecureRepo
SecureRepo is a cybersecurity sandbox built specifically for students and educators. 
1. **Rule-Based Scanning**: Fast, predictable, and deterministic scanning. We never pass source code directly to an AI for detection, keeping scanning results 100% explainable and compliant with security sandbox practices.
2. **AI-Enabled Explanations**: We use the Gemini API only to explain findings. The scanner handles detection, and Gemini acts as a friendly computer science teacher, breaking down the vulnerability in encouraging, simple language.
3. **Beginner-Specific Rules**: Beyond standard secrets, we scan for typical learning mistakes—committed SQLite databases, hardcoded home directories (`C:\Users\username`), active debugging server options, and unresolved Git conflict tags.
4. **Modern Cybersecurity UI**: An interactive, responsive, dark cyberpunk dashboard displaying historical scores and learning insights.

---

## 🛠️ Stack & Architecture
- **Frontend**: React (Vite) styled with a sleek cyberpunk dark-theme using Tailwind CSS.
- **Backend**: FastAPI (Python) delivering robust REST routes.
- **Scanning Engine**: Custom rule-based modules utilizing python file mapping, regex patterns, and local repository cloning.
- **Generative AI**: Google Gemini API via the google-generativeai SDK (only for summarizing findings and translating them to educational content).
- **Database / Auth**: Firebase Auth + Cloud Firestore.

---

## 🌟 Key Features
- **Anonymous Scanning**: Try the tool instantly by supplying a public repository URL or local directory.
- **Educational Cards**: Accordion-based vulnerability cards showing details, exact code fixes, and CS-friendly guides.
- **Security Score (0-100)**: Transparent score calculation subtracting severity weights.
- **Runtime/Dependency Inventories**: Clean reports indicating EOL runtimes (like EOL Python or Node) and vulnerable packages.
- **Persistent Dashboard**: Account history, average score trackers, and scan history.
- **Mock Fallback Modes**: Fully functional mock environments for Auth, Firestore database, and Gemini so the project runs offline and out-of-the-box.
