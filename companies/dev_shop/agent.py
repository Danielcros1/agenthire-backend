"""
TechCrossIT — The Dev Shop
AI development team: builds code, fixes bugs, writes tests, reviews code, writes docs.
"""

import os
import time
import uuid
from anthropic import Anthropic
from marketplace.models import JobIntake, JobResult, JobStatus


SYSTEM_PROMPT = """You are The Dev Shop — TechCrossIT's elite AI development team.
You write clean, production-ready code with proper error handling, type hints, comments, and tests.
Always output fully working, runnable code — never placeholders or pseudocode.
Use Python 3.11+ conventions unless the client specifies another language.
Format all code output inside markdown code blocks with the correct language tag.
Be concise but complete: every function must be usable without modification."""


JOB_PROMPTS = {

    "build_api_endpoint": """Build a complete, production-ready REST API endpoint based on the following brief.
Include: route definition, request/response Pydantic models, validation, error handling, docstring, and example curl command.
Use FastAPI.
Brief: {brief}
Context: {context}""",

    "fix_bug": """Debug and fix the following code issue completely.
Steps:
1. Identify the root cause (explain clearly in 2-3 sentences)
2. Provide the corrected code
3. Explain what changed and why
4. Add a unit test that proves the fix works

Brief / code to fix: {brief}
Context: {context}""",

    "write_tests": """Write a comprehensive test suite for the following code or feature.
Include: unit tests, edge cases, error cases, and at least one integration test.
Use pytest. Mock external dependencies. Aim for 90%+ coverage.
Code / feature to test: {brief}
Context: {context}""",

    "code_review": """Perform a thorough code review of the following code.
Cover: correctness, security, performance, readability, naming, error handling, and test coverage.
Format as:
- CRITICAL issues (must fix before shipping)
- WARNINGS (should fix)
- SUGGESTIONS (nice to have)
- APPROVED checks (things done well)
Code to review: {brief}
Context: {context}""",

    "write_docs": """Write clear, professional documentation for the following code or project.
Include: overview, installation/setup, usage examples, API reference (if applicable), and FAQ.
Use Markdown. Assume the reader is a developer but not familiar with the codebase.
Code / project to document: {brief}
Context: {context}""",

    "build_scraper": """Build a complete web scraper for the following requirement.
Include: full Python script using requests + BeautifulSoup (or Playwright if JS rendering needed),
rate limiting, retry logic, output to CSV/JSON, and error handling.
Brief: {brief}
Context: {context}""",

    "design_db_schema": """Design an optimal relational database schema for the following requirements.
Provide:
1. Entity-Relationship description
2. Full SQL CREATE TABLE statements with proper types, constraints, indexes, and foreign keys
3. Sample INSERT statements to demonstrate usage
4. Brief explanation of design decisions

Requirements: {brief}
Context: {context}""",

    "refactor_code": """Refactor and optimise the following code.
Goals: improve readability, performance, and maintainability.
Provide:
1. The refactored code (fully working)
2. A bullet-point changelog of what was improved and why
3. Performance impact estimate if applicable

Code to refactor: {brief}
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
                company_id="dev_shop",
                job_type=intake.job_type,
                status=JobStatus.FAILED,
                error=f"Unknown job type: {intake.job_type}",
            )

        prompt = prompt_template.format(
            brief=intake.brief,
            context=intake.context or "No additional context provided.",
        )

        if intake.tone == "casual":
            prompt += "\n\nKeep comments conversational — this is an internal team project."
        elif intake.tone == "technical":
            prompt += "\n\nMaximise technical depth — the audience are senior engineers."

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
            company_id="dev_shop",
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
            company_id="dev_shop",
            job_type=intake.job_type,
            status=JobStatus.FAILED,
            error=str(e),
            duration_ms=int((time.time() - start) * 1000),
        )
