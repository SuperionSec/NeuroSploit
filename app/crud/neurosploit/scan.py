from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.models.scan import Scan
from backend.models.target import Target
from backend.models.endpoint import Endpoint
from backend.models.vulnerability import Vulnerability


async def get_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> Optional[Scan]:
    stmt = select(Scan).where(Scan.id == scan_id)
    if created_by:
        stmt = stmt.where(Scan.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_scans(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    scan_type: Optional[str] = None,
    created_by: Optional[str] = None,
) -> List[Scan]:
    stmt = select(Scan)
    if status:
        stmt = stmt.where(Scan.status == status)
    if scan_type:
        stmt = stmt.where(Scan.scan_type == scan_type)
    if created_by:
        stmt = stmt.where(Scan.created_by == created_by)
    stmt = stmt.order_by(Scan.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_scans_by_user(db: AsyncSession, created_by: str, skip: int = 0, limit: int = 100) -> List[Scan]:
    stmt = select(Scan).where(Scan.created_by == created_by)
    stmt = stmt.order_by(Scan.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_scan(db: AsyncSession, scan: Scan) -> Scan:
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    return scan


async def update_scan(db: AsyncSession, scan_id: str, scan_data: dict, created_by: Optional[str] = None) -> Optional[Scan]:
    existing = await get_scan(db, scan_id, created_by)
    if not existing:
        return None
    for key, value in scan_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_scan(db, scan_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True


async def update_scan_progress(
    db: AsyncSession,
    scan_id: str,
    progress: int,
    current_phase: Optional[str] = None,
    created_by: Optional[str] = None,
) -> Optional[Scan]:
    existing = await get_scan(db, scan_id, created_by)
    if not existing:
        return None
    existing.progress = progress
    if current_phase is not None:
        existing.current_phase = current_phase
    await db.commit()
    await db.refresh(existing)
    return existing


async def update_scan_stats(
    db: AsyncSession,
    scan_id: str,
    total_endpoints: Optional[int] = None,
    total_vulnerabilities: Optional[int] = None,
    critical_count: Optional[int] = None,
    high_count: Optional[int] = None,
    medium_count: Optional[int] = None,
    low_count: Optional[int] = None,
    info_count: Optional[int] = None,
    created_by: Optional[str] = None,
) -> Optional[Scan]:
    existing = await get_scan(db, scan_id, created_by)
    if not existing:
        return None
    if total_endpoints is not None:
        existing.total_endpoints = total_endpoints
    if total_vulnerabilities is not None:
        existing.total_vulnerabilities = total_vulnerabilities
    if critical_count is not None:
        existing.critical_count = critical_count
    if high_count is not None:
        existing.high_count = high_count
    if medium_count is not None:
        existing.medium_count = medium_count
    if low_count is not None:
        existing.low_count = low_count
    if info_count is not None:
        existing.info_count = info_count
    await db.commit()
    await db.refresh(existing)
    return existing


async def get_scan_with_stats(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> Optional[dict]:
    scan = await get_scan(db, scan_id, created_by)
    if not scan:
        return None

    endpoints_count_stmt = select(func.count()).select_from(Endpoint).where(Endpoint.scan_id == scan_id)
    vulnerabilities_count_stmt = select(func.count()).select_from(Vulnerability).where(Vulnerability.scan_id == scan_id)

    endpoints_count = (await db.execute(endpoints_count_stmt)).scalar()
    vulnerabilities_count = (await db.execute(vulnerabilities_count_stmt)).scalar()

    return {
        **scan.to_dict(),
        "total_endpoints_actual": endpoints_count,
        "total_vulnerabilities_actual": vulnerabilities_count,
    }
