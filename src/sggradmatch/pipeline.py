"""Orchestrate profile parsing, catalogue loading, ranking and explanation.

``recommend`` is the main application boundary used by both interfaces.
"""

from __future__ import annotations

from .data import load_programmes
from .generator import grounded_summary, openai_explanations
from .models import StudentProfile
from .ranking import rank_programmes


def recommend(
    profile_data: dict,
    method: str = "hybrid",
    use_openai: bool = False,
    programme_path: str | None = None,
) -> dict:
    """Return a grounded recommendation response for one profile dictionary."""
    profile = StudentProfile.from_dict(profile_data)
    programmes = load_programmes(programme_path)
    ranked = rank_programmes(profile, programmes, method=method, limit=3)
    result = grounded_summary(profile, ranked)
    if use_openai and result["status"] == "ok":
        result["llm_explanations"] = openai_explanations(profile, ranked)
    return result
