from pydantic import BaseModel, Field
from typing import Optional

class Issue(BaseModel):
    issue_id: Optional[str] = Field(None, description="Unique identifier for the issue")
    scan_id: Optional[str] = Field(None, description="Associated scan identifier")
    user_id: Optional[str] = Field(None, description="Owner user identifier")
    type: str = Field(..., description="Type/Category of the security issue (e.g. Secret, Config, Dependency)")
    severity: str = Field(..., description="Severity level: Critical, High, Medium, Low")
    file: str = Field(..., description="File path relative to repository root")
    line: Optional[int] = Field(None, description="Line number of the issue, if applicable")
    message: str = Field(..., description="Detailed message describing the finding")
    fix: str = Field(..., description="Actionable fix recommendation")
    studentExplanation: Optional[str] = Field(None, description="Student-friendly educational explanation of the vulnerability")
