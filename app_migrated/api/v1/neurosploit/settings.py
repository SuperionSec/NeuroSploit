import os
import re
from pathlib import Path
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, func, delete

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Scan, Target, Endpoint, Vulnerability, Report

router = APIRouter()

ENV_FILE_PATH = Path(__file__).parent.parent.parent.parent.parent / ".env"


class SettingsUpdate(BaseModel):
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    ollama_base_url: Optional[str] = None
    max_concurrent_scans: Optional[int] = None
    aggressive_mode: Optional[bool] = None
    default_scan_type: Optional[str] = None
    recon_enabled_by_default: Optional[bool] = None
    enable_model_routing: Optional[bool] = None
    enable_browser_validation: Optional[bool] = None
    max_output_tokens: Optional[int] = None


class SettingsResponse(BaseModel):
    llm_provider: str = "claude"
    llm_model: str = ""
    has_anthropic_key: bool = False
    has_openai_key: bool = False
    has_openrouter_key: bool = False
    has_gemini_key: bool = False
    ollama_base_url: str = ""
    max_concurrent_scans: int = 3
    aggressive_mode: bool = False
    default_scan_type: str = "full"
    recon_enabled_by_default: bool = True
    enable_model_routing: bool = False
    enable_browser_validation: bool = False
    max_output_tokens: Optional[int] = None


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: User = Depends(get_current_active_user),
):
    return SettingsResponse(
        llm_provider=os.getenv("LLM_PROVIDER", "claude"),
        llm_model=os.getenv("DEFAULT_LLM_MODEL", ""),
        has_anthropic_key=bool(os.getenv("ANTHROPIC_API_KEY")),
        has_openai_key=bool(os.getenv("OPENAI_API_KEY")),
        has_openrouter_key=bool(os.getenv("OPENROUTER_API_KEY")),
        has_gemini_key=bool(os.getenv("GEMINI_API_KEY")),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", ""),
        max_concurrent_scans=int(os.getenv("MAX_CONCURRENT_SCANS", "3")),
        aggressive_mode=os.getenv("AGGRESSIVE_MODE", "").lower() in ("true", "1"),
        default_scan_type=os.getenv("DEFAULT_SCAN_TYPE", "full"),
        recon_enabled_by_default=os.getenv("RECON_ENABLED_BY_DEFAULT", "true").lower() in ("true", "1"),
        enable_model_routing=os.getenv("ENABLE_MODEL_ROUTING", "").lower() in ("true", "1"),
        enable_browser_validation=os.getenv("ENABLE_BROWSER_VALIDATION", "").lower() in ("true", "1"),
        max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS")) if os.getenv("MAX_OUTPUT_TOKENS") else None,
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    settings_data: SettingsUpdate,
    current_user: User = Depends(get_current_active_user),
):
    env_updates: Dict[str, str] = {}
    if settings_data.llm_provider is not None:
        os.environ["LLM_PROVIDER"] = settings_data.llm_provider
        env_updates["LLM_PROVIDER"] = settings_data.llm_provider
    if settings_data.llm_model is not None:
        os.environ["DEFAULT_LLM_MODEL"] = settings_data.llm_model
        env_updates["DEFAULT_LLM_MODEL"] = settings_data.llm_model
    if settings_data.anthropic_api_key is not None:
        os.environ["ANTHROPIC_API_KEY"] = settings_data.anthropic_api_key
        env_updates["ANTHROPIC_API_KEY"] = settings_data.anthropic_api_key
    if settings_data.openai_api_key is not None:
        os.environ["OPENAI_API_KEY"] = settings_data.openai_api_key
        env_updates["OPENAI_API_KEY"] = settings_data.openai_api_key
    if settings_data.openrouter_api_key is not None:
        os.environ["OPENROUTER_API_KEY"] = settings_data.openrouter_api_key
        env_updates["OPENROUTER_API_KEY"] = settings_data.openrouter_api_key
    if settings_data.gemini_api_key is not None:
        os.environ["GEMINI_API_KEY"] = settings_data.gemini_api_key
        env_updates["GEMINI_API_KEY"] = settings_data.gemini_api_key
    if settings_data.ollama_base_url is not None:
        os.environ["OLLAMA_BASE_URL"] = settings_data.ollama_base_url
        env_updates["OLLAMA_BASE_URL"] = settings_data.ollama_base_url
    if settings_data.max_concurrent_scans is not None:
        os.environ["MAX_CONCURRENT_SCANS"] = str(settings_data.max_concurrent_scans)
        env_updates["MAX_CONCURRENT_SCANS"] = str(settings_data.max_concurrent_scans)
    if settings_data.aggressive_mode is not None:
        val = str(settings_data.aggressive_mode).lower()
        os.environ["AGGRESSIVE_MODE"] = val
        env_updates["AGGRESSIVE_MODE"] = val
    if settings_data.default_scan_type is not None:
        os.environ["DEFAULT_SCAN_TYPE"] = settings_data.default_scan_type
        env_updates["DEFAULT_SCAN_TYPE"] = settings_data.default_scan_type
    if settings_data.recon_enabled_by_default is not None:
        val = str(settings_data.recon_enabled_by_default).lower()
        os.environ["RECON_ENABLED_BY_DEFAULT"] = val
        env_updates["RECON_ENABLED_BY_DEFAULT"] = val
    if settings_data.enable_model_routing is not None:
        val = str(settings_data.enable_model_routing).lower()
        os.environ["ENABLE_MODEL_ROUTING"] = val
        env_updates["ENABLE_MODEL_ROUTING"] = val
    if settings_data.enable_browser_validation is not None:
        val = str(settings_data.enable_browser_validation).lower()
        os.environ["ENABLE_BROWSER_VALIDATION"] = val
        env_updates["ENABLE_BROWSER_VALIDATION"] = val
    if settings_data.max_output_tokens is not None:
        os.environ["MAX_OUTPUT_TOKENS"] = str(settings_data.max_output_tokens)
        env_updates["MAX_OUTPUT_TOKENS"] = str(settings_data.max_output_tokens)
    if env_updates and ENV_FILE_PATH.exists():
        _update_env_file(env_updates)
    return await get_settings(current_user=current_user)


