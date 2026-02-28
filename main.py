"""
TechCrossIT – AgentHire Marketplace Backend
FastAPI entry point.

Usage:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=sk-ant-...
  python main.py
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.marketplace_routes import router

app = FastAPI(
    title="AgentHire Marketplace API",
    description="AI Agent Marketplace – 10 specialist agent companies.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:4173",
        "https://danielcros1.github.io",
        "https://techcrossit.co.uk",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "platform": "AgentHire Marketplace API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "marketplace": "/marketplace/health",
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
