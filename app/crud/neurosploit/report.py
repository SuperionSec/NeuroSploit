from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.report import Report


async def get_report(db: AsyncSession, report_id: str, created_by: Optional[str] = None) -> Optional[Report]:
    stmt = select(Report).where(Report.id == report_id)
    if created_by:
        stmt = stmt.where(Report.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_reports(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    scan_id: Optional[str] = None,
    format: Optional[str] = None,
    auto_generated: Optional[bool] = None,
    created_by: Optional[str] = None,
) -> List[Report]:
    stmt = select(Report)
    if scan_id:
        stmt = stmt.where(Report.scan_id == scan_id)
    if format:
        stmt = stmt.where(Report.format == format)
    if auto_generated is not None:
        stmt = stmt.where(Report.auto_generated == auto_generated)
    if created_by:
        stmt = stmt.where(Report.created_by == created_by)
    stmt = stmt.order_by(Report.generated_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_reports_by_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> List[Report]:
    stmt = select(Report).where(Report.scan_id == scan_id)
    if created_by:
        stmt = stmt.where(Report.created_by == created_by)
    stmt = stmt.order_by(Report.generated_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_report(db: AsyncSession, report: Report) -> Report:
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def update_report(db: AsyncSession, report_id: str, report_data: dict, created_by: Optional[str] = None) -> Optional[Report]:
    existing = await get_report(db, report_id, created_by)
    if not existing:
        return None
    for key, value in report_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_report(db: AsyncSession, report_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_report(db, report_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
