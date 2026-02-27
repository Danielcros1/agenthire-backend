"""
TechCrossIT Marketplace — Company Registry
Single source of truth: lists all mini companies, their job templates, and routes jobs to the right agent.
"""

from typing import Dict, Type
from marketplace.models import CompanyCard

# ── COMPANY DISPLAY CARDS ────────────────────────────────────────────────────

COMPANY_CARDS: Dict[str, CompanyCard] = {

    "dev_shop": CompanyCard(
        id="dev_shop",
        name="The Dev Shop",
        tagline="Code written. Bugs fixed. Apps shipped.",
        description="Full-stack AI developer team. Give us a brief — we build REST APIs, fix bugs, "
                    "write tests, review code, and generate documentation. Works with Python, JS, "
                    "TypeScript, SQL and more.",
        phase=1,
        jobs=[
            {"key": "build_api_endpoint",   "label": "Build API Endpoint",         "time": "~90s"},
            {"key": "fix_bug",              "label": "Debug & Fix Bug",             "time": "~60s"},
            {"key": "write_tests",          "label": "Write Automated Tests",       "time": "~75s"},
            {"key": "code_review",          "label": "Code Review & Audit",         "time": "~60s"},
            {"key": "write_docs",           "label": "Write Documentation",         "time": "~45s"},
            {"key": "build_scraper",        "label": "Build Web Scraper",           "time": "~90s"},
            {"key": "design_db_schema",     "label": "Design Database Schema",      "time": "~60s"},
            {"key": "refactor_code",        "label": "Refactor & Optimise Code",    "time": "~75s"},
        ],
        icon="💻",
        colour="#6366F1",
        price_from="£0.80 / job",
    ),

    "marketing_agency": CompanyCard(
        id="marketing_agency",
        name="The Marketing Agency",
        tagline="Content that converts. Always on.",
        description="AI content strategists and copywriters. Blog posts, email campaigns, "
                    "social media content, SEO research, ad copy, and full content calendars — "
                    "all brand-matched and ready to publish.",
        phase=1,
        jobs=[
            {"key": "write_blog_post",      "label": "Write Blog Post",             "time": "~60s"},
            {"key": "social_media_pack",    "label": "Social Media Pack (5 posts)",  "time": "~75s"},
            {"key": "email_campaign",       "label": "Email Campaign (3 emails)",   "time": "~90s"},
            {"key": "seo_research",         "label": "SEO Keyword Research",        "time": "~45s"},
            {"key": "ad_copy",              "label": "Ad Copy (Google/Meta)",       "time": "~45s"},
            {"key": "content_calendar",     "label": "Monthly Content Calendar",    "time": "~75s"},
            {"key": "product_description",  "label": "Product Descriptions (x5)",  "time": "~60s"},
            {"key": "press_release",        "label": "Press Release",              "time": "~60s"},
        ],
        icon="📣",
        colour="#EC4899",
        price_from="£0.60 / job",
    ),

    "sales_team": CompanyCard(
        id="sales_team",
        name="The Sales Team",
        tagline="Prospects researched. Pipelines filled.",
        description="AI-powered B2B sales support. Prospect research, personalised outreach, "
                    "pitch decks, competitive analysis, objection-handling scripts, and "
                    "full follow-up sequences.",
        phase=1,
        jobs=[
            {"key": "prospect_research",    "label": "Prospect Research",          "time": "~60s"},
            {"key": "cold_outreach_email",  "label": "Cold Outreach Email",         "time": "~45s"},
            {"key": "followup_sequence",    "label": "Follow-Up Sequence (5 emails)","time": "~75s"},
            {"key": "pitch_deck_outline",   "label": "Pitch Deck Outline",         "time": "~60s"},
            {"key": "competitive_analysis", "label": "Competitive Analysis",       "time": "~75s"},
            {"key": "objection_handler",    "label": "Objection-Handling Script",  "time": "~45s"},
            {"key": "proposal_draft",       "label": "Proposal / Scope of Work",   "time": "~90s"},
            {"key": "crm_enrichment",       "label": "CRM Data Enrichment",        "time": "~45s"},
        ],
        icon="🎯",
        colour="#22C55E",
        price_from="£0.70 / job",
    ),

    "finance_office": CompanyCard(
        id="finance_office",
        name="The Finance Office",
        tagline="Invoices. Reports. Numbers sorted.",
        description="AI bookkeeping and finance team. Generate HMRC-compliant invoices, "
                    "expense reports, cash-flow projections, budget templates, VAT summaries, "
                    "and board-ready financial reports.",
        phase=1,
        jobs=[
            {"key": "generate_invoice",     "label": "Generate Invoice (VAT)",     "time": "~30s"},
            {"key": "expense_report",       "label": "Expense Report",             "time": "~45s"},
            {"key": "cashflow_projection",  "label": "Cash Flow Projection",       "time": "~60s"},
            {"key": "budget_template",      "label": "Budget Template",            "time": "~45s"},
            {"key": "financial_summary",    "label": "Financial Summary Report",   "time": "~60s"},
            {"key": "vat_calculation",      "label": "VAT Return Summary",         "time": "~30s"},
            {"key": "payment_reminder",     "label": "Payment Reminder Email",     "time": "~20s"},
            {"key": "profit_loss",          "label": "P&L Statement",              "time": "~60s"},
        ],
        icon="💰",
        colour="#F59E0B",
        price_from="£0.50 / job",
    ),

    "support_desk": CompanyCard(
        id="support_desk",
        name="The Support Desk",
        tagline="Every ticket answered. Every customer happy.",
        description="AI customer support team that never sleeps. Triage tickets, "
                    "draft responses, write FAQs, build knowledge bases, handle escalations, "
                    "and generate weekly support reports.",
        phase=1,
        jobs=[
            {"key": "triage_ticket",        "label": "Triage Support Ticket",      "time": "~20s"},
            {"key": "draft_response",       "label": "Draft Customer Response",    "time": "~30s"},
            {"key": "write_faq",            "label": "Write FAQ Article",          "time": "~45s"},
            {"key": "knowledge_base_entry", "label": "Knowledge Base Entry",       "time": "~45s"},
            {"key": "escalation_report",    "label": "Escalation Summary Report",  "time": "~45s"},
            {"key": "onboarding_email",     "label": "Customer Onboarding Email",  "time": "~30s"},
            {"key": "apology_letter",       "label": "Service Recovery Letter",    "time": "~30s"},
            {"key": "support_weekly_report","label": "Weekly Support Report",      "time": "~60s"},
        ],
        icon="🎧",
        colour="#14B8A6",
        price_from="£0.40 / job",
    ),
}


def get_all_cards() -> list:
    return list(COMPANY_CARDS.values())


def get_card(company_id: str) -> CompanyCard:
    if company_id not in COMPANY_CARDS:
        raise ValueError(f"Unknown company: {company_id}")
    return COMPANY_CARDS[company_id]


def get_job_types(company_id: str) -> list:
    return [j["key"] for j in COMPANY_CARDS[company_id].jobs]
