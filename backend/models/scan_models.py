from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from backend.models.issue_models import Issue

class RepoDetails(BaseModel):
    owner: str = Field(..., description="GitHub repository owner")
    name: str = Field(..., description="GitHub repository name")
    url: str = Field(..., description="Full GitHub repository URL")

class ScanSummary(BaseModel):
    critical: int = Field(default=0)
    high: int = Field(default=0)
    medium: int = Field(default=0)
    low: int = Field(default=0)

class DetectedSoftware(BaseModel):
    name: str = Field(..., description="Name of the software or framework")
    version: str = Field(..., description="Detected version")
    status: str = Field(..., description="Status: Outdated, Secure, Warning")
    type: str = Field(..., description="Language/runtime context (e.g. Python, Node, Docker)")
    latest_stable: Optional[str] = Field(None, description="Latest stable version suggestion")

class ScanRequest(BaseModel):
    repo_url: str = Field(..., description="Public GitHub repository URL (or local path for testing)")
    user_id: Optional[str] = Field(None, description="Firebase user ID (optional)")
    use_ai_explanation: Optional[bool] = Field(True, description="Whether to include Gemini explanations")

class ScanResponse(BaseModel):
    scan_id: str = Field(..., description="Unique scan identifier")
    repo: RepoDetails
    score: int = Field(..., description="Security score from 0 to 100")
    risk_level: str = Field(..., description="Risk level (Excellent, Good, Medium Risk, High Risk, Critical Risk)")
    summary: ScanSummary
    issues: List[Issue] = Field(default_list=[])
    detected_software: List[DetectedSoftware] = Field(default_list=[])
    ai_summary: Optional[str] = Field(None, description="Gemini-generated scan overview")

class ExplainRequest(BaseModel):
    issue_id: str = Field(..., description="ID of the issue to explain")
    user_id: Optional[str] = Field(None, description="Firebase user ID")
