"""
TechCrossIT Mini Companies — Live Demo Script
Tests one job from each of the 5 Phase 1 companies using real Claude API calls.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python demo.py

Or test a single company:
  python demo.py dev_shop
"""

import os
import sys
import time

# Set up path
sys.path.insert(0, os.path.dirname(__file__))

from marketplace.models import JobIntake, CompanyID
from companies.dev_shop.agent        import run as dev_run
from companies.marketing_agency.agent import run as mkt_run
from companies.sales_team.agent      import run as sales_run
from companies.finance_office.agent  import run as finance_run
from companies.support_desk.agent    import run as support_run


# ── DEMO JOBS ────────────────────────────────────────────────────────────────

DEMOS = {
    "dev_shop": {
        "runner": dev_run,
        "intake": JobIntake(
            company_id="dev_shop",
            job_type="build_api_endpoint",
            brief="Build a POST /api/subscribe endpoint that accepts email and plan_id, "
                  "validates the email format, checks the plan_id is in ['starter','pro','enterprise'], "
                  "and returns a JSON confirmation. Use FastAPI with Pydantic.",
            client_name="TechCrossIT Demo",
            tone="technical",
        ),
    },
    "marketing_agency": {
        "runner": mkt_run,
        "intake": JobIntake(
            company_id="marketing_agency",
            job_type="write_blog_post",
            brief="How AI Agent Mini Companies Are Replacing Freelancer Platforms in 2026",
            context="Target audience: SME owners and entrepreneurs. "
                    "Company: TechCrossIT — an AI agent marketplace platform based in the UK.",
            client_name="TechCrossIT Demo",
            tone="professional",
        ),
    },
    "sales_team": {
        "runner": sales_run,
        "intake": JobIntake(
            company_id="sales_team",
            job_type="cold_outreach_email",
            brief="Prospect: Sarah Bennett, Head of Operations at Bloom & Wild (UK flower subscription). "
                  "We are TechCrossIT, offering AI agents that automate customer support, content, and invoicing. "
                  "Goal: book a 20-min demo call.",
            client_name="TechCrossIT Demo",
            tone="professional",
        ),
    },
    "finance_office": {
        "runner": finance_run,
        "intake": JobIntake(
            company_id="finance_office",
            job_type="generate_invoice",
            brief="Invoice from TechCrossIT Ltd to Acme Digital Agency Ltd. "
                  "Services: AI Agent Platform setup (£8,000) + 3 months Pro subscription (£299/month). "
                  "Invoice date: today. Payment terms: 30 days.",
            client_name="TechCrossIT Demo",
            tone="formal",
        ),
    },
    "support_desk": {
        "runner": support_run,
        "intake": JobIntake(
            company_id="support_desk",
            job_type="triage_ticket",
            brief="Ticket from customer Jane Smith: 'I was charged twice this month! "
                  "I can see two payments of £99 on my bank statement from 14 Feb and 15 Feb. "
                  "This is absolutely ridiculous. I want a refund immediately and an explanation. "
                  "I've been a customer for 2 years!'",
            client_name="TechCrossIT Demo",
            tone="empathetic",
        ),
    },
}


def run_demo(company_id: str):
    demo = DEMOS[company_id]
    print(f"\n{'='*60}")
    print(f"  COMPANY: {company_id.upper().replace('_', ' ')}")
    print(f"  JOB:     {demo['intake'].job_type}")
    print(f"{'='*60}")
    print(f"\nBRIEF: {demo['intake'].brief[:100]}...\n")

    start = time.time()
    result = demo["runner"](demo["intake"])
    elapsed = time.time() - start

    print(f"STATUS:   {result.status}")
    print(f"JOB ID:   {result.job_id}")
    print(f"DURATION: {result.duration_ms}ms (total: {elapsed:.2f}s)")
    print(f"TOKENS:   {result.tokens_used}")
    print(f"\n--- OUTPUT (first 800 chars) ---\n")
    if result.output:
        print(result.output[:800])
        if len(result.output) > 800:
            print(f"\n... [{len(result.output) - 800} more chars]")
    else:
        print(f"ERROR: {result.error}")
    print()


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nERROR: ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    target = sys.argv[1] if len(sys.argv) > 1 else None

    print("\n" + "="*60)
    print("  TechCrossIT Mini Companies — Live Demo")
    print("="*60)

    if target:
        if target not in DEMOS:
            print(f"Unknown company: {target}. Choose from: {list(DEMOS.keys())}")
            sys.exit(1)
        run_demo(target)
    else:
        for company_id in DEMOS:
            run_demo(company_id)
            time.sleep(1)  # Small pause between calls

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
