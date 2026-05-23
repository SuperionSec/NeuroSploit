from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class ReportGenerate(SQLModel):
    scan_id: str = Field(..., description="Scan ID to generate report for")
    format: str = Field(default="html", description="Report format: html, pdf, json")
    title: Optional[str] = Field(default=None, description="Custom report title")
    include_executive_summary: bool = Field(default=True, description="Include executive summary")
    include_poc: bool = Field(default=True, description="Include proof of concept")
    include_remediation: bool = Field(default=True, description="Include remediation steps")
    preferred_provider: Optional[str] = Field(default=None, description="Preferred LLM provider for AI report generation")
    preferred_model: Optional[str] = Field(default=None, description="Preferred model for AI report generation")


class ReportPublic(SQLModel):
    id: str
    scan_id: str
    title: Optional[str]
    format: str
    file_path: Optional[str]
    executive_summary: Optional[str]
    auto_generated: bool
    is_partial: bool
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
