"""Create grounded recommendation explanations.

The default path formats local ranking evidence without an external service.
The optional OpenAI path explains programme IDs that local code already fixed.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .models import Recommendation, StudentProfile


def grounded_summary(
    profile: StudentProfile, recommendations: list[Recommendation]
) -> dict:
    """Format ranked records, sources and warnings into the public response."""
    if len(recommendations) < 2:
        return {
            "status": "abstain",
            "message": "Fewer than two programmes satisfy the stated hard constraints.",
            "recommendations": [],
        }
    results = []
    for item in recommendations:
        programme = item.programme
        results.append(
            {
                "programme_id": programme.programme_id,
                "programme_name": programme.programme_name,
                "university": programme.university,
                "score": item.score,
                "fit": item.fit_reasons,
                "trade_offs": item.warnings
                or ["Admission remains subject to the university's formal assessment."],
                "source_url": programme.source_url,
                "last_verified_at": programme.last_verified_at,
            }
        )
    return {
        "status": "ok",
        "message": (
            "Programme fit is decision support, not an admission prediction. "
            "Verify all requirements on the cited official pages."
        ),
        "profile_id": profile.profile_id,
        "recommendations": results,
    }


def openai_explanations(
    profile: StudentProfile, recommendations: list[Recommendation]
) -> dict:
    """Generate explanations for a ranking that the local pipeline already fixed.

    The model cannot add or replace programme IDs. The function is optional and is
    never called unless the user explicitly enables it and supplies OPENAI_API_KEY.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    model = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    grounded = grounded_summary(profile, recommendations)
    allowed = [item["programme_id"] for item in grounded["recommendations"]]
    prompt = {
        "task": "Explain the fixed ranked list using only the supplied evidence.",
        "rules": [
            "Do not add or replace programme IDs.",
            "Do not predict admission outcomes.",
            "Do not invent missing fees, requirements, dates, or rankings.",
            "Keep each explanation under 90 words.",
        ],
        "student_profile": profile.__dict__,
        "fixed_ranking": grounded["recommendations"],
    }
    schema = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "programme_id": {"type": "string", "enum": allowed},
                        "explanation": {"type": "string"},
                        "caution": {"type": "string"},
                    },
                    "required": ["programme_id", "explanation", "caution"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False,
    }
    payload = {
        "model": model,
        "store": False,
        "input": json.dumps(prompt),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "grounded_programme_explanations",
                "strict": True,
                "schema": schema,
            }
        },
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI request failed with HTTP {exc.code}: {detail}") from exc

    output_text = body.get("output_text")
    if not output_text:
        for item in body.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    output_text = content.get("text")
                    break
    if not output_text:
        raise RuntimeError("OpenAI response did not contain output text")
    result = json.loads(output_text)
    returned = [item["programme_id"] for item in result["recommendations"]]
    if set(returned) != set(allowed):
        raise RuntimeError("Model output changed the fixed programme set")
    return result
