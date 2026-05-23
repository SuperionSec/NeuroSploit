from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, JSON, String, Text
from sqlmodel import Field, SQLModel

from app.utils.uuid7 import uuid7


class Prompt(SQLModel, table=True):
    __tablename__ = "prompts"

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(max_length=255, sa_column=Column(String(255)))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    content: str = Field(sa_column=Column(Text))

    is_preset: bool = Field(default=False)
    category: Optional[str] = Field(default=None, max_length=100, sa_column=Column(String(100)))

    parsed_vulnerabilities: list = Field(default_factory=list, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "content": self.content,
            "is_preset": self.is_preset,
            "category": self.category,
            "parsed_vulnerabilities": self.parsed_vulnerabilities,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
