from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Prompt
from app.schemas.neurosploit import PromptCreate, PromptUpdate, PromptPublic, PromptPreset, PromptParse, PromptParseResult

router = APIRouter()

PRESET_PROMPTS = [
    {
        "id": "full_pentest",
        "name": "Full Penetration Test",
        "description": "Comprehensive security assessment covering all vulnerability categories",
        "category": "pentest",
        "content": "Perform a comprehensive penetration test on the target application. Test for ALL vulnerability categories including injection, authentication, authorization, file handling, request forgery, API security, client-side, information disclosure, infrastructure, and business logic flaws.",
    },
    {
        "id": "owasp_top10",
        "name": "OWASP Top 10",
        "description": "Test for OWASP Top 10 2021 vulnerabilities",
        "category": "compliance",
        "content": "Test for OWASP Top 10 2021 vulnerabilities: Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Authentication Failures, Data Integrity Failures, Logging Failures, SSRF.",
    },
    {
        "id": "api_security",
        "name": "API Security Testing",
        "description": "Focused testing for REST and GraphQL APIs",
        "category": "api",
        "content": "Perform API security testing: authentication & authorization, input validation, data exposure, GraphQL specific tests, API abuse testing.",
    },
    {
        "id": "bug_bounty",
        "name": "Bug Bounty Hunter",
        "description": "Focus on high-impact, bounty-worthy vulnerabilities",
        "category": "bug_bounty",
        "content": "Hunt for high-impact vulnerabilities: RCE, SQL injection leading to data breach, authentication bypass, SSRF to internal services, privilege escalation to admin, stored XSS, IDOR, account takeover, payment manipulation, PII exposure.",
    },
    {
        "id": "quick_scan",
        "name": "Quick Security Scan",
        "description": "Fast scan for common vulnerabilities",
        "category": "quick",
        "content": "Perform a quick security scan: reflected XSS, basic SQL injection, directory traversal, security headers check, SSL/TLS configuration, common misconfigurations, information disclosure.",
    },
    {
        "id": "auth_testing",
        "name": "Authentication Testing",
        "description": "Focus on authentication and session management",
        "category": "auth",
        "content": "Test authentication and session management: login functionality, session management, password reset, multi-factor authentication, OAuth/SSO.",
    },
]


@router.get("/presets", response_model=List[PromptPreset])
async def get_preset_prompts():
    return [
        PromptPreset(
            id=p["id"],
            name=p["name"],
            description=p["description"],
            category=p["category"],
            vulnerability_count=len(p["content"].split("\n")),
        )
        for p in PRESET_PROMPTS
    ]


@router.get("/presets/{preset_id}")
async def get_preset_prompt(preset_id: str):
    for preset in PRESET_PROMPTS:
        if preset["id"] == preset_id:
            return preset
    raise HTTPException(status_code=404, detail="Preset not found")


@router.post("/parse", response_model=PromptParseResult)
async def parse_prompt(
    prompt_data: PromptParse,
    current_user: User = Depends(get_current_active_user),
):
    vulnerabilities_to_test = []
    keywords = {
        "xss": ("XSS", "Cross-Site Scripting"),
        "sqli": ("SQL Injection", "SQL Injection"),
        "ssrf": ("SSRF", "Server-Side Request Forgery"),
        "csrf": ("CSRF", "Cross-Site Request Forgery"),
        "lfi": ("LFI", "Local File Inclusion"),
        "rce": ("RCE", "Remote Code Execution"),
    }
    for keyword, (name, description) in keywords.items():
        if keyword in prompt_data.content.lower():
            vulnerabilities_to_test.append(
                {"type": keyword, "name": name, "description": description, "detected_in_prompt": True}
            )
    return PromptParseResult(
        content=prompt_data.content,
        vulnerabilities_to_test=vulnerabilities_to_test,
        total_vulnerabilities=len(vulnerabilities_to_test),
    )


@router.get("/", response_model=List[PromptPublic])
async def list_prompts(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    query = select(Prompt).where(Prompt.is_preset == False, Prompt.created_by == current_user.id)
    if category:
        query = query.where(Prompt.category == category)
    prompts = db.exec(query.order_by(Prompt.created_at.desc()).offset(skip).limit(limit)).all()
    return [PromptPublic(**p.model_dump()) for p in prompts]


@router.post("/", response_model=PromptPublic, status_code=201)
async def create_prompt(
    prompt_data: PromptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prompt = Prompt(
        created_by=current_user.id,
        is_preset=False,
        **prompt_data.model_dump(),
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return PromptPublic(**prompt.model_dump())


@router.get("/{prompt_id}", response_model=PromptPublic)
async def get_prompt(
    prompt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prompt = db.exec(
        select(Prompt).where(Prompt.id == prompt_id, Prompt.created_by == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return PromptPublic(**prompt.model_dump())


@router.put("/{prompt_id}", response_model=PromptPublic)
async def update_prompt(
    prompt_id: str,
    prompt_data: PromptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prompt = db.exec(
        select(Prompt).where(Prompt.id == prompt_id, Prompt.created_by == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.is_preset:
        raise HTTPException(status_code=400, detail="Cannot modify preset prompts")
    for key, value in prompt_data.model_dump(exclude_unset=True).items():
        setattr(prompt, key, value)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return PromptPublic(**prompt.model_dump())


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prompt = db.exec(
        select(Prompt).where(Prompt.id == prompt_id, Prompt.created_by == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.is_preset:
        raise HTTPException(status_code=400, detail="Cannot delete preset prompts")
    db.delete(prompt)
    db.commit()
    return {"message": "Prompt deleted"}


@router.post("/upload")
async def upload_prompt(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in {".md", ".txt"}:
        raise HTTPException(status_code=400, detail="Invalid file type. Use .md or .txt")
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unable to decode file")
    return {"filename": file.filename, "content": text}