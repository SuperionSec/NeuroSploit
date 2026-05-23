from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.prompt import Prompt


async def get_prompt(db: AsyncSession, prompt_id: str, created_by: Optional[str] = None) -> Optional[Prompt]:
    stmt = select(Prompt).where(Prompt.id == prompt_id)
    if created_by:
        stmt = stmt.where(Prompt.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_prompts(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    is_preset: Optional[bool] = None,
    category: Optional[str] = None,
    created_by: Optional[str] = None,
) -> List[Prompt]:
    stmt = select(Prompt)
    if is_preset is not None:
        stmt = stmt.where(Prompt.is_preset == is_preset)
    if category:
        stmt = stmt.where(Prompt.category == category)
    if created_by:
        stmt = stmt.where(Prompt.created_by == created_by)
    stmt = stmt.order_by(Prompt.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_prompt(db: AsyncSession, prompt: Prompt) -> Prompt:
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    return prompt


async def update_prompt(db: AsyncSession, prompt_id: str, prompt_data: dict, created_by: Optional[str] = None) -> Optional[Prompt]:
    existing = await get_prompt(db, prompt_id, created_by)
    if not existing:
        return None
    for key, value in prompt_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_prompt(db: AsyncSession, prompt_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_prompt(db, prompt_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
