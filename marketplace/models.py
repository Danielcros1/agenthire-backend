"""
TechCrossIT Marketplace — Shared Models
Job intake forms, output schemas, and company metadata.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


# ── ENUMS ───────────────────────────────────────────────────────────────────

class CompanyID(str, Enum):
    DEV_SHOP          = "dev_shop"
    MARKETING_AGENCY  = "marketing_agency"
    SALES_TEAM        = "sales_team"
    FINANCE_OFFICE    = "finance_office"
    SUPPORT_DESK      = "support_desk"


class JobStatus(str, Enum):
    QUEUED      = "queued"
    RUNNING     = "running"
    DONE        = "done"
    FAILED      = "failed"


# ── JOB INTAKE (universal) ──────────────────────────────────────────────────

class JobIntake(BaseModel):
    """Universal job submission model — used by every mini company."""
    company_id:   CompanyID           = Field(..., description="Which mini company to hire")
    job_type:     str                  = Field(..., description="Specific job template key")
    brief:        str                  = Field(..., description="Plain-English description of the work")
    context:      Optional[str]        = Field(None, description="Background info, existing files, URLs etc.")
    client_name:  Optional[str]        = Field(None, description="Client / requester name")
    tone:         Optional[str]        = Field("professional", description="Tone: formal | casual | technical | friendly")
    output_format: Optional[str]       = Field("text", description="Output format: text | markdown | json | html")
    priority:     Optional[str]        = Field("normal", description="normal | urgent | scheduled")
    extra:        Optional[Dict[str, Any]] = Field(default_factory=dict, description="Company-specific extra fields")

    class Config:
        use_enum_values = True


# ── JOB RESULT ──────────────────────────────────────────────────────────────

class JobResult(BaseModel):
    """Standardised result returned by every mini company agent."""
    job_id:       str
    company_id:   str
    job_type:     str
    status:       JobStatus
    output:       Optional[str]  = None      # Main deliverable (text/markdown/json)
    metadata:     Dict[str, Any] = Field(default_factory=dict)
    error:        Optional[str]  = None
    duration_ms:  Optional[int]  = None
    tokens_used:  Optional[int]  = None


# ── COMPANY CARD (for marketplace listing) ──────────────────────────────────

class CompanyCard(BaseModel):
    """Display card shown in the Lovable frontend marketplace grid."""
    id:           str
    name:         str
    tagline:      str
    description:  str
    phase:        int                   # 1 = live, 2 = coming soon, 3 = premium
    jobs:         List[Dict[str, str]]  # [{"key": "write_blog", "label": "Write Blog Post", "time": "~45s"}]
    icon:         str                   # emoji or URL
    colour:       str                   # hex accent colour
    price_from:   str                   # "£0.50 / job" or "Subscription"
