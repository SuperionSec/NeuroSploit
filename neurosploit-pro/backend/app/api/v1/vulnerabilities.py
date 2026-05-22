from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.vulnerability import Vulnerability
from app.schemas.vulnerability import VulnerabilityCreate, VulnerabilityResponse

router = APIRouter()


@router.get("/scan/{scan_id}", response_model=List[VulnerabilityResponse])
async def get_scan_vulnerabilities(
    scan_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Vulnerability).where(Vulnerability.scan_id == scan_id)
    )
    return result.scalars().all()


@router.get("/{vuln_id}", response_model=VulnerabilityResponse)
async def get_vulnerability(
    vuln_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Vulnerability).where(Vulnerability.id == vuln_id))
    vuln = result.scalar_one_or_none()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln


@router.post("/", response_model=VulnerabilityResponse, status_code=201)
async def create_vulnerability(
    vuln: VulnerabilityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_vuln = Vulnerability(
        id=str(uuid.uuid4()),
        scan_id=vuln.scan_id,
        title=vuln.title,
        vulnerability_type=vuln.vulnerability_type,
        severity=vuln.severity,
        cvss_score=vuln.cvss_score,
        description=vuln.description,
        affected_endpoint=vuln.affected_endpoint,
        poc_payload=vuln.poc_payload,
        remediation=vuln.remediation,
        references=[],
        validation_status="ai_confirmed"
    )
    db.add(db_vuln)
    await db.commit()
    await db.refresh(db_vuln)
    return db_vuln
