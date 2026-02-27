# TechCrossIT — AI Mini Companies Platform

5 specialist AI agent companies, each a plug-and-play team you can hire for any task.

---

## Phase 1 Companies (Live Now)

| # | Company | Jobs | Price |
|---|---------|------|-------|
| 1 | 💻 **The Dev Shop** | Build APIs, fix bugs, write tests, review code, docs | £0.80/job |
| 2 | 📣 **The Marketing Agency** | Blog posts, social packs, email campaigns, SEO, ad copy | £0.60/job |
| 3 | 🎯 **The Sales Team** | Prospect research, cold email, proposals, pitch decks | £0.70/job |
| 4 | 💰 **The Finance Office** | Invoices, expense reports, P&L, cash flow, VAT | £0.50/job |
| 5 | 🎧 **The Support Desk** | Ticket triage, responses, FAQs, knowledge base | £0.40/job |

Each company has **8 job templates** = **40 total jobs** in Phase 1.

---

## Quick Start

```bash
# 1. Clone / copy this folder to your server
cd techcrossit-mini-companies

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 4. Start the server
uvicorn main:app --reload --port 8001

# 5. Open the API docs
open http://localhost:8001/docs
```

---

## Key API Endpoints

### List all companies (for marketplace grid)
```
GET /marketplace/companies
```

### Get jobs for a company
```
GET /marketplace/companies/dev_shop/jobs
```

### Submit a job
```
POST /marketplace/submit
Content-Type: application/json

{
  "company_id": "dev_shop",
  "job_type": "build_api_endpoint",
  "brief": "Build a POST /api/checkout endpoint with Stripe integration...",
  "context": "FastAPI app, Python 3.11, already have stripe installed",
  "client_name": "Acme Corp",
  "tone": "technical",
  "output_format": "markdown"
}
```

### Demo endpoint (no API key needed for testing)
```
GET /marketplace/demo/dev_shop/build_api_endpoint?brief=Test+brief
```

### Health check
```
GET /marketplace/health
```

---

## Connecting to Lovable.ai Frontend

Your techcrossit.co.uk site was built with Lovable.ai (React/Vite). To connect it to this backend:

### Step 1 — Deploy this backend
Deploy to Railway, Render, or AWS. You'll get a URL like:
```
https://techcrossit-api.railway.app
```

### Step 2 — In your Lovable project, add a `.env` file
```
VITE_API_BASE_URL=https://techcrossit-api.railway.app
```

### Step 3 — Add this API client to your Lovable project
Create `src/lib/marketplace.ts`:

```typescript
const BASE = import.meta.env.VITE_API_BASE_URL;

export async function getCompanies() {
  const res = await fetch(`${BASE}/marketplace/companies`);
  return res.json();
}

export async function submitJob(intake: {
  company_id: string;
  job_type: string;
  brief: string;
  context?: string;
  client_name?: string;
  tone?: string;
}) {
  const res = await fetch(`${BASE}/marketplace/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(intake),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
```

### Step 4 — Use it in your Lovable component
```typescript
import { getCompanies, submitJob } from "@/lib/marketplace";

// Load marketplace grid
const { companies } = await getCompanies();

// Submit a job when user clicks "Hire"
const result = await submitJob({
  company_id: "dev_shop",
  job_type: "fix_bug",
  brief: userInputBrief,
  client_name: user.name,
});

// Display result.output in a modal/card
```

---

## Project Structure

```
techcrossit-mini-companies/
├── main.py                         # FastAPI entry point
├── requirements.txt
├── .env.example
├── demo.py                         # Live test script
│
├── marketplace/
│   ├── models.py                   # JobIntake, JobResult, CompanyCard
│   ├── registry.py                 # All company listings
│   └── __init__.py
│
├── companies/
│   ├── dev_shop/agent.py           # 8 dev jobs
│   ├── marketing_agency/agent.py   # 8 marketing jobs
│   ├── sales_team/agent.py         # 8 sales jobs
│   ├── finance_office/agent.py     # 8 finance jobs
│   └── support_desk/agent.py       # 8 support jobs
│
└── api/
    └── marketplace_routes.py       # All REST endpoints
```

---

## Running the Demo

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Test all 5 companies
python demo.py

# Test one company
python demo.py dev_shop
python demo.py marketing_agency
python demo.py sales_team
python demo.py finance_office
python demo.py support_desk
```

---

## Phase 2 & 3 Roadmap

**Phase 2 (coming soon):**
- 🏗️ The Design Studio (logos, brand kits, social graphics)
- 🔍 The Research Lab (market research, competitor intel, data analysis)
- ⚖️ The Legal Desk (contract review, NDA drafting, GDPR checks)
- 🤝 The HR Office (job descriptions, onboarding, policies)
- 📊 The Data Team (dashboards, reports, analytics)

**Phase 3 (premium):**
- 🏢 The Consulting Firm
- 🎓 The Training Academy
- 🌍 The Translation Bureau
- 🔐 The Security Audit Team
- 🚀 The Product Team

---

## Built with
- **Anthropic Claude** (`claude-sonnet-4-6`) — AI backbone
- **FastAPI** — REST API framework
- **Pydantic v2** — Data validation
- **Lovable.ai** — Frontend (techcrossit.co.uk)
- **Supabase** — Auth, job history, user credits (add-on)
- **Stripe** — Payments (add-on)
