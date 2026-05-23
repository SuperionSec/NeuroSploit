from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.target import Target


async def get_target(db: AsyncSession, target_id: str, created_by: Optional[str] = None) -> Optional[Target]:
    stmt = select(Target).where(Target.id == target_id)
    if created_by:
        stmt = stmt.where(Target.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_targets(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    scan_id: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[str] = None,
) -> List[Target]:
    stmt = select(Target)
    if scan_id:
        stmt = stmt.where(Target.scan_id == scan_id)
    if status:
        stmt = stmt.where(Target.status == status)
    if created_by:
        stmt = stmt.where(Target.created_by == created_by)
    stmt = stmt.order_by(Target.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_targets_by_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> List[Target]:
    stmt = select(Target).where(Target.scan_id == scan_id)
    if created_by:
        stmt = stmt.where(Target.created_by == created_by)
    stmt = stmt.order_by(Target.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_target(db: AsyncSession, target: Target) -> Target:
    db.add(target)
    await db.commit()
    await db.refresh(target)
    return target


async def update_target(db: AsyncSession, target_id: str, target_data: dict, created_by: Optional[str] = None) -> Optional[Target]:
    existing = await get_target(db, target_id, created_by)
    if not existing:
        return None
    for key, value in target_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_target(db: AsyncSession, target_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_target(db, target_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
