from typing import Optional, Dict, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Scan, Target, Vulnerability, Endpoint, Report, VulnLabChallenge

router = APIRouter()

VULN_CATEGORIES = {
    "injection": {
        "label": "Injection",
        "types": [
            "xss_reflected", "xss_stored", "xss_dom",
            "sqli_error", "sqli_union", "sqli_blind",
            "command_injection", "ssti", "nosql_injection",
        ],
    },
    "file_access": {
        "label": "File Access",
        "types": ["lfi", "rfi", "path_traversal", "xxe", "file_upload"],
    },
    "request_forgery": {
        "label": "Request Forgery",
        "types": ["ssrf", "csrf"],
    },
    "authentication": {
        "label": "Authentication",
        "types": ["auth_bypass", "jwt_manipulation", "session_fixation"],
    },
    "authorization": {
        "label": "Authorization",
        "types": ["idor", "bola", "privilege_escalation"],
    },
    "infrastructure": {
        "label": "Infrastructure",
        "types": ["security_headers", "ssl_issues", "http_methods"],
    },
}


class VulnLabRunRequest(BaseModel):
    target_url: str = Field(..., description="Target URL to test")
    vuln_type: str = Field(..., description="Vulnerability type to test")
    challenge_name: Optional[str] = Field(None, description="Challenge name")
    auth_type: Optional[str] = Field(None, description="Auth type")
    auth_value: Optional[str] = Field(None, description="Auth credential value")
    custom_headers: Optional[Dict[str, str]] = Field(None, description="Custom HTTP headers")


class VulnLabResponse(BaseModel):
    challenge_id: str
    agent_id: str
    status: str
    message: str


@router.get("/types")
async def list_vuln_types():
    result = {}
    for cat_key, cat_info in VULN_CATEGORIES.items():
        result[cat_key] = {
            "label": cat_info["label"],
            "types": [{"key": t, "title": t.replace("_", " ").title()} for t in cat_info["types"]],
            "count": len(cat_info["types"]),
        }
    return {"categories": result, "total_types": sum(len(c["types"]) for c in VULN_CATEGORIES.values())}


@router.post("/run", response_model=VulnLabResponse)
async def run_vuln_lab(
    request: VulnLabRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    import uuid

    valid_types = []
    for cat in VULN_CATEGORIES.values():
        valid_types.extend(cat["types"])
    if request.vuln_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Unknown vulnerability type: {request.vuln_type}")

    challenge_id = str(uuid.uuid4())
    agent_id = str(uuid.uuid4())[:8]

    challenge = VulnLabChallenge(
        id=challenge_id,
        target_url=request.target_url,
        challenge_name=request.challenge_name,
        vuln_type=request.vuln_type,
        status="running",
        agent_id=agent_id,
        started_at=datetime.utcnow(),
        created_by=current_user.id,
    )
    db.add(challenge)
    db.commit()

    return VulnLabResponse(
        challenge_id=challenge_id,
        agent_id=agent_id,
        status="running",
        message=f"Testing {request.vuln_type} against {request.target_url}",
    )


@router.get("/challenges")
async def list_challenges(
    vuln_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    query = select(VulnLabChallenge).where(VulnLabChallenge.created_by == current_user.id).order_by(
        VulnLabChallenge.created_at.desc()
    )
    if vuln_type:
        query = query.where(VulnLabChallenge.vuln_type == vuln_type)
    if status:
        query = query.where(VulnLabChallenge.status == status)
    challenges = db.exec(query.limit(limit)).all()
    return {"challenges": [c.model_dump() for c in challenges], "total": len(challenges)}


@router.get("/challenges/{challenge_id}")
async def get_challenge(
    challenge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    challenge = db.exec(
        select(VulnLabChallenge).where(
            VulnLabChallenge.id == challenge_id,
            VulnLabChallenge.created_by == current_user.id,
        )
    ).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge.model_dump()


@router.post("/challenges/{challenge_id}/stop")
async def stop_challenge(
    challenge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    challenge = db.exec(
        select(VulnLabChallenge).where(
            VulnLabChallenge.id == challenge_id,
            VulnLabChallenge.created_by == current_user.id,
        )
    ).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    challenge.status = "stopped"
    challenge.completed_at = datetime.utcnow()
    db.add(challenge)
    db.commit()
    return {"message": "Challenge stopped"}


@router.delete("/challenges/{challenge_id}")
async def delete_challenge(
    challenge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    challenge = db.exec(
        select(VulnLabChallenge).where(
            VulnLabChallenge.id == challenge_id,
            VulnLabChallenge.created_by == current_user.id,
        )
    ).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    db.delete(challenge)
    db.commit()
    return {"message": "Challenge deleted"}


@router.get("/stats")
async def get_lab_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    total = db.exec(
        select(func.count()).select_from(VulnLabChallenge).where(VulnLabChallenge.created_by == current_user.id)
    ).one() or 0
    running = db.exec(
        select(func.count()).select_from(VulnLabChallenge).where(
            VulnLabChallenge.status == "running",
            VulnLabChallenge.created_by == current_user.id,
        )
    ).one() or 0
    completed = db.exec(
        select(func.count()).select_from(VulnLabChallenge).where(
            VulnLabChallenge.status == "completed",
            VulnLabChallenge.created_by == current_user.id,
        )
    ).one() or 0
    return {
        "total": total,
        "running": running,
        "completed": completed,
        "detection_rate": 0,
    }