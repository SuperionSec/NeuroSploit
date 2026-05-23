from typing import List
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select, func

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Target
from app.schemas.neurosploit import (
    TargetCreate,
    TargetUpdate,
    TargetPublic,
    TargetBulkCreate,
    TargetValidation,
)

router = APIRouter()


def validate_url(url: str) -> TargetValidation:
    url = url.strip()
    if not url:
        return TargetValidation(url=url, valid=False, error="URL is empty")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    try:
        parsed = urlparse(url)
        return TargetValidation(
            url=url,
            valid=True,
            normalized_url=url,
            hostname=parsed.hostname,
            port=parsed.port or (443 if parsed.scheme == "https" else 80),
            protocol=parsed.scheme,
        )
    except Exception as e:
        return TargetValidation(url=url, valid=False, error=str(e))


@router.get("/", response_model=List[TargetPublic])
async def list_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    targets = db.exec(
        select(Target)
        .join(Target.scan)  # Scan has created_by
        .where(Scan.created_by == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    return [TargetPublic(**t.model_dump()) for t in targets]


@router.post("/", response_model=TargetPublic, status_code=201)
async def create_target(
    target_data: TargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    target = Target(**target_data.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return TargetPublic(**target.model_dump())


@router.put("/{target_id}", response_model=TargetPublic)
async def update_target(
    target_id: str,
    target_data: TargetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    target = db.exec(select(Target).where(Target.id == target_id)).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    for key, value in target_data.model_dump(exclude_unset=True).items():
        setattr(target, key, value)
    db.add(target)
    db.commit()
    db.refresh(target)
    return TargetPublic(**target.model_dump())


@router.delete("/{target_id}")
async def delete_target(
    target_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    target = db.exec(select(Target).where(Target.id == target_id)).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    db.delete(target)
    db.commit()
    return {"message": "Target deleted", "target_id": target_id}


@router.post("/validate", response_model=TargetValidation)
async def validate_target(
    target: TargetCreate,
    current_user: User = Depends(get_current_active_user),
):
    return validate_url(target.url)


@router.post("/validate/bulk", response_model=List[TargetValidation])
async def validate_targets_bulk(
    targets: TargetBulkCreate,
    current_user: User = Depends(get_current_active_user),
):
    return [validate_url(url) for url in targets.urls]


@router.post("/upload", response_model=List[TargetValidation])
async def upload_targets(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    allowed = {".txt", ".csv", ".lst"}
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(allowed)}")
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = content.decode("latin-1")
        except Exception:
            raise HTTPException(status_code=400, detail="Unable to decode file")
    urls = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," in line and "://" in line:
            urls.extend(u.strip() for u in line.split(",") if u.strip())
        else:
            urls.append(line)
    if not urls:
        raise HTTPException(status_code=400, detail="No URLs found in file")
    return [validate_url(u) for u in urls]