from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import SQLModel


class EndpointPublic(SQLModel):
    id: str
    scan_id: str
    target_id: Optional[str]
    url: str
    method: str
    path: Optional[str]
    parameters: list
    headers: dict
    response_status: Optional[int]
    content_type: Optional[str]
    content_length: Optional[int]
    technologies: list
    interesting: bool
    discovered_at: datetime

    model_config = ConfigDict(from_attributes=True)
