"""
TechCrossIT — The Sales Team
AI B2B sales support: prospect research, outreach emails, pitch decks, proposals, competitive analysis.
"""

import os
import time
import uuid
from anthropic import Anthropic
from marketplace.models import JobIntake, JobResult, JobStatus


SYSTEM_PROMPT = """You are The Sales Team — TechCrossIT's AI-powered B2B sales unit.
You are expert at research, persuasion, and closing. Your outputs are specific, personalised, and actionable.
Never use generic templates — always weave in the client's context and the prospect's situation.
Be direct, confident, and value-focused. Every piece of output should move a deal forward."""


JOB_PROMPTS = {

    "prospect_research": """Research the following prospect and produce a structured intelligence brief.
Include:
- Company overview (size, sector, revenue estimate, key products/services)
- Key decision-makers (names, titles, LinkedIn cues from brief)
- Recent news / trigger events (funding, expansion, pain signals)
- Budget signals and procurement cycle
- Recommended angle / hook for outreach
- 3 personalised conversation starters

Prospect brief: {brief}
Context: {context}""",

    "cold_outreach_email": """Write a highly personalised cold outreach email.
Rules: Subject line under 8 words, opening line references something specific about the prospect,
value prop in 1-2 sentences, social proof (1 sentence), clear single CTA (meeting request).
Max 150 words in the body. Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "followup_sequence": """Write a 5-email follow-up sequence for a prospect who hasn't responded.
Email 1 (day 3): soft bump
Email 2 (day 7): add new value / insight
Email 3 (day 14): different angle / case study
Email 4 (day 21): social proof / urgency
Email 5 (day 30): graceful breakup
Each email: subject line + full body copy (max 120 words each). Tone: {tone}.
Brief / original outreach context: {brief}
Context: {context}""",

    "pitch_deck_outline": """Create a structured pitch deck outline for the following opportunity.
Provide 10-12 slides with: slide title, key message (1 sentence), bullet points (3-5), and visual suggestion.
Slides must tell a story: Problem → Solution → Market → Product → Traction → Team → Ask.
Brief: {brief}
Context: {context}""",

    "competitive_analysis": """Produce a competitive analysis for the following market/product.
Cover: 4-6 key competitors, feature comparison matrix, pricing comparison, strengths and weaknesses,
positioning gaps we can exploit, and a recommended differentiation strategy.
Format clearly for use in a sales conversation. Brief: {brief}
Context: {context}""",

    "objection_handler": """Write a complete objection-handling script for common sales objections.
For each objection provide: the objection, an empathetic acknowledgement, the reframe,
supporting evidence, and a closing question to regain momentum.
Cover at least 8 objections relevant to the brief. Tone: {tone}.
Brief / product/service context: {brief}
Context: {context}""",

    "proposal_draft": """Write a full client proposal / scope of work document.
Structure:
1. Executive Summary
2. Understanding of the Brief
3. Proposed Solution / Approach
4. Deliverables & Timeline
5. Investment (use [PRICE] placeholder for client to fill)
6. Team / Why Us
7. Next Steps
Professional, client-ready tone. Length: 600-900 words.
Brief: {brief}
Context: {context}""",

    "crm_enrichment": """Enrich the following CRM record with research-based data.
Provide: full company profile, estimated employee count, industry code (SIC), tech stack signals,
LinkedIn company page URL format, estimated annual revenue band, and 3 tailored notes a sales rep
should know before calling. Format as clean JSON + plain text summary.
Record: {brief}
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
                company_id="sales_team",
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
            company_id="sales_team",
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
            company_id="sales_team",
            job_type=intake.job_type,
            status=JobStatus.FAILED,
            error=str(e),
            duration_ms=int((time.time() - start) * 1000),
        )
