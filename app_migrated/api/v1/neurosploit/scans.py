from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Scan, Target, Endpoint, Vulnerability
from app.schemas.neurosploit import (
    ScanCreate,
    ScanUpdate,
    ScanPublic,
    ScanListResponse,
    ScanProgress,
    ScanTargetsResponse,
)

router = APIRouter()


@router.get("/", response_model=ScanListResponse)
async def list_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
):
    query = select(Scan).where(Scan.created_by == current_user.id).order_by(Scan.created_at.desc())
    if status:
        query = query.where(Scan.status == status)
    total = db.exec(select(func.count()).select_from(Scan).where(Scan.created_by == current_user.id)).one()
    scans = db.exec(query.offset(skip).limit(limit)).all()
    scan_responses = []
    for scan in scans:
        targets = db.exec(select(Target).where(Target.scan_id == scan.id)).all()
        sd = scan.model_dump()
        sd["targets"] = [t.model_dump() for t in targets]
        scan_responses.append(ScanPublic(**sd))
    return ScanListResponse(scans=scan_responses, total=total, page=skip // limit + 1, per_page=limit)


@router.post("/", response_model=ScanPublic, status_code=201)
async def create_scan(
    scan_data: ScanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = Scan(
        name=scan_data.name or f"Scan {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        scan_type=scan_data.scan_type,
        recon_enabled=scan_data.recon_enabled,
        custom_prompt=scan_data.custom_prompt,
        config=scan_data.config,
        status="pending",
        created_by=current_user.id,
    )
    db.add(scan)
    db.flush()
    targets = []
    for url in scan_data.targets:
        target = Target(
            scan_id=scan.id,
            url=url,
        )
        db.add(target)
        targets.append(target)
    db.commit()
    db.refresh(scan)
    sd = scan.model_dump()
    sd["targets"] = [t.model_dump() for t in targets]
    return ScanPublic(**sd)


@router.get("/{scan_id}", response_model=ScanPublic)
async def get_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    targets = db.exec(select(Target).where(Target.scan_id == scan_id)).all()
    sd = scan.model_dump()
    sd["targets"] = [t.model_dump() for t in targets]
    return ScanPublic(**sd)


@router.put("/{scan_id}", response_model=ScanPublic)
async def update_scan(
    scan_id: str,
    scan_data: ScanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    for key, value in scan_data.model_dump(exclude_unset=True).items():
        setattr(scan, key, value)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    targets = db.exec(select(Target).where(Target.scan_id == scan_id)).all()
    sd = scan.model_dump()
    sd["targets"] = [t.model_dump() for t in targets]
    return ScanPublic(**sd)


@router.delete("/{scan_id}")
async def delete_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status == "running":
        raise HTTPException(status_code=400, detail="Cannot delete running scan")
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted", "scan_id": scan_id}


@router.post("/{scan_id}/start")
async def start_scan(
    scan_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status == "running":
        raise HTTPException(status_code=400, detail="Scan is already running")
    scan.status = "running"
    scan.started_at = datetime.utcnow()
    scan.current_phase = "initializing"
    scan.progress = 0
    db.add(scan)
    db.commit()
    return {"message": "Scan started", "scan_id": scan_id}


@router.post("/{scan_id}/stop")
async def stop_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status not in ("running", "paused"):
        raise HTTPException(status_code=400, detail="Scan is not running or paused")
    scan.status = "stopped"
    scan.completed_at = datetime.utcnow()
    scan.current_phase = "stopped"
    if scan.started_at:
        scan.duration = int((scan.completed_at - scan.started_at).total_seconds())
    for severity in ["critical", "high", "medium", "low", "info"]:
        count = db.exec(
            select(func.count()).select_from(Vulnerability)
            .where(Vulnerability.scan_id == scan_id, Vulnerability.severity == severity)
        ).one()
        setattr(scan, f"{severity}_count", count or 0)
    total_vuln = db.exec(
        select(func.count()).select_from(Vulnerability).where(Vulnerability.scan_id == scan_id)
    ).one()
    scan.total_vulnerabilities = total_vuln or 0
    total_ep = db.exec(
        select(func.count()).select_from(Endpoint).where(Endpoint.scan_id == scan_id)
    ).one()
    scan.total_endpoints = total_ep or 0
    db.add(scan)
    db.commit()
    summary = {
        "total_endpoints": scan.total_endpoints,
        "total_vulnerabilities": scan.total_vulnerabilities,
        "critical": scan.critical_count,
        "high": scan.high_count,
        "medium": scan.medium_count,
        "low": scan.low_count,
        "info": scan.info_count,
        "duration": scan.duration,
        "progress": scan.progress,
    }
    return {"message": "Scan stopped", "scan_id": scan_id, "summary": summary}


@router.post("/{scan_id}/pause")
async def pause_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status != "running":
        raise HTTPException(status_code=400, detail="Scan is not running")
    scan.status = "paused"
    scan.current_phase = "paused"
    db.add(scan)
    db.commit()
    return {"message": "Scan paused", "scan_id": scan_id}


@router.post("/{scan_id}/resume")
async def resume_scan(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.status != "paused":
        raise HTTPException(status_code=400, detail="Scan is not paused")
    scan.status = "running"
    scan.current_phase = "testing"
    db.add(scan)
    db.commit()
    return {"message": "Scan resumed", "scan_id": scan_id}


@router.get("/{scan_id}/status", response_model=ScanProgress)
async def get_scan_status(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return ScanProgress(
        scan_id=scan.id,
        status=scan.status,
        progress=scan.progress,
        current_phase=scan.current_phase,
        total_endpoints=scan.total_endpoints,
        total_vulnerabilities=scan.total_vulnerabilities,
    )


@router.get("/{scan_id}/endpoints")
async def get_scan_endpoints(
    scan_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    total = db.exec(select(func.count()).select_from(Endpoint).where(Endpoint.scan_id == scan_id)).one()
    endpoints = db.exec(
        select(Endpoint).where(Endpoint.scan_id == scan_id).order_by(Endpoint.discovered_at.desc()).offset(skip).limit(limit)
    ).all()
    return {"endpoints": [e.model_dump() for e in endpoints], "total": total, "page": skip // limit + 1, "per_page": limit}


@router.get("/{scan_id}/vulnerabilities")
async def get_scan_vulnerabilities(
    scan_id: str,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    query = select(Vulnerability).where(Vulnerability.scan_id == scan_id)
    if severity:
        query = query.where(Vulnerability.severity == severity)
    query = query.order_by(Vulnerability.created_at.desc()).offset(skip).limit(limit)
    total = db.exec(
        select(func.count()).select_from(Vulnerability).where(Vulnerability.scan_id == scan_id)
    ).one()
    vulnerabilities = db.exec(query).all()
    return {
        "vulnerabilities": [v.model_dump() for v in vulnerabilities],
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
    }