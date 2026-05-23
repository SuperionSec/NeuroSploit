from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlmodel import Field, Relationship, SQLModel

from app.utils.uuid7 import uuid7


class AgentTask(SQLModel, table=True):
    __tablename__ = "agent_tasks"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", ondelete="CASCADE")

    task_type: str = Field(max_length=50, sa_column=Column(String(50)))
    task_name: str = Field(max_length=255, sa_column=Column(String(255)))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))

    tool_name: Optional[str] = Field(default=None, max_length=100, sa_column=Column(String(100)))
    tool_category: Optional[str] = Field(default=None, max_length=50, sa_column=Column(String(50)))

    status: str = Field(default="pending", max_length=20, sa_column=Column(String(20)))

    started_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    completed_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    duration_ms: Optional[int] = Field(default=None)

    items_processed: int = Field(default=0)
    items_found: int = Field(default=0)
    result_summary: Optional[str] = Field(default=None, sa_column=Column(Text))

    error_message: Optional[str] = Field(default=None, sa_column=Column(Text))

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    scan: "Scan" = Relationship(back_populates="agent_tasks")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "scan_id": str(self.scan_id),
            "task_type": self.task_type,
            "task_name": self.task_name,
            "description": self.description,
            "tool_name": self.tool_name,
            "tool_category": self.tool_category,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "items_processed": self.items_processed,
            "items_found": self.items_found,
            "result_summary": self.result_summary,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def start(self):
        self.status = "running"
        self.started_at = datetime.utcnow()

    def complete(self, items_processed: int = 0, items_found: int = 0, summary: str = None):
        self.status = "completed"
        self.completed_at = datetime.utcnow()
        self.items_processed = items_processed
        self.items_found = items_found
        self.result_summary = summary
        if self.started_at:
            self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)

    def fail(self, error: str):
        self.status = "failed"
        self.completed_at = datetime.utcnow()
        self.error_message = error
        if self.started_at:
            self.duration_ms = int((self.completed_at - self.started_at).total_seconds() * 1000)
