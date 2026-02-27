"""
TechCrossIT Marketplace — FastAPI Routes
All endpoints consumed by the Lovable.ai frontend.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import asyncio
import uuid
from typing import Optional

from marketplace.models import JobIntake, JobResult, JobStatus, CompanyID
from marketplace.registry import get_all_cards, get_card, get_job_types

# ── Company agents ──────────────────────────────────────────────────────────
from companies.dev_shop.agent        import run as run_dev_shop
from companies.marketing_agency.agent import run as run_marketing
from companies.sales_team.agent      import run as run_sales
from companies.finance_office.agent  import run as run_finance
from companies.support_desk.agent    import run as run_support

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

# ── Dispatcher map ────────────────────────────────────────────────────────
RUNNERS = {
    "dev_shop":          run_dev_shop,
    "marketing_agency":  run_marketing,
    "sales_team":        run_sales,
    "finance_office":    run_finance,
    "support_desk":      run_support,
}


# ── MARKETPLACE LISTING ─────────────────────────────────────────────────────

@router.get("/companies")
async def list_companies():
    """Return all available mini companies for the marketplace grid."""
    return {"companies": [c.dict() for c in get_all_cards()]}


@router.get("/companies/{company_id}")
async def get_company(company_id: str):
    """Return a single company card."""
    try:
        return get_card(company_id).dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/companies/{company_id}/jobs")
async def list_jobs(company_id: str):
    """Return all available job types for a company."""
    try:
        card = get_card(company_id)
        return {"company_id": company_id, "jobs": card.jobs}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── JOB SUBMISSION ───────────────────────────────────────────────────────────

@router.post("/submit", response_model=JobResult)
async def submit_job(intake: JobIntake):
    """
    Submit a job to a mini company. Returns the result synchronously.
    For production, consider switching to async queue (Celery / Redis).
    """
    runner = RUNNERS.get(intake.company_id)
    if not runner:
        raise HTTPException(status_code=404, detail=f"Company '{intake.company_id}' not found.")

    # Validate job type
    valid_jobs = get_job_types(intake.company_id)
    if intake.job_type not in valid_jobs:
        raise HTTPException(
            status_code=422,
            detail=f"Job type '{intake.job_type}' not available for '{intake.company_id}'. "
                   f"Valid types: {valid_jobs}",
        )

    # Run agent (blocking — wrap in executor for production async)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, runner, intake)

    if result.status == JobStatus.FAILED:
        raise HTTPException(status_code=500, detail=result.error)

    return result


# ── QUICK DEMO ENDPOINT (no API key needed — for testing) ────────────────────

@router.get("/demo/{company_id}/{job_type}")
async def demo_job(company_id: str, job_type: str, brief: Optional[str] = None):
    """
    Demo endpoint that shows the job prompt template without calling the AI.
    Useful for testing the Lovable frontend connection before spending credits.
    """
    try:
        card = get_card(company_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    valid_jobs = get_job_types(company_id)
    if job_type not in valid_jobs:
        raise HTTPException(status_code=422, detail=f"Unknown job_type: {job_type}")

    job_label = next((j["label"] for j in card.jobs if j["key"] == job_type), job_type)

    return {
        "company": card.name,
        "job_type": job_type,
        "job_label": job_label,
        "brief_received": brief or "(none provided)",
        "estimated_time": next((j["time"] for j in card.jobs if j["key"] == job_type), "~60s"),
        "status": "demo — no AI call made",
        "message": f"POST /marketplace/submit with company_id='{company_id}' and job_type='{job_type}' to run this job.",
    }


# ── HEALTH ───────────────────────────────────────────────────────────────────

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "companies": list(RUNNERS.keys()),
        "total_job_types": sum(len(get_job_types(c)) for c in RUNNERS),
    }
