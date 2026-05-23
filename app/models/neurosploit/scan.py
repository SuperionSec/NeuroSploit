from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlmodel import Field, Relationship, SQLModel

from app.utils.uuid7 import uuid7


class Scan(SQLModel, table=True):
    __tablename__ = "scans"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=255, sa_column=Column(String(255)))
    status: str = Field(default="pending", max_length=50, sa_column=Column(String(50)))
    scan_type: str = Field(default="full", max_length=50, sa_column=Column(String(50)))
    recon_enabled: bool = Field(default=True)

    progress: int = Field(default=0)
    current_phase: Optional[str] = Field(default=None, max_length=50, sa_column=Column(String(50)))

    config: dict = Field(default_factory=dict, sa_column=Column(JSON))

    custom_prompt: Optional[str] = Field(default=None, sa_column=Column(Text))
    prompt_id: Optional[uuid.UUID] = Field(default=None, sa_column=Column(String(36)))

    auth_type: Optional[str] = Field(default=None, max_length=50, sa_column=Column(String(50)))
    auth_credentials: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    custom_headers: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    duration: Optional[int] = Field(default=None)

    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))

    total_endpoints: int = Field(default=0)
    total_vulnerabilities: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    info_count: int = Field(default=0)

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    targets: List["Target"] = Relationship(back_populates="scan", cascade_delete=True)
    endpoints: List["Endpoint"] = Relationship(back_populates="scan", cascade_delete=True)
    vulnerabilities: List["Vulnerability"] = Relationship(back_populates="scan", cascade_delete=True)
    reports: List["Report"] = Relationship(back_populates="scan", cascade_delete=True)
    agent_tasks: List["AgentTask"] = Relationship(back_populates="scan", cascade_delete=True)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "status": self.status,
            "scan_type": self.scan_type,
            "recon_enabled": self.recon_enabled,
            "progress": self.progress,
            "current_phase": self.current_phase,
            "config": self.config,
            "custom_prompt": self.custom_prompt,
            "prompt_id": str(self.prompt_id) if self.prompt_id else None,
            "auth_type": self.auth_type,
            "auth_credentials": self.auth_credentials,
            "custom_headers": self.custom_headers,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "error_message": self.error_message,
            "total_endpoints": self.total_endpoints,
            "total_vulnerabilities": self.total_vulnerabilities,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "medium_count": self.medium_count,
            "low_count": self.low_count,
            "info_count": self.info_count,
        }
