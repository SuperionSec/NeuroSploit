from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class VulnLabChallengePublic(SQLModel):
    id: str
    target_url: str
    challenge_name: Optional[str]
    vuln_type: str
    vuln_category: Optional[str]
    auth_type: Optional[str]
    status: str
    result: Optional[str]
    agent_id: Optional[str]
    scan_id: Optional[str]
    findings_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    findings_detail: list
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration: Optional[int]
    notes: Optional[str]
    logs: list
    endpoints_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VulnLabCreate(SQLModel):
    target_url: str = Field(..., description="Vulnerable target URL")
    challenge_name: Optional[str] = Field(default=None, description="Challenge name")
    vuln_type: str = Field(..., description="Vulnerability type to test")
    vuln_category: Optional[str] = Field(default=None, description="Vulnerability category")
    auth_type: Optional[str] = Field(default=None, description="Auth type for the challenge")
    auth_value: Optional[str] = Field(default=None, description="Auth value for the challenge")
