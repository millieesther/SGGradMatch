"""Apply deterministic eligibility checks before relevance ranking.

Known conflicts in study mode, tuition or duration reject a programme.
Unknown numeric values remain eligible but produce explicit warnings.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Programme, StudentProfile


@dataclass
class RuleDecision:
    """Eligibility result with fit reasons and uncertainty warnings."""
    eligible: bool
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def evaluate_hard_constraints(
    profile: StudentProfile, programme: Programme
) -> RuleDecision:
    """Evaluate one programme against the profile's hard constraints."""
    reasons: list[str] = []
    warnings: list[str] = []

    if profile.preferred_mode and profile.preferred_mode not in programme.study_modes:
        return RuleDecision(False, warnings=["Preferred study mode is unavailable."])
    reasons.append(f"Offers {profile.preferred_mode} study.")

    if profile.budget_sgd is not None:
        if programme.tuition_sgd is None:
            warnings.append("Tuition is unknown and must be checked on the official page.")
        elif programme.tuition_sgd > profile.budget_sgd:
            return RuleDecision(False, warnings=["Known tuition exceeds the stated budget."])
        else:
            reasons.append("Known tuition is within the stated budget.")

    duration = (
        programme.duration_ft_months
        if profile.preferred_mode == "full-time"
        else programme.duration_pt_months
    )
    if profile.max_duration_months is not None:
        if duration is None:
            warnings.append("Duration is unknown and must be verified.")
        elif duration > profile.max_duration_months:
            return RuleDecision(False, warnings=["Known duration exceeds the stated limit."])
        else:
            reasons.append("Known duration is within the stated limit.")

    if programme.tuition_sgd is None:
        warnings.append("Dataset does not contain a verified tuition figure.")
    return RuleDecision(True, reasons=reasons, warnings=warnings)
