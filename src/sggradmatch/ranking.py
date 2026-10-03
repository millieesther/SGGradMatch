"""Rank eligible programmes with the baseline or hybrid scoring formula.

Both methods share deterministic hard filtering. The rule-only baseline uses
overlap scores; the hybrid method adds local TF-IDF relevance.
"""

from __future__ import annotations

from .models import Programme, Recommendation, StudentProfile
from .retrieval import TfidfIndex, overlap_score
from .rules import evaluate_hard_constraints


def rank_programmes(
    profile: StudentProfile,
    programmes: list[Programme],
    method: str = "hybrid",
    limit: int = 3,
) -> list[Recommendation]:
    """Return up to ``limit`` eligible programmes ordered by the chosen method."""
    if method not in {"rule", "hybrid"}:
        raise ValueError("method must be 'rule' or 'hybrid'")

    eligible: list[tuple[Programme, list[str], list[str]]] = []
    for programme in programmes:
        decision = evaluate_hard_constraints(profile, programme)
        if decision.eligible:
            eligible.append((programme, decision.reasons, decision.warnings))

    index = TfidfIndex([item[0].retrieval_text() for item in eligible])
    semantic_scores = index.similarities(profile.search_text()) if eligible else []

    ranked: list[Recommendation] = []
    for position, (programme, reasons, warnings) in enumerate(eligible):
        interest_score = overlap_score(
            [profile.career_goal, *profile.interests],
            [*programme.domains, programme.curriculum, programme.career_outcomes],
        )
        background_score = overlap_score(
            [profile.academic_background], programme.academic_backgrounds
        )
        semantic_score = semantic_scores[position]
        if method == "rule":
            score = 0.8 * interest_score + 0.2 * background_score
        else:
            score = 0.7 * semantic_score + 0.2 * interest_score + 0.1 * background_score

        fit_reasons = list(reasons)
        if interest_score > 0:
            fit_reasons.append("Curriculum or career outcomes overlap with the stated goal.")
        if semantic_score > 0:
            fit_reasons.append("Programme description is semantically related to the profile.")
        if background_score > 0:
            fit_reasons.append("Published background guidance overlaps with the profile.")
        if not fit_reasons:
            fit_reasons.append("Programme passed the available hard constraints.")

        ranked.append(
            Recommendation(
                programme=programme,
                score=round(score, 6),
                method=method,
                fit_reasons=fit_reasons,
                warnings=warnings,
            )
        )

    ranked.sort(key=lambda item: (-item.score, item.programme.programme_id))
    return ranked[:limit]
