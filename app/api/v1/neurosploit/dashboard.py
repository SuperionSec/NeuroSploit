from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Scan, Vulnerability, Endpoint, AgentTask, Report

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user_scans = select(Scan.id).where(Scan.created_by == current_user.id)
    total_scans = db.exec(select(func.count()).select_from(Scan).where(Scan.created_by == current_user.id)).one() or 0
    running_scans = db.exec(
        select(func.count()).select_from(Scan).where(Scan.status == "running", Scan.created_by == current_user.id)
    ).one() or 0
    completed_scans = db.exec(
        select(func.count()).select_from(Scan).where(Scan.status == "completed", Scan.created_by == current_user.id)
    ).one() or 0
    failed_scans = db.exec(
        select(func.count()).select_from(Scan).where(Scan.status == "failed", Scan.created_by == current_user.id)
    ).one() or 0
    pending_scans = db.exec(
        select(func.count()).select_from(Scan).where(Scan.status == "pending", Scan.created_by == current_user.id)
    ).one() or 0
    vuln_counts = {}
    for severity in ["critical", "high", "medium", "low", "info"]:
        vc = db.exec(
            select(func.count()).select_from(Vulnerability).where(
                Vulnerability.severity == severity,
                Vulnerability.scan_id.in_(user_scans),
            )
        ).one() or 0
        vuln_counts[severity] = vc
    total_vulns = sum(vuln_counts.values())
    total_endpoints = db.exec(
        select(func.count()).select_from(Endpoint).where(Endpoint.scan_id.in_(user_scans))
    ).one() or 0
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_scans = db.exec(
        select(func.count()).select_from(Scan).where(Scan.created_at >= week_ago, Scan.created_by == current_user.id)
    ).one() or 0
    recent_vulns = db.exec(
        select(func.count()).select_from(Vulnerability).where(
            Vulnerability.created_at >= week_ago,
            Vulnerability.scan_id.in_(user_scans),
        )
    ).one() or 0
    return {
        "scans": {
            "total": total_scans,
            "running": running_scans,
            "completed": completed_scans,
            "failed": failed_scans,
            "pending": pending_scans,
            "recent": recent_scans,
        },
        "vulnerabilities": {
            "total": total_vulns,
            "critical": vuln_counts["critical"],
            "high": vuln_counts["high"],
            "medium": vuln_counts["medium"],
            "low": vuln_counts["low"],
            "info": vuln_counts["info"],
            "recent": recent_vulns,
        },
        "endpoints": {"total": total_endpoints},
    }


@router.get("/activity-feed")
async def get_activity_feed(
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    activities = []
    user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
    scans = db.exec(
        select(Scan).where(Scan.created_by == current_user.id).order_by(Scan.created_at.desc()).limit(limit // 3)
    ).all()
    for scan in scans:
        activities.append({
            "type": "scan",
            "action": f"Scan {scan.status}",
            "title": scan.name or "Unnamed Scan",
            "description": f"{scan.total_vulnerabilities} vulnerabilities found",
            "status": scan.status,
            "severity": None,
            "timestamp": scan.created_at.isoformat(),
            "scan_id": scan.id,
            "link": f"/scan/{scan.id}",
        })
    vulns = db.exec(
        select(Vulnerability)
        .where(Vulnerability.scan_id.in_(user_scans))
        .order_by(Vulnerability.created_at.desc())
        .limit(limit // 3)
    ).all()
    for vuln in vulns:
        activities.append({
            "type": "vulnerability",
            "action": "Vulnerability found",
            "title": vuln.title,
            "description": vuln.affected_endpoint or "",
            "status": None,
            "severity": vuln.severity,
            "timestamp": vuln.created_at.isoformat(),
            "scan_id": vuln.scan_id,
            "link": f"/scan/{vuln.scan_id}",
        })
    reports = db.exec(
        select(Report)
        .where(Report.scan_id.in_(user_scans))
        .order_by(Report.generated_at.desc())
        .limit(limit // 4)
    ).all()
    for report in reports:
        activities.append({
            "type": "report",
            "action": "Report generated" if report.auto_generated else "Report created",
            "title": report.title or "Report",
            "description": f"{report.format.upper()} format",
            "status": "auto" if report.auto_generated else "manual",
            "severity": None,
            "timestamp": report.generated_at.isoformat(),
            "scan_id": report.scan_id,
            "link": "/reports",
        })
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return {"activities": activities[:limit], "total": len(activities)}


@router.get("/recent")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    recent_scans = db.exec(
        select(Scan).where(Scan.created_by == current_user.id).order_by(Scan.created_at.desc()).limit(limit)
    ).all()
    user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
    recent_vulns = db.exec(
        select(Vulnerability)
        .where(Vulnerability.scan_id.in_(user_scans))
        .order_by(Vulnerability.created_at.desc())
        .limit(limit)
    ).all()
    return {
        "recent_scans": [s.model_dump() for s in recent_scans],
        "recent_vulnerabilities": [v.model_dump() for v in recent_vulns],
    }


@router.get("/findings")
async def get_recent_findings(
    limit: int = 20,
    severity: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
    query = select(Vulnerability).where(Vulnerability.scan_id.in_(user_scans)).order_by(Vulnerability.created_at.desc())
    if severity:
        query = query.where(Vulnerability.severity == severity)
    vulnerabilities = db.exec(query.limit(limit)).all()
    return {"findings": [v.model_dump() for v in vulnerabilities], "total": len(vulnerabilities)}


@router.get("/vulnerability-types")
async def get_vulnerability_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user_scans = db.exec(select(Scan.id).where(Scan.created_by == current_user.id)).all()
    query = select(
        Vulnerability.vulnerability_type,
        func.count(Vulnerability.id).label("count"),
    ).where(Vulnerability.scan_id.in_(user_scans)).group_by(Vulnerability.vulnerability_type)
    rows = db.exec(query).all()
    return {"distribution": [{"type": row[0], "count": row[1]} for row in rows]}


@router.get("/scan-history")
async def get_scan_history(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    start_date = datetime.utcnow() - timedelta(days=days)
    all_scans = db.exec(
        select(Scan)
        .where(Scan.created_at >= start_date, Scan.created_by == current_user.id)
        .order_by(Scan.created_at)
    ).all()
    history = {}
    for scan in all_scans:
        date_str = scan.created_at.strftime("%Y-%m-%d")
        if date_str not in history:
            history[date_str] = {"date": date_str, "scans": 0, "vulnerabilities": 0, "critical": 0, "high": 0}
        history[date_str]["scans"] += 1
        history[date_str]["vulnerabilities"] += scan.total_vulnerabilities
        history[date_str]["critical"] += scan.critical_count
        history[date_str]["high"] += scan.high_count
    return {"history": list(history.values())}