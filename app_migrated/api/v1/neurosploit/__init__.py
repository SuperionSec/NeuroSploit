from fastapi import APIRouter

from app.api.v1.neurosploit import (
    scans,
    targets,
    vulnerabilities,
    agent,
    reports,
    dashboard,
    scheduler,
    vuln_lab,
    prompts,
    settings,
    agent_tasks,
)

neurosploit_router = APIRouter(prefix="/neurosploit")

neurosploit_router.include_router(scans.router, prefix="/scans", tags=["scans"])
neurosploit_router.include_router(targets.router, prefix="/targets", tags=["targets"])
neurosploit_router.include_router(vulnerabilities.router, prefix="/vulnerabilities", tags=["vulnerabilities"])
neurosploit_router.include_router(agent.router, prefix="/agent", tags=["agent"])
neurosploit_router.include_router(reports.router, prefix="/reports", tags=["reports"])
neurosploit_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
neurosploit_router.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])
neurosploit_router.include_router(vuln_lab.router, prefix="/vuln-lab", tags=["vuln-lab"])
neurosploit_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
neurosploit_router.include_router(settings.router, prefix="/settings", tags=["settings"])
neurosploit_router.include_router(agent_tasks.router, prefix="/agent-tasks", tags=["agent-tasks"])