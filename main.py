"""
TechCrossIT — Mini Companies Platform
FastAPI entry point. Connect this to your Lovable.ai frontend via REST.

Usage:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=sk-ant-...
  uvicorn main:app --reload --port 8001

Lovable.ai frontend connects to: http://localhost:8001 (dev) or your deployed URL (prod)
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.marketplace_routes import router

# ── APP ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="TechCrossIT Marketplace API",
    description="AI Mini Company Platform — 5 specialist agent teams ready to execute work.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allow Lovable.ai frontend and localhost dev) ───────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",        # Local Lovable dev
        "http://localhost:5173",        # Vite dev server
        "https://techcrossit.co.uk",    # Production domain
        "https://*.lovable.app",        # Lovable.ai preview URLs
        "*",                            # Remove in production — set exact origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTES ───────────────────────────────────────────────────────────────────

app.include_router(router)


@app.get("/")
async def root():
    return {
        "platform": "TechCrossIT AI Marketplace",
        "version": "1.0.0",
        "companies": 5,
        "total_job_types": 40,
        "docs": "/docs",
        "marketplace": "/marketplace/companies",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


# ── DEV SERVER ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
