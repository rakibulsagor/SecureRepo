from fastapi import APIRouter, HTTPException
from backend.models.scan_models import ScanResponse, ExplainRequest
from backend.services.report_service import ReportService
from backend.services.firebase_service import FirebaseService
from backend.services.gemini_service import GeminiService
from backend.models.issue_models import Issue

router = APIRouter()
report_service = ReportService()
firebase_service = FirebaseService()
gemini_service = GeminiService()

@router.get("/scan/{scan_id}", response_model=ScanResponse)
def get_scan_report(scan_id: str):
    """Retrieves the full report, issues, and AI overview for a completed scan."""
    report = report_service.get_existing_report(scan_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Scan report with ID {scan_id} not found.")
    return report

@router.post("/explain")
def explain_vulnerability(request: ExplainRequest):
    """Regenerates or fetches a student-friendly explanation for a specific flagged issue."""
    # Find issue in database
    db_data = firebase_service.get_scan_issues(request.issue_id)  # Wait, get_scan_issues gets all issues for a scan.
    # Let's write a get_issue in firebase_service?
    # Wait, we can fetch all issues for the scan_id or find it from the DB.
    # Let's search issues in the DB!
    # In firebase_service, let's look at the DB. We can find the issue by filtering all issues or we can write a helper.
    # Let's fetch all issues in mock DB or Firestore.
    # To keep firebase_service clean, let's implement get_issue or just search.
    # Let's search by ID. Let's see:
    
    issue_data = None
    if not firebase_service.is_mock and firebase_service.db:
        doc = firebase_service.db.collection("issues").document(request.issue_id).get()
        if doc.exists:
            issue_data = doc.to_dict()
    else:
        db_db = firebase_service._read_mock_db()
        issue_data = db_db["issues"].get(request.issue_id)

    if not issue_data:
        raise HTTPException(status_code=404, detail="Issue not found.")

    issue = Issue(
        issue_id=issue_data["issueId"],
        scan_id=issue_data["scanId"],
        user_id=issue_data["userId"],
        type=issue_data["type"],
        severity=issue_data["severity"],
        file=issue_data["file"],
        line=issue_data["line"],
        message=issue_data["message"],
        fix=issue_data["fix"],
        studentExplanation=issue_data.get("studentExplanation")
    )

    explanation = gemini_service.explain_issue(issue)
    
    # Save the updated explanation to database
    issue_data["studentExplanation"] = explanation
    if not firebase_service.is_mock and firebase_service.db:
        firebase_service.db.collection("issues").document(request.issue_id).update({
            "studentExplanation": explanation
        })
    else:
        db_db = firebase_service._read_mock_db()
        db_db["issues"][request.issue_id] = issue_data
        firebase_service._write_mock_db(db_db)

    return {
        "issue_id": request.issue_id,
        "explanation": explanation
    }
