from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.models.scan_models import ScanRequest, ScanResponse
from backend.services.report_service import ReportService

router = APIRouter()
report_service = ReportService()

@router.post("/scan", response_model=ScanResponse)
def run_repository_scan(request: ScanRequest):
    """
    Triggers a security scan on a public GitHub repository.
    Can also scan a local path in debug mode.
    """
    try:
        response = report_service.generate_report(
            repo_url=request.repo_url,
            user_id=request.user_id,
            use_ai=request.use_ai_explanation
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal scanning error: {str(e)}")
