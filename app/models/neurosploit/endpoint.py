from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlmodel import Field, Relationship, SQLModel

from app.utils.uuid7 import uuid7


class Endpoint(SQLModel, table=True):
    __tablename__ = "endpoints"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", ondelete="CASCADE")
    target_id: Optional[uuid.UUID] = Field(default=None, foreign_key="targets.id", ondelete="SET NULL")

    url: str = Field(sa_column=Column(Text))
    method: str = Field(default="GET", max_length=10, sa_column=Column(String(10)))
    path: Optional[str] = Field(default=None, sa_column=Column(Text))

    parameters: list = Field(default_factory=list, sa_column=Column(JSON))
    headers: dict = Field(default_factory=dict, sa_column=Column(JSON))

    response_status: Optional[int] = Field(default=None)
    content_type: Optional[str] = Field(default=None, max_length=100, sa_column=Column(String(100)))
    content_length: Optional[int] = Field(default=None)

    technologies: list = Field(default_factory=list, sa_column=Column(JSON))
    interesting: bool = Field(default=False)

    discovered_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    scan: "Scan" = Relationship(back_populates="endpoints")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "scan_id": str(self.scan_id),
            "target_id": str(self.target_id) if self.target_id else None,
            "url": self.url,
            "method": self.method,
            "path": self.path,
            "parameters": self.parameters,
            "headers": self.headers,
            "response_status": self.response_status,
            "content_type": self.content_type,
            "content_length": self.content_length,
            "technologies": self.technologies,
            "interesting": self.interesting,
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
        }
