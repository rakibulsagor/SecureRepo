from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.report_service import ReportService

router = APIRouter()
report_service = ReportService()


class ScanRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub URL or local repository path")
    use_ai_explanation: Optional[bool] = Field(True, description="Whether to add beginner explanations")


@router.post("/scan")
def scan_repository(request: ScanRequest):
    try:
        return report_service.generate_report(
            repo_url=request.repo_url,
            use_ai_explanation=bool(request.use_ai_explanation),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal scanning error: {exc}")
