from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class AgentTaskCreate(SQLModel):
    scan_id: str = Field(..., description="Scan ID this task belongs to")
    task_type: str = Field(..., description="Task type: recon, analysis, testing, reporting")
    task_name: str = Field(..., description="Human-readable task name")
    description: Optional[str] = Field(default=None, description="Task description")
    tool_name: Optional[str] = Field(default=None, description="Tool being used")
    tool_category: Optional[str] = Field(default=None, description="Tool category")


class AgentTaskUpdate(SQLModel):
    status: Optional[str] = Field(default=None, description="Task status")
    items_processed: Optional[int] = Field(default=None, description="Items processed")
    items_found: Optional[int] = Field(default=None, description="Items found")
    result_summary: Optional[str] = Field(default=None, description="Result summary")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")


class AgentTaskPublic(SQLModel):
    id: str
    scan_id: str
    task_type: str
    task_name: str
    description: Optional[str]
    tool_name: Optional[str]
    tool_category: Optional[str]
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_ms: Optional[int]
    items_processed: int
    items_found: int
    result_summary: Optional[str]
    error_message: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentTaskSummary(SQLModel):
    total: int
    pending: int
    running: int
    completed: int
    failed: int
    by_type: dict
    by_tool: dict
