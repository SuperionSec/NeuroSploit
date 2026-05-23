from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlmodel import Field, Relationship, SQLModel

from app.utils.uuid7 import uuid7


class Target(SQLModel, table=True):
    __tablename__ = "targets"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", ondelete="CASCADE")

    url: str = Field(max_length=2048, sa_column=Column(String(2048)))
    hostname: Optional[str] = Field(default=None, max_length=255, sa_column=Column(String(255)))
    port: Optional[int] = Field(default=None)
    protocol: Optional[str] = Field(default=None, max_length=10, sa_column=Column(String(10)))
    path: Optional[str] = Field(default=None, max_length=2048, sa_column=Column(String(2048)))

    status: str = Field(default="pending", max_length=50, sa_column=Column(String(50)))

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    scan: "Scan" = Relationship(back_populates="targets")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "scan_id": str(self.scan_id),
            "url": self.url,
            "hostname": self.hostname,
            "port": self.port,
            "protocol": self.protocol,
            "path": self.path,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