def _update_env_file(updates: Dict[str, str]) -> bool:
    if not ENV_FILE_PATH.exists():
        return False
    try:
        lines = ENV_FILE_PATH.read_text().splitlines()
        updated_keys = set()
        new_lines = []
        for line in lines:
            stripped = line.strip()
            matched = False
            for key, value in updates.items():
                pattern = rf'^#?\s*{re.escape(key)}\s*='
                if re.match(pattern, stripped):
                    new_lines.append(f"{key}={value}")
                    updated_keys.add(key)
                    matched = True
                    break
            if not matched:
                new_lines.append(line)
        for key, value in updates.items():
            if key not in updated_keys:
                new_lines.append(f"{key}={value}")
        ENV_FILE_PATH.write_text("\n".join(new_lines) + "\n")
        return True
    except Exception:
        return False


@router.post("/clear-database")
async def clear_database(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db.exec(delete(Vulnerability))
    db.exec(delete(Endpoint))
    db.exec(delete(Report))
    db.exec(delete(Target))
    db.exec(delete(Scan))
    db.commit()
    return {"message": "Database cleared successfully", "status": "success"}


@router.get("/stats")
async def get_database_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user_scans = select(Scan.id).where(Scan.created_by == current_user.id)
    scans_count = db.exec(select(func.count()).select_from(Scan).where(Scan.created_by == current_user.id)).one() or 0
    vulns_count = db.exec(select(func.count()).select_from(Vulnerability).where(Vulnerability.scan_id.in_(user_scans))).one() or 0
    endpoints_count = db.exec(select(func.count()).select_from(Endpoint).where(Endpoint.scan_id.in_(user_scans))).one() or 0
    reports_count = db.exec(select(func.count()).select_from(Report).where(Report.scan_id.in_(user_scans))).one() or 0
    return {"scans": scans_count, "vulnerabilities": vulns_count, "endpoints": endpoints_count, "reports": reports_count}