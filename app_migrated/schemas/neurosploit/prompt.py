from datetime import datetime
from typing import Optional, List
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class PromptCreate(SQLModel):
    name: str = Field(..., max_length=255, description="Prompt name")
    description: Optional[str] = Field(default=None, description="Prompt description")
    content: str = Field(..., min_length=10, description="Prompt content")
    category: Optional[str] = Field(default=None, description="Prompt category")


class PromptUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class PromptPublic(SQLModel):
    id: str
    name: str
    description: Optional[str]
    content: str
    is_preset: bool
    category: Optional[str]
    parsed_vulnerabilities: List
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromptParse(SQLModel):
    content: str = Field(..., min_length=10, description="Prompt content to parse")
