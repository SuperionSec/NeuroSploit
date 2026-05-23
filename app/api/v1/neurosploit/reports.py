from typing import List, Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Report, Scan, Vulnerability
from app.schemas.neurosploit import (
    ReportPublic,
    ReportListResponse,
    ReportGenerate,
)

router = APIRouter()


@router.get("/", response_model=ReportListResponse)
async def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    scan_id: Optional[str] = None,
):
    user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
    query = select(Report).where(Report.scan_id.in_(user_scans)).order_by(Report.generated_at.desc())
    if scan_id:
        query = query.where(Report.scan_id == scan_id)
    total = db.exec(select(func.count()).select_from(Report).where(Report.scan_id.in_(user_scans))).one()
    reports = db.exec(query.offset(skip).limit(limit)).all()
    return ReportListResponse(
        reports=[ReportPublic(**r.model_dump()) for r in reports],
        total=total,
    )


@router.post("/", response_model=ReportPublic, status_code=201)
async def generate_report(
    report_data: ReportGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(select(Scan).where(Scan.id == report_data.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    report = Report(
        scan_id=scan.id,
        title=report_data.title or f"Report - {scan.name}",
        format=report_data.format,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return ReportPublic(**report.model_dump())


@router.get("/{report_id}", response_model=ReportPublic)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    report = db.exec(select(Report).where(Report.id == report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    scan = db.exec(select(Scan).where(Scan.id == report.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    return ReportPublic(**report.model_dump())


@router.get("/{report_id}/view")
async def view_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    report = db.exec(select(Report).where(Report.id == report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    scan = db.exec(select(Scan).where(Scan.id == report.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    if not report.file_path:
        raise HTTPException(status_code=404, detail="Report file not found")
    file_path = Path(report.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found on disk")
    if report.format == "html":
        return HTMLResponse(content=file_path.read_text())
    return FileResponse(path=str(file_path), media_type="application/octet-stream", filename=file_path.name)


@router.get("/{report_id}/download/{format}")
async def download_report(
    report_id: str,
    format: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    report = db.exec(select(Report).where(Report.id == report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    scan = db.exec(select(Scan).where(Scan.id == report.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    if not report.file_path:
        raise HTTPException(status_code=404, detail="Report file not found")
    file_path = Path(report.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found on disk")
    media_types = {"html": "text/html", "pdf": "application/pdf", "json": "application/json"}
    return FileResponse(
        path=str(file_path),
        media_type=media_types.get(format, "application/octet-stream"),
        filename=file_path.name,
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    report = db.exec(select(Report).where(Report.id == report_id)).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    scan = db.exec(select(Scan).where(Scan.id == report.scan_id, Scan.created_by == current_user.id)).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    if report.file_path:
        fp = Path(report.file_path)
        if fp.exists():
            fp.unlink()
    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}