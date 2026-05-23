from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.vuln_lab import VulnLabChallenge


async def get_vuln_lab_challenge(db: AsyncSession, challenge_id: str, created_by: Optional[str] = None) -> Optional[VulnLabChallenge]:
    stmt = select(VulnLabChallenge).where(VulnLabChallenge.id == challenge_id)
    if created_by:
        stmt = stmt.where(VulnLabChallenge.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_vuln_lab_challenges(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    vuln_type: Optional[str] = None,
    vuln_category: Optional[str] = None,
    result: Optional[str] = None,
    agent_id: Optional[str] = None,
    scan_id: Optional[str] = None,
    created_by: Optional[str] = None,
) -> List[VulnLabChallenge]:
    stmt = select(VulnLabChallenge)
    if status:
        stmt = stmt.where(VulnLabChallenge.status == status)
    if vuln_type:
        stmt = stmt.where(VulnLabChallenge.vuln_type == vuln_type)
    if vuln_category:
        stmt = stmt.where(VulnLabChallenge.vuln_category == vuln_category)
    if result:
        stmt = stmt.where(VulnLabChallenge.result == result)
    if agent_id:
        stmt = stmt.where(VulnLabChallenge.agent_id == agent_id)
    if scan_id:
        stmt = stmt.where(VulnLabChallenge.scan_id == scan_id)
    if created_by:
        stmt = stmt.where(VulnLabChallenge.created_by == created_by)
    stmt = stmt.order_by(VulnLabChallenge.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_vuln_lab_challenge(db: AsyncSession, challenge: VulnLabChallenge) -> VulnLabChallenge:
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)
    return challenge


async def update_vuln_lab_challenge(db: AsyncSession, challenge_id: str, challenge_data: dict, created_by: Optional[str] = None) -> Optional[VulnLabChallenge]:
    existing = await get_vuln_lab_challenge(db, challenge_id, created_by)
    if not existing:
        return None
    for key, value in challenge_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_vuln_lab_challenge(db: AsyncSession, challenge_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_vuln_lab_challenge(db, challenge_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
