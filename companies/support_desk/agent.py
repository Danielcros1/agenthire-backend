"""
TechCrossIT — The Support Desk
AI customer support team: ticket triage, responses, FAQs, knowledge base, reports.
"""

import os
import time
import uuid
from anthropic import Anthropic
from marketplace.models import JobIntake, JobResult, JobStatus


SYSTEM_PROMPT = """You are The Support Desk — TechCrossIT's AI customer support team.
You are empathetic, clear, and solution-focused. Every response should leave the customer feeling heard and helped.
Match the client's brand tone. Never escalate unnecessarily — resolve at first contact where possible.
When triaging, be precise about priority and category. When writing documentation, be clear enough for a non-technical reader."""


JOB_PROMPTS = {

    "triage_ticket": """Triage the following support ticket. Provide:
- Priority: P1 (critical/outage) | P2 (urgent) | P3 (normal) | P4 (low)
- Category: Bug | Billing | Account | Feature Request | How-To | Complaint | Other
- Sentiment: Angry | Frustrated | Neutral | Happy
- Suggested assignee team: Technical / Billing / Customer Success / Management
- Suggested SLA: response within X hours
- 2-sentence summary of the issue
- Suggested resolution path (what needs to happen to close this)

Ticket: {brief}
Context: {context}""",

    "draft_response": """Draft a professional, empathetic customer support response to the following ticket.
The response should:
- Acknowledge the customer's issue
- Apologise if appropriate (without admitting fault unless facts confirm it)
- Provide a clear resolution or next step
- Set expectations for timeline
- Close warmly with contact details
Max 200 words. Tone: {tone}.

Ticket / situation: {brief}
Context: {context}""",

    "write_faq": """Write a comprehensive FAQ article for the following topic/product feature.
Include: article title, 6-10 Q&As, a "Still need help?" footer section.
Use plain English. Organise questions from basic to advanced.

Topic: {brief}
Context: {context}""",

    "knowledge_base_entry": """Write a knowledge base article for the following topic.
Structure:
- Title (action-oriented: "How to...", "Understanding...")
- Overview (2-3 sentences)
- Prerequisites (if any)
- Step-by-step instructions (numbered)
- Screenshots/video placeholders (note where visuals should go)
- Common errors and fixes
- Related articles (suggest 3 titles)
- Last updated: [today's date]

Topic: {brief}
Context: {context}""",

    "escalation_report": """Write an escalation summary report for the following support situation.
Include:
- Incident summary
- Timeline of events
- Customer impact assessment
- Root cause (known or suspected)
- Actions taken so far
- Recommended escalation path
- Proposed resolution and timeline
- Lessons learned / prevention suggestions

Situation: {brief}
Context: {context}""",

    "onboarding_email": """Write a warm, helpful customer onboarding email sequence (3 emails).
Email 1 (day 0 - welcome): Welcome message, account setup steps, key resources
Email 2 (day 3 - getting started): First key action to take, quick wins, tip
Email 3 (day 7 - check-in): Progress check, feature highlight, invite to office hours/demo

Each email: subject line, preview text, full body, CTA. Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "apology_letter": """Write a sincere, professional service recovery letter for the following situation.
The letter should:
- Open with a genuine, specific apology
- Acknowledge the impact on the customer
- Explain briefly what happened (without over-explaining)
- State concrete steps being taken to fix/prevent this
- Offer a goodwill gesture (use [GOODWILL_GESTURE] placeholder if not specified)
- Close with a personal commitment

Situation: {brief}
Context: {context}""",

    "support_weekly_report": """Generate a weekly support report based on the data provided.
Include:
- Week summary (total tickets, resolution rate, avg response time)
- Ticket volume by category (table)
- Top 5 recurring issues
- Customer satisfaction highlights (positive + negative)
- SLA compliance rate
- Trends vs previous week
- 3 recommended actions for next week

Data / brief: {brief}
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
                company_id="support_desk",
                job_type=intake.job_type,
                status=JobStatus.FAILED,
                error=f"Unknown job type: {intake.job_type}",
            )

        prompt = prompt_template.format(
            brief=intake.brief,
            context=intake.context or "No additional context provided.",
            tone=intake.tone or "friendly",
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
            company_id="support_desk",
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
            company_id="support_desk",
            job_type=intake.job_type,
            status=JobStatus.FAILED,
            error=str(e),
            duration_ms=int((time.time() - start) * 1000),
        )
