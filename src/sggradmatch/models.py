"""Typed domain models for student profiles, programmes and recommendations.

The conversion helpers normalise JSON and CSV values at the boundary so the
ranking pipeline can operate on consistent Python types.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


def _items(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value if str(item).strip()]
    return [item.strip().lower() for item in str(value).split("|") if item.strip()]


def _number(value: Any) -> float | None:
    if value in (None, "", "unknown", "null"):
        return None
    return float(value)


@dataclass(frozen=True)
class StudentProfile:
    """Applicant goals and constraints accepted by the ranking pipeline."""
    profile_id: str
    academic_background: str
    career_goal: str
    interests: list[str]
    budget_sgd: float | None = None
    preferred_mode: str = "full-time"
    max_duration_months: int | None = None
    years_experience: float = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StudentProfile":
        return cls(
            profile_id=str(data.get("profile_id", "interactive-profile")),
            academic_background=str(data.get("academic_background", "")).strip().lower(),
            career_goal=str(data.get("career_goal", "")).strip().lower(),
            interests=_items(data.get("interests")),
            budget_sgd=_number(data.get("budget_sgd")),
            preferred_mode=str(data.get("preferred_mode", "full-time")).strip().lower(),
            max_duration_months=(
                int(data["max_duration_months"])
                if data.get("max_duration_months") not in (None, "", "unknown")
                else None
            ),
            years_experience=float(data.get("years_experience", 0) or 0),
        )

    def search_text(self) -> str:
        return " ".join(
            [self.academic_background, self.career_goal, *self.interests]
        ).strip()


@dataclass(frozen=True)
class Programme:
    """One source-linked programme record from the curated catalogue."""
    programme_id: str
    university: str
    programme_name: str
    domains: list[str]
    study_modes: list[str]
    duration_ft_months: int | None
    duration_pt_months: int | None
    tuition_sgd: float | None
    academic_backgrounds: list[str]
    experience_note: str
    curriculum: str
    career_outcomes: str
    source_url: str
    last_verified_at: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Programme":
        def integer(name: str) -> int | None:
            value = row.get(name, "").strip()
            return int(value) if value else None

        return cls(
            programme_id=row["programme_id"].strip(),
            university=row["university"].strip(),
            programme_name=row["programme_name"].strip(),
            domains=_items(row.get("domains")),
            study_modes=_items(row.get("study_modes")),
            duration_ft_months=integer("duration_ft_months"),
            duration_pt_months=integer("duration_pt_months"),
            tuition_sgd=_number(row.get("tuition_sgd")),
            academic_backgrounds=_items(row.get("academic_backgrounds")),
            experience_note=row.get("experience_note", "").strip(),
            curriculum=row.get("curriculum", "").strip(),
            career_outcomes=row.get("career_outcomes", "").strip(),
            source_url=row.get("source_url", "").strip(),
            last_verified_at=row.get("last_verified_at", "").strip(),
        )

    def retrieval_text(self) -> str:
        return " ".join(
            [
                self.programme_name,
                " ".join(self.domains),
                " ".join(self.academic_backgrounds),
                self.curriculum,
                self.career_outcomes,
            ]
        )


@dataclass
class Recommendation:
    """A ranked programme with its score, fit reasons and warnings."""
    programme: Programme
    score: float
    method: str
    fit_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["programme"] = asdict(self.programme)
        return data
