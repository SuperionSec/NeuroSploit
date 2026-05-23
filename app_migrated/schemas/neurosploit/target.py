import re
from datetime import datetime
from typing import Optional, List
from pydantic import ConfigDict, field_validator
from sqlmodel import Field, SQLModel


class TargetCreate(SQLModel):
    url: str = Field(..., description="Target URL")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL cannot be empty")
        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if not url_pattern.match(v):
            if url_pattern.match(f"https://{v}"):
                return f"https://{v}"
            raise ValueError(f"Invalid URL format: {v}")
        return v


class TargetBulkCreate(SQLModel):
    urls: List[str] = Field(..., min_length=1, description="List of URLs")

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v: List[str]) -> List[str]:
        cleaned = []
        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        for url in v:
            url = url.strip()
            if not url:
                continue
            if url_pattern.match(url):
                cleaned.append(url)
            elif url_pattern.match(f"https://{url}"):
                cleaned.append(f"https://{url}")
        if not cleaned:
            raise ValueError("No valid URLs provided")
        return cleaned


class TargetPublic(SQLModel):
    id: str
    scan_id: str
    url: str
    hostname: Optional[str]
    port: Optional[int]
    protocol: Optional[str]
    path: Optional[str]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
