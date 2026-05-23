from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlmodel import Field, Relationship, SQLModel

from app.utils.uuid7 import uuid7


class Report(SQLModel, table=True):
    __tablename__ = "reports"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", ondelete="CASCADE")

    title: Optional[str] = Field(default=None, max_length=255, sa_column=Column(String(255)))
    format: str = Field(default="html", max_length=20, sa_column=Column(String(20)))
    file_path: Optional[str] = Field(default=None, sa_column=Column(Text))

    executive_summary: Optional[str] = Field(default=None, sa_column=Column(Text))

    auto_generated: bool = Field(default=False)
    is_partial: bool = Field(default=False)

    generated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    scan: "Scan" = Relationship(back_populates="reports")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "scan_id": str(self.scan_id),
            "title": self.title,
            "format": self.format,
            "file_path": self.file_path,
            "executive_summary": self.executive_summary,
            "auto_generated": self.auto_generated,
            "is_partial": self.is_partial,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
