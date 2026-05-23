from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.agent_task import AgentTask


async def get_agent_task(db: AsyncSession, task_id: str, created_by: Optional[str] = None) -> Optional[AgentTask]:
    stmt = select(AgentTask).where(AgentTask.id == task_id)
    if created_by:
        stmt = stmt.where(AgentTask.created_by == created_by)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_agent_tasks(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    scan_id: Optional[str] = None,
    task_type: Optional[str] = None,
    status: Optional[str] = None,
    tool_name: Optional[str] = None,
    created_by: Optional[str] = None,
) -> List[AgentTask]:
    stmt = select(AgentTask)
    if scan_id:
        stmt = stmt.where(AgentTask.scan_id == scan_id)
    if task_type:
        stmt = stmt.where(AgentTask.task_type == task_type)
    if status:
        stmt = stmt.where(AgentTask.status == status)
    if tool_name:
        stmt = stmt.where(AgentTask.tool_name == tool_name)
    if created_by:
        stmt = stmt.where(AgentTask.created_by == created_by)
    stmt = stmt.order_by(AgentTask.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_agent_tasks_by_scan(db: AsyncSession, scan_id: str, created_by: Optional[str] = None) -> List[AgentTask]:
    stmt = select(AgentTask).where(AgentTask.scan_id == scan_id)
    if created_by:
        stmt = stmt.where(AgentTask.created_by == created_by)
    stmt = stmt.order_by(AgentTask.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_agent_task(db: AsyncSession, agent_task: AgentTask) -> AgentTask:
    db.add(agent_task)
    await db.commit()
    await db.refresh(agent_task)
    return agent_task


async def update_agent_task(db: AsyncSession, task_id: str, agent_task_data: dict, created_by: Optional[str] = None) -> Optional[AgentTask]:
    existing = await get_agent_task(db, task_id, created_by)
    if not existing:
        return None
    for key, value in agent_task_data.items():
        if hasattr(existing, key):
            setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_agent_task(db: AsyncSession, task_id: str, created_by: Optional[str] = None) -> bool:
    existing = await get_agent_task(db, task_id, created_by)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
