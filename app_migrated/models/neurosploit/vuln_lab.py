from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text
from sqlmodel import Field, SQLModel

from app.utils.uuid7 import uuid7


class VulnLabChallenge(SQLModel, table=True):
    __tablename__ = "vuln_lab_challenges"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)

    target_url: str = Field(sa_column=Column(Text))
    challenge_name: Optional[str] = Field(default=None, max_length=255, sa_column=Column(String(255)))

    vuln_type: str = Field(max_length=100, sa_column=Column(String(100)))
    vuln_category: Optional[str] = Field(default=None, max_length=50, sa_column=Column(String(50)))

    auth_type: Optional[str] = Field(default=None, max_length=20, sa_column=Column(String(20)))
    auth_value: Optional[str] = Field(default=None, sa_column=Column(Text))

    status: str = Field(default="pending", max_length=20, sa_column=Column(String(20)))
    result: Optional[str] = Field(default=None, max_length=20, sa_column=Column(String(20)))

    agent_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(String(36)))
    scan_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(String(36)))

    findings_count: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    info_count: int = Field(default=0)

    findings_detail: list = Field(default_factory=list, sa_column=Column(JSON))

    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    duration: Optional[int] = Field(default=None)

    notes: Optional[str] = Field(default=None, sa_column=Column(Text))

    logs: list = Field(default_factory=list, sa_column=Column(JSON))

    endpoints_count: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "target_url": self.target_url,
            "challenge_name": self.challenge_name,
            "vuln_type": self.vuln_type,
            "vuln_category": self.vuln_category,
            "auth_type": self.auth_type,
            "status": self.status,
            "result": self.result,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "scan_id": str(self.scan_id) if self.scan_id else None,
            "findings_count": self.findings_count,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "medium_count": self.medium_count,
            "low_count": self.low_count,
            "info_count": self.info_count,
            "findings_detail": self.findings_detail or [],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "notes": self.notes,
            "logs": self.logs or [],
            "endpoints_count": self.endpoints_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
