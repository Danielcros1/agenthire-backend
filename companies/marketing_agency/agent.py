"""
TechCrossIT — The Marketing Agency
AI content and copywriting team: blogs, email campaigns, social media, SEO, ad copy.
"""

import os
import time
import uuid
from anthropic import Anthropic
from marketplace.models import JobIntake, JobResult, JobStatus


SYSTEM_PROMPT = """You are The Marketing Agency — TechCrossIT's AI content and copywriting team.
You create compelling, conversion-focused content that is brand-consistent and ready to publish.
Always match the requested tone. Write for humans, not search engines.
Structure output clearly: use headers, subheadings, and calls-to-action where appropriate.
Every piece of content must be complete and ready to use — no placeholders."""


JOB_PROMPTS = {

    "write_blog_post": """Write a full, SEO-optimised blog post based on the brief below.
Include: H1 title, meta description (155 chars), introduction hook, 4-6 sections with H2 headings,
relevant statistics or examples, CTA at the end, and suggested 5 tags.
Length: 800-1200 words. Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "social_media_pack": """Create a social media content pack of 5 posts based on the brief.
Provide one post for each: LinkedIn, X (Twitter), Instagram, Facebook, and TikTok caption.
Each post must be platform-appropriate in length and style.
Include relevant hashtags. Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "email_campaign": """Write a 3-email nurture campaign sequence.
Email 1 — Welcome/Introduction (day 1)
Email 2 — Value/Education (day 3)
Email 3 — Soft CTA / Offer (day 7)
Each email: subject line, preview text, full body copy, and CTA button text.
Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "seo_research": """Perform SEO keyword research for the topic below.
Provide:
1. Primary keyword (highest intent)
2. 10 secondary/long-tail keywords with estimated search intent (informational / transactional / navigational)
3. 5 competitor content gap opportunities
4. Recommended content structure for the primary keyword
5. Meta title and description suggestions

Topic: {brief}
Context: {context}""",

    "ad_copy": """Write high-converting ad copy for Google and Meta (Facebook/Instagram).
For Google Ads: 3 headlines (30 chars each), 2 descriptions (90 chars each), display URL path.
For Meta Ads: primary text (125 chars), headline (40 chars), description (30 chars).
Also provide: A/B variant for each format.
Tone: {tone}. Target audience context:
Brief: {brief}
Context: {context}""",

    "content_calendar": """Create a detailed 4-week content calendar for the following brand/campaign.
For each week: 2 blog post ideas (title + outline), 5 social posts spread across platforms,
1 email newsletter theme, 1 PR/outreach opportunity.
Format as a clean markdown table or structured list.
Brief: {brief}
Context: {context}""",

    "product_description": """Write 5 compelling product/service descriptions based on the brief.
Each description: 80-120 words, benefit-led (not feature-led), with a strong closing CTA.
Include an SEO-friendly title for each.
Tone: {tone}.
Brief: {brief}
Context: {context}""",

    "press_release": """Write a professional press release based on the brief.
Structure: Headline, subheadline, dateline, lead paragraph (who/what/when/where/why),
body (2-3 paragraphs), quote from spokesperson, boilerplate about the company, contact details.
Follow AP/UK press release style. Tone: {tone}.
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
                company_id="marketing_agency",
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
            company_id="marketing_agency",
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
            company_id="marketing_agency",
            job_type=intake.job_type,
            status=JobStatus.FAILED,
            error=str(e),
            duration_ms=int((time.time() - start) * 1000),
        )
