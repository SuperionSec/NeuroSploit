from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import AgentTask, Scan
from app.schemas.neurosploit import (
    AgentTaskPublic,
    AgentTaskListResponse,
    AgentTaskSummary,
)

router = APIRouter()


@router.get("/", response_model=AgentTaskListResponse)
async def list_agent_tasks(
    scan_id: str,
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(
        select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)
    ).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    query = select(AgentTask).where(AgentTask.scan_id == scan_id).order_by(AgentTask.created_at.desc())
    if status:
        query = query.where(AgentTask.status == status)
    if task_type:
        query = query.where(AgentTask.task_type == task_type)
    total = db.exec(
        select(func.count()).select_from(AgentTask).where(AgentTask.scan_id == scan_id)
    ).one() or 0
    tasks = db.exec(query.offset(skip).limit(limit)).all()
    return AgentTaskListResponse(
        tasks=[AgentTaskPublic(**t.model_dump()) for t in tasks],
        total=total,
        scan_id=scan_id,
    )


@router.get("/summary", response_model=AgentTaskSummary)
async def get_agent_tasks_summary(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(
        select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)
    ).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    total = db.exec(
        select(func.count()).select_from(AgentTask).where(AgentTask.scan_id == scan_id)
    ).one() or 0
    status_counts = {}
    for s in ["pending", "running", "completed", "failed"]:
        status_counts[s] = db.exec(
            select(func.count()).select_from(AgentTask)
            .where(AgentTask.scan_id == scan_id, AgentTask.status == s)
        ).one() or 0
    type_rows = db.exec(
        select(AgentTask.task_type, func.count(AgentTask.id))
        .where(AgentTask.scan_id == scan_id)
        .group_by(AgentTask.task_type)
    ).all()
    by_type = {row[0]: row[1] for row in type_rows}
    tool_rows = db.exec(
        select(AgentTask.tool_name, func.count(AgentTask.id))
        .where(AgentTask.scan_id == scan_id, AgentTask.tool_name != None)
        .group_by(AgentTask.tool_name)
    ).all()
    by_tool = {row[0]: row[1] for row in tool_rows}
    return AgentTaskSummary(
        total=total,
        pending=status_counts.get("pending", 0),
        running=status_counts.get("running", 0),
        completed=status_counts.get("completed", 0),
        failed=status_counts.get("failed", 0),
        by_type=by_type,
        by_tool=by_tool,
    )


@router.get("/{task_id}", response_model=AgentTaskPublic)
async def get_agent_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    task = db.exec(select(AgentTask).where(AgentTask.id == task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Agent task not found")
    scan = db.exec(
        select(Scan).where(Scan.id == task.scan_id, Scan.created_by == current_user.id)
    ).first()
    if not scan:
        raise HTTPException(status_code=403, detail="Access denied")
    return AgentTaskPublic(**task.model_dump())


@router.get("/scan/{scan_id}/timeline")
async def get_agent_tasks_timeline(
    scan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    scan = db.exec(
        select(Scan).where(Scan.id == scan_id, Scan.created_by == current_user.id)
    ).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    tasks = db.exec(
        select(AgentTask).where(AgentTask.scan_id == scan_id).order_by(AgentTask.created_at.asc())
    ).all()
    timeline = []
    for task in tasks:
        timeline.append({
            "id": task.id,
            "task_name": task.task_name,
            "task_type": task.task_type,
            "tool_name": task.tool_name,
            "status": task.status,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "duration_ms": task.duration_ms,
            "items_processed": task.items_processed,
            "items_found": task.items_found,
            "result_summary": task.result_summary,
            "error_message": task.error_message,
        })
    return {"scan_id": scan_id, "timeline": timeline, "total": len(timeline)}