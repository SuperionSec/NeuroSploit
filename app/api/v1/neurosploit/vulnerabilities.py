from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Vulnerability, Scan
from app.schemas.neurosploit import VulnerabilityPublic, VulnerabilityTypeInfo

router = APIRouter()

VULNERABILITY_TYPES = {
    "injection": {
        "xss_reflected": {"name": "Reflected XSS", "description": "Cross-site scripting via user input reflected in response", "severity_range": "medium-high", "owasp_category": "A03:2021", "cwe_ids": ["CWE-79"]},
        "xss_stored": {"name": "Stored XSS", "description": "Cross-site scripting stored in application database", "severity_range": "high-critical", "owasp_category": "A03:2021", "cwe_ids": ["CWE-79"]},
        "sqli_error": {"name": "Error-based SQL Injection", "description": "SQL injection detected via error messages", "severity_range": "high-critical", "owasp_category": "A03:2021", "cwe_ids": ["CWE-89"]},
        "sqli_union": {"name": "Union-based SQL Injection", "description": "SQL injection exploitable via UNION queries", "severity_range": "critical", "owasp_category": "A03:2021", "cwe_ids": ["CWE-89"]},
        "command_injection": {"name": "Command Injection", "description": "OS command injection vulnerability", "severity_range": "critical", "owasp_category": "A03:2021", "cwe_ids": ["CWE-78"]},
        "ssti": {"name": "Server-Side Template Injection", "description": "Template injection allowing code execution", "severity_range": "high-critical", "owasp_category": "A03:2021", "cwe_ids": ["CWE-94"]},
    },
    "file_access": {
        "lfi": {"name": "Local File Inclusion", "description": "Include local files via path manipulation", "severity_range": "high-critical", "owasp_category": "A01:2021", "cwe_ids": ["CWE-98"]},
        "rfi": {"name": "Remote File Inclusion", "description": "Include remote files for code execution", "severity_range": "critical", "owasp_category": "A01:2021", "cwe_ids": ["CWE-98"]},
        "path_traversal": {"name": "Path Traversal", "description": "Access files outside web root", "severity_range": "high", "owasp_category": "A01:2021", "cwe_ids": ["CWE-22"]},
        "xxe": {"name": "XML External Entity", "description": "XXE injection vulnerability", "severity_range": "high-critical", "owasp_category": "A05:2021", "cwe_ids": ["CWE-611"]},
    },
    "authentication": {
        "auth_bypass": {"name": "Authentication Bypass", "description": "Bypass authentication mechanisms", "severity_range": "critical", "owasp_category": "A07:2021", "cwe_ids": ["CWE-287"]},
        "jwt_manipulation": {"name": "JWT Token Manipulation", "description": "Manipulate JWT tokens for auth bypass", "severity_range": "high-critical", "owasp_category": "A07:2021", "cwe_ids": ["CWE-347"]},
    },
    "authorization": {
        "idor": {"name": "Insecure Direct Object Reference", "description": "Access objects without proper authorization", "severity_range": "high", "owasp_category": "A01:2021", "cwe_ids": ["CWE-639"]},
        "privilege_escalation": {"name": "Privilege Escalation", "description": "Escalate to higher privilege level", "severity_range": "critical", "owasp_category": "A01:2021", "cwe_ids": ["CWE-269"]},
    },
    "request_forgery": {
        "ssrf": {"name": "Server-Side Request Forgery", "description": "Forge requests from the server", "severity_range": "high-critical", "owasp_category": "A10:2021", "cwe_ids": ["CWE-918"]},
        "csrf": {"name": "Cross-Site Request Forgery", "description": "Forge requests as authenticated user", "severity_range": "medium-high", "owasp_category": "A01:2021", "cwe_ids": ["CWE-352"]},
    },
}


@router.get("/", response_model=List[VulnerabilityPublic])
async def list_vulnerabilities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    scan_id: Optional[str] = None,
):
    query = select(Vulnerability)
    if scan_id:
        scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
        if not scan:
            raise HTTPException(status_code=403, detail="Access denied to scan")
        query = query.where(Vulnerability.scan_id == scan_id)
    else:
        user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
        query = query.where(Vulnerability.scan_id.in_(user_scans))
    if severity:
        query = query.where(Vulnerability.severity == severity)
    query = query.order_by(Vulnerability.created_at.desc()).offset(skip).limit(limit)
    vulns = db.exec(query).all()
    return [VulnerabilityPublic(**v.model_dump()) for v in vulns]


@router.get("/types")
async def get_vulnerability_types():
    return VULNERABILITY_TYPES


@router.get("/types/{category}")
async def get_vulnerability_types_by_category(category: str):
    if category not in VULNERABILITY_TYPES:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    return VULNERABILITY_TYPES[category]


@router.get("/types/{category}/{vuln_type}", response_model=VulnerabilityTypeInfo)
async def get_vulnerability_type_info(category: str, vuln_type: str):
    if category not in VULNERABILITY_TYPES:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    if vuln_type not in VULNERABILITY_TYPES[category]:
        raise HTTPException(status_code=404, detail=f"Type '{vuln_type}' not found in category '{category}'")
    info = VULNERABILITY_TYPES[category][vuln_type]
    return VulnerabilityTypeInfo(type=vuln_type, category=category, **info)


@router.get("/{vuln_id}", response_model=VulnerabilityPublic)
async def get_vulnerability(
    vuln_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    vuln = db.exec(select(Vulnerability).where(Vulnerability.id == vuln_id)).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    scan = db.exec(select(Scan).where(Scan.id == vuln.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    return VulnerabilityPublic(**vuln.model_dump())


class ValidationRequest(BaseModel):
    validation_status: str
    notes: Optional[str] = None


@router.patch("/{vuln_id}/validate")
async def validate_vulnerability(
    vuln_id: str,
    body: ValidationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    valid_statuses = {"validated", "false_positive", "ai_confirmed", "ai_rejected", "pending_review"}
    if body.validation_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    vuln = db.exec(select(Vulnerability).where(Vulnerability.id == vuln_id)).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    vuln.validation_status = body.validation_status
    if body.notes:
        vuln.ai_rejection_reason = body.notes
    db.add(vuln)
    db.commit()
    return {"message": "Vulnerability validation updated", "vulnerability": vuln.model_dump()}


class FeedbackRequest(BaseModel):
    is_true_positive: bool
    explanation: str = ""


@router.post("/{vuln_id}/feedback")
async def submit_vulnerability_feedback(
    vuln_id: str,
    body: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    vuln = db.exec(select(Vulnerability).where(Vulnerability.id == vuln_id)).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    if len(body.explanation) < 3 and not body.is_true_positive:
        raise HTTPException(status_code=400, detail="Explanation required for false positive feedback")
    vuln.validation_status = "validated" if body.is_true_positive else "false_positive"
    if body.explanation:
        vuln.ai_rejection_reason = body.explanation
    db.add(vuln)
    db.commit()
    return {"message": "Feedback recorded", "vulnerability_id": vuln_id, "is_true_positive": body.is_true_positive}