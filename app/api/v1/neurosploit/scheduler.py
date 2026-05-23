from typing import List, Optional, Dict
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import ScheduledJob
from app.schemas.neurosploit import ScheduledJobCreate, ScheduledJobUpdate, ScheduledJobPublic

router = APIRouter()


@router.get("/", response_model=List[ScheduledJobPublic])
async def list_scheduled_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    jobs = db.exec(
        select(ScheduledJob)
        .where(ScheduledJob.created_by == current_user.id)
        .order_by(ScheduledJob.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()
    return [ScheduledJobPublic(**j.model_dump()) for j in jobs]


@router.post("/", response_model=ScheduledJobPublic, status_code=201)
async def create_scheduled_job(
    job: ScheduledJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not job.cron_expression and not job.interval_minutes:
        raise HTTPException(status_code=400, detail="Either cron_expression or interval_minutes must be provided")
    db_job = ScheduledJob(
        created_by=current_user.id,
        **job.model_dump(),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return ScheduledJobPublic(**db_job.model_dump())


@router.get("/{job_id}", response_model=ScheduledJobPublic)
async def get_scheduled_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    job = db.exec(
        select(ScheduledJob).where(ScheduledJob.id == job_id, ScheduledJob.created_by == current_user.id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    return ScheduledJobPublic(**job.model_dump())


@router.put("/{job_id}", response_model=ScheduledJobPublic)
async def update_scheduled_job(
    job_id: str,
    job_data: ScheduledJobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    job = db.exec(
        select(ScheduledJob).where(ScheduledJob.id == job_id, ScheduledJob.created_by == current_user.id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    for key, value in job_data.model_dump(exclude_unset=True).items():
        setattr(job, key, value)
    db.add(job)
    db.commit()
    db.refresh(job)
    return ScheduledJobPublic(**job.model_dump())


@router.delete("/{job_id}")
async def delete_scheduled_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    job = db.exec(
        select(ScheduledJob).where(ScheduledJob.id == job_id, ScheduledJob.created_by == current_user.id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    db.delete(job)
    db.commit()
    return {"message": "Scheduled job deleted", "id": job_id}


@router.post("/{job_id}/pause")
async def pause_scheduled_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    job = db.exec(
        select(ScheduledJob).where(ScheduledJob.id == job_id, ScheduledJob.created_by == current_user.id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    job.status = "paused"
    db.add(job)
    db.commit()
    return {"message": "Job paused", "id": job_id, "status": "paused"}


@router.post("/{job_id}/resume")
async def resume_scheduled_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    job = db.exec(
        select(ScheduledJob).where(ScheduledJob.id == job_id, ScheduledJob.created_by == current_user.id)
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scheduled job not found")
    job.status = "active"
    db.add(job)
    db.commit()
    return {"message": "Job resumed", "id": job_id, "status": "active"}