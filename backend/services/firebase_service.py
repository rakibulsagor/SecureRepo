import os
import json
import datetime
from typing import List, Dict, Any, Optional
from backend.firebase_admin_config import db, is_mock

class FirebaseService:
    def __init__(self):
        self.is_mock = is_mock
        # Setup mock DB file path
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mock_db_path = os.path.join(dir_path, "mock_db.json")
        self._init_mock_db()

    def _init_mock_db(self):
        """Initializes the mock database file if it does not exist."""
        if not os.path.exists(self.mock_db_path):
            with open(self.mock_db_path, "w", encoding="utf-8") as f:
                json.dump({
                    "users": {},
                    "scans": {},
                    "issues": {},
                    "reports": {}
                }, f, indent=2)

    def _read_mock_db(self) -> Dict[str, Any]:
        """Reads mock database contents."""
        try:
            with open(self.mock_db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "scans": {}, "issues": {}, "reports": {}}

    def _write_mock_db(self, data: Dict[str, Any]):
        """Writes data to mock database."""
        try:
            with open(self.mock_db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error writing to mock DB: {e}")

    # --- USER COLLECTION ---
    def save_user(self, user_id: str, email: str, name: str) -> Dict[str, Any]:
        user_data = {
            "userId": user_id,
            "name": name,
            "email": email,
            "createdAt": datetime.datetime.utcnow().isoformat()
        }
        if not self.is_mock and db:
            try:
                db.collection("users").document(user_id).set(user_data)
            except Exception as e:
                print(f"Firestore error saving user: {e}")
        else:
            db_data = self._read_mock_db()
            db_data["users"][user_id] = user_data
            self._write_mock_db(db_data)
        return user_data

    # --- SCANS COLLECTION ---
    def save_scan(self, scan_data: Dict[str, Any]):
        if "createdAt" not in scan_data:
            scan_data["createdAt"] = datetime.datetime.utcnow().isoformat()

        scan_id = scan_data["scanId"]
        if not self.is_mock and db:
            try:
                db.collection("scans").document(scan_id).set(scan_data)
            except Exception as e:
                print(f"Firestore error saving scan: {e}")
        else:
            db_data = self._read_mock_db()
            db_data["scans"][scan_id] = scan_data
            self._write_mock_db(db_data)

    # --- ISSUES COLLECTION ---
    def save_issues(self, issues_list: List[Dict[str, Any]]):
        if not self.is_mock and db:
            try:
                batch = db.batch()
                for issue in issues_list:
                    issue_id = issue["issueId"]
                    doc_ref = db.collection("issues").document(issue_id)
                    batch.set(doc_ref, issue)
                batch.commit()
            except Exception as e:
                print(f"Firestore error saving issues batch: {e}")
        else:
            db_data = self._read_mock_db()
            for issue in issues_list:
                issue_id = issue["issueId"]
                db_data["issues"][issue_id] = issue
            self._write_mock_db(db_data)

    # --- REPORTS COLLECTION ---
    def save_report(self, report_data: Dict[str, Any]):
        if "createdAt" not in report_data:
            report_data["createdAt"] = datetime.datetime.utcnow().isoformat()

        report_id = report_data["reportId"]
        if not self.is_mock and db:
            try:
                db.collection("reports").document(report_id).set(report_data)
            except Exception as e:
                print(f"Firestore error saving report: {e}")
        else:
            db_data = self._read_mock_db()
            db_data["reports"][report_id] = report_data
            self._write_mock_db(db_data)

    # --- GET OPERATIONS ---
    def get_user_scans(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves scan history for a user, sorted newest first."""
        scans = []
        if not self.is_mock and db:
            try:
                docs = db.collection("scans").where("userId", "==", user_id).stream()
                for doc in docs:
                    scans.append(doc.to_dict())
                scans.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
            except Exception as e:
                print(f"Firestore error fetching user scans: {e}")
        else:
            db_data = self._read_mock_db()
            for scan in db_data["scans"].values():
                if scan.get("userId") == user_id:
                    scans.append(scan)
            scans.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        return scans

    def get_scan(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single scan details."""
        if not self.is_mock and db:
            try:
                doc = db.collection("scans").document(scan_id).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                print(f"Firestore error fetching scan: {e}")
        else:
            db_data = self._read_mock_db()
            return db_data["scans"].get(scan_id)
        return None

    def get_scan_issues(self, scan_id: str) -> List[Dict[str, Any]]:
        """Retrieves all issues associated with a scan."""
        issues = []
        if not self.is_mock and db:
            try:
                docs = db.collection("issues").where("scanId", "==", scan_id).stream()
                for doc in docs:
                    issues.append(doc.to_dict())
            except Exception as e:
                print(f"Firestore error fetching scan issues: {e}")
        else:
            db_data = self._read_mock_db()
            for issue in db_data["issues"].values():
                if issue.get("scanId") == scan_id:
                    issues.append(issue)
        return issues

    def get_scan_report(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the report associated with a scan."""
        if not self.is_mock and db:
            try:
                docs = db.collection("reports").where("scanId", "==", scan_id).limit(1).stream()
                for doc in docs:
                    return doc.to_dict()
            except Exception as e:
                print(f"Firestore error fetching scan report: {e}")
        else:
            db_data = self._read_mock_db()
            for report in db_data["reports"].values():
                if report.get("scanId") == scan_id:
                    return report
        return None

    # --- DELETE SCAN ---
    def delete_scan(self, scan_id: str) -> bool:
        """Deletes a scan and all associated issues and reports."""
        if not self.is_mock and db:
            try:
                # Delete scan doc
                db.collection("scans").document(scan_id).delete()
                
                # Delete related issues (requires fetching IDs first)
                issues = self.get_scan_issues(scan_id)
                batch = db.batch()
                for issue in issues:
                    doc_ref = db.collection("issues").document(issue["issueId"])
                    batch.delete(doc_ref)
                
                # Delete related reports
                report = self.get_scan_report(scan_id)
                if report:
                    db.collection("reports").document(report["reportId"]).delete()
                
                batch.commit()
                return True
            except Exception as e:
                print(f"Firestore error deleting scan: {e}")
                return False
        else:
            db_data = self._read_mock_db()
            
            # Delete scan
            if scan_id in db_data["scans"]:
                del db_data["scans"][scan_id]
                
            # Delete issues
            issues_to_del = [issue_id for issue_id, issue in db_data["issues"].items() if issue.get("scanId") == scan_id]
            for issue_id in issues_to_del:
                del db_data["issues"][issue_id]
                
            # Delete reports
            reports_to_del = [rep_id for rep_id, rep in db_data["reports"].items() if rep.get("scanId") == scan_id]
            for rep_id in reports_to_del:
                del db_data["reports"][rep_id]
                
            self._write_mock_db(db_data)
            return True
