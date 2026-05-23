from typing import Optional, Dict, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.models.neurosploit import Scan, Target
from app.schemas.neurosploit import AgentRunRequest, AgentResponse, AgentStatusResponse

router = APIRouter()

agent_results: Dict[str, Dict] = {}
agent_instances: Dict[str, object] = {}
agent_tasks: Dict[str, object] = {}
agent_to_scan: Dict[str, str] = {}
scan_to_agent: Dict[str, str] = {}


@router.get("/status")
async def get_llm_status(
    current_user: User = Depends(get_current_active_user),
):
    import os

    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if anthropic_key in ("", "your-anthropic-api-key"):
        anthropic_key = None
    if openai_key in ("", "your-openai-api-key"):
        openai_key = None

    provider = None
    if anthropic_key:
        status = "ready"
        provider = "claude"
        message = "Claude API configured and ready"
    elif openai_key:
        status = "ready"
        provider = "openai"
        message = "OpenAI API configured and ready"
    else:
        status = "not_configured"
        message = "No API key configured"

    return {
        "status": status,
        "provider": provider,
        "message": message,
        "details": {
            "anthropic_key_set": bool(anthropic_key),
            "openai_key_set": bool(openai_key),
        },
    }


@router.post("/run", response_model=AgentResponse)
async def run_agent(
    request: AgentRunRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
):
    import uuid

    agent_id = str(uuid.uuid4())[:8]
    agent_results[agent_id] = {
        "status": "running",
        "mode": request.mode,
        "started_at": datetime.utcnow().isoformat(),
        "target": request.target,
        "logs": [],
        "findings": [],
        "report": None,
        "progress": 0,
        "phase": "initializing",
    }

    return AgentResponse(
        agent_id=agent_id,
        status="running",
        mode=request.mode,
        message=f"Agent deployed on {request.target}",
    )


@router.post("/stop/{agent_id}")
async def stop_agent(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent_results[agent_id]["status"] != "running":
        return {"message": "Agent is not running", "status": agent_results[agent_id]["status"]}
    if agent_id in agent_instances:
        agent_instances[agent_id].cancel()
    agent_results[agent_id]["status"] = "stopped"
    agent_results[agent_id]["phase"] = "stopped"
    agent_results[agent_id]["completed_at"] = datetime.utcnow().isoformat()
    return {"message": "Agent stopped", "agent_id": agent_id}


@router.post("/pause/{agent_id}")
async def pause_agent(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent_results[agent_id]["status"] != "running":
        return {"message": "Agent is not running", "status": agent_results[agent_id]["status"]}
    if agent_id in agent_instances:
        agent_instances[agent_id].pause()
    agent_results[agent_id]["last_phase"] = agent_results[agent_id].get("phase", "recon")
    agent_results[agent_id]["status"] = "paused"
    agent_results[agent_id]["phase"] = "paused"
    return {"message": "Agent paused", "agent_id": agent_id}


@router.post("/resume/{agent_id}")
async def resume_agent(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent_results[agent_id]["status"] != "paused":
        return {"message": "Agent is not paused", "status": agent_results[agent_id]["status"]}
    if agent_id in agent_instances:
        agent_instances[agent_id].resume()
    agent_results[agent_id]["status"] = "running"
    agent_results[agent_id]["phase"] = agent_results[agent_id].get("last_phase", "testing")
    return {"message": "Agent resumed", "agent_id": agent_id}


@router.get("/status/{agent_id}", response_model=AgentStatusResponse)
async def get_agent_status(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = agent_results[agent_id]
    return AgentStatusResponse(
        agent_id=agent_id,
        status=result["status"],
        mode=result.get("mode", "full_auto"),
        target=result["target"],
        progress=result.get("progress", 0),
        phase=result.get("phase", "unknown"),
        findings_count=len(result.get("findings", [])),
        started_at=result.get("started_at"),
    )


@router.get("/active")
async def list_active_agents(
    current_user: User = Depends(get_current_active_user),
):
    active = []
    for aid, data in agent_results.items():
        if data.get("status") in ("running", "paused"):
            active.append({
                "agent_id": aid,
                "target": data.get("target", ""),
                "status": data["status"],
                "progress": data.get("progress", 0),
                "phase": data.get("phase", ""),
                "scan_id": agent_to_scan.get(aid),
                "started_at": data.get("started_at", ""),
                "findings_count": len(data.get("findings", [])),
            })
    return {"agents": active, "running_count": sum(1 for a in active if a["status"] == "running")}


@router.get("/logs/{agent_id}")
async def get_agent_logs(
    agent_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    logs = agent_results[agent_id].get("logs", [])
    return {"agent_id": agent_id, "total_logs": len(logs), "logs": logs[-limit:]}


@router.get("/findings/{agent_id}")
async def get_agent_findings(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id not in agent_results:
        raise HTTPException(status_code=404, detail="Agent not found")
    findings = agent_results[agent_id].get("findings", [])
    return {"agent_id": agent_id, "total_findings": len(findings), "findings": findings}


@router.delete("/{agent_id}")
async def delete_agent_result(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
):
    if agent_id in agent_results:
        del agent_results[agent_id]
        return {"message": f"Agent {agent_id} results deleted"}
    raise HTTPException(status_code=404, detail="Agent not found")