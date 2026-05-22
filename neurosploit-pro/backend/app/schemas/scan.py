from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class ScanBase(BaseModel):
    name: str
    scan_type: str = "full"
    target_url: str
    config: Optional[Dict] = {}


class ScanCreate(ScanBase):
    pass


class ScanUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None


class ScanResponse(ScanBase):
    id: str
    status: str
    progress: int
    current_phase: Optional[str]
    created_by: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    total_endpoints: int
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

    class Config:
        from_attributes = True
