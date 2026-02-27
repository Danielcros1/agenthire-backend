"""
TechCrossIT — The Finance Office
AI bookkeeping and finance team: invoices, expense reports, budgets, cash flow, VAT.
"""

import os
import time
import uuid
from anthropic import Anthropic
from marketplace.models import JobIntake, JobResult, JobStatus


SYSTEM_PROMPT = """You are The Finance Office — TechCrossIT's AI accounting and finance team.
You produce HMRC-compliant, accurate financial documents for UK businesses.
Always use GBP (£) unless stated otherwise. Apply 20% standard VAT rate unless instructed.
Format numbers consistently: £12,500.00. Use ISO 8601 dates (DD Mon YYYY format for documents).
All output must be ready for immediate use — no placeholders for numbers the client provided."""


JOB_PROMPTS = {

    "generate_invoice": """Generate a complete, HMRC-compliant invoice based on the brief.
Include:
- Invoice number (format: INV-YYYYMMDD-XXXX), date, payment due date (30 days default)
- Seller and buyer details (use what's provided in the brief)
- Line items with quantity, unit price, and line total
- Subtotal, VAT @ 20%, and TOTAL DUE
- Payment terms and bank details placeholders
- Professional formatting in plain text / markdown

Brief: {brief}
Context: {context}""",

    "expense_report": """Create a professional expense report based on the details provided.
Include:
- Report title, employee name, period covered
- Itemised expense table (date, description, category, amount, VAT recoverable)
- Category subtotals
- Grand total and VAT total
- Approval line

Brief: {brief}
Context: {context}""",

    "cashflow_projection": """Build a 12-month cash flow projection based on the brief.
Include:
- Opening balance
- Monthly income (broken down by revenue stream where stated)
- Monthly outgoings (by category)
- Net cash flow per month
- Closing balance
- Commentary: 3 key observations about the projection
- Risk flags if any months go negative

Brief: {brief}
Context: {context}""",

    "budget_template": """Create a structured annual budget template.
Include:
- Revenue budget (split by product/service line if stated)
- Cost of Sales
- Gross Profit
- Operating expenses (HR, Marketing, Tech, Admin, etc.)
- EBITDA
- Monthly breakdown
- YTD actuals column (blank, ready to fill)
Format as a clear markdown table with all figures.

Brief: {brief}
Context: {context}""",

    "financial_summary": """Write a clear, board-ready financial summary report.
Include:
- Executive summary (3 key headlines)
- Revenue performance vs target
- Cost analysis
- Profitability metrics (gross margin, EBITDA)
- Cash position
- Key variances explained
- Forward outlook / recommendations
Length: 400-600 words plus supporting tables.

Brief: {brief}
Context: {context}""",

    "vat_calculation": """Calculate and summarise VAT obligations based on the information provided.
Include:
- VAT registration threshold note (£90,000 UK 2024)
- Taxable supplies total
- VAT collected (output tax)
- VAT paid on purchases (input tax)
- Net VAT payable / reclaimable
- Quarterly return period
- Any applicable schemes (Flat Rate, Cash Accounting) if relevant

Brief: {brief}
Context: {context}""",

    "payment_reminder": """Write a professional payment reminder email sequence (3 levels).
Level 1 (due date): polite reminder
Level 2 (7 days overdue): firm but friendly
Level 3 (14 days overdue): formal final notice
Each email: subject line, full body, and action required. Tone: {tone}.

Brief: {brief}
Context: {context}""",

    "profit_loss": """Generate a Profit & Loss statement based on the figures provided.
Include:
- Revenue (by category if available)
- Cost of Goods Sold / Cost of Sales
- Gross Profit & Gross Margin %
- Operating Expenses (itemised)
- Operating Profit (EBIT)
- Interest / Finance costs
- Profit Before Tax
- Tax estimate (25% Corporation Tax for UK)
- Net Profit & Net Margin %
- Period-over-period comparison if prior data provided

Brief: {brief}
Context: {context}""",
}


def run(intake: JobIntake) -> JobResult:
    start = time.time()
    job_id = str(uuid.uuid4())[:12]

    try:
        prompt_template = JOB_PROMPTS.get(intake.job_type)
        if not prompt_template:
            return JobResult(
                job_id=job_id,
                company_id="finance_office",
                job_type=intake.job_type,
                status=JobStatus.FAILED,
                error=f"Unknown job type: {intake.job_type}",
            )

        prompt = prompt_template.format(
            brief=intake.brief,
            context=intake.context or "No additional context provided.",
            tone=intake.tone or "professional",
        )

        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        output = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        duration = int((time.time() - start) * 1000)

        return JobResult(
            job_id=job_id,
            company_id="finance_office",
            job_type=intake.job_type,
            status=JobStatus.DONE,
            output=output,
            metadata={
                "client": intake.client_name or "Anonymous",
                "tone": intake.tone,
                "model": "claude-sonnet-4-6",
            },
            duration_ms=duration,
            tokens_used=tokens,
        )

    except Exception as e:
        return JobResult(
            job_id=job_id,
            company_id="finance_office",
            job_type=intake.job_type,
            status=JobStatus.FAILED,
            error=str(e),
            duration_ms=int((time.time() - start) * 1000),
        )
