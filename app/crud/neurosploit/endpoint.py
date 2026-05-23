from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.endpoint import Endpoint


async def get_endpoint(db: AsyncSession, endpoint_id: str, created_by: Optional[str] = None) -> Optional[Endpoint]:
    stmt = select(Endpoint).where(Endpoint.id == endpoint_id)
    if created_by:
        stmt = stmt.where(Endpoint.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_endpoints(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    scan_id: Optional[str] = None,
    target_id: Optional[str] = None,
    interesting: Optional[bool] = None,
    created_by: Optional[str] = None,
) -> List[Endpoint]:
    stmt = select(Endpoint)
    if scan_id:
        stmt = stmt.where(Endpoint.scan_id == scan_id)
    if target_id:
        stmt = stmt.where(Endpoint.target_id == target_id)
    if interesting is not None:
        stmt = stmt.where(Endpoint.interesting == interesting)
    if created_by:
        stmt = stmt.where(Endpoint.created_by == created_by)
    stmt = stmt.order_by(Endpoint.discovered_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_endpoints_by_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> List[Endpoint]:
    stmt = select(Endpoint).where(Endpoint.scan_id == scan_id)
    if created_by:
        stmt = stmt.where(Endpoint.created_by == created_by)
    stmt = stmt.order_by(Endpoint.discovered_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_endpoint(db: AsyncSession, endpoint: Endpoint) -> Endpoint:
    db.add(endpoint)
    await db.commit()
    await db.refresh(endpoint)
    return endpoint


async def update_endpoint(db: AsyncSession, endpoint_id: str, endpoint_data: dict, created_by: Optional[str] = None) -> Optional[Endpoint]:
    existing = await get_endpoint(db, endpoint_id, created_by)
    if not existing:
        return None
    for key, value in endpoint_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_endpoint(db: AsyncSession, endpoint_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_endpoint(db, endpoint_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
