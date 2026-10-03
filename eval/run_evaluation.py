"""Compare rule-only and hybrid ranking on the fixed JSONL benchmark.

The script reports aggregate metrics and saves per-profile cases for error
analysis. Checked-in labels are second-pass author-reviewed judgements.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sggradmatch.data import load_programmes  # noqa: E402
from sggradmatch.models import StudentProfile  # noqa: E402
from sggradmatch.ranking import rank_programmes  # noqa: E402
from sggradmatch.rules import evaluate_hard_constraints  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def evaluate(method: str, profiles: list[dict], truth: dict[str, set[str]]) -> dict:
    """Evaluate one ranking method against the supplied relevance sets."""
    programmes = load_programmes(ROOT / "data" / "processed" / "programmes.csv")
    successes = 0
    relevant = 0
    returned = 0
    violations = 0
    cases = []
    for raw_profile in profiles:
        profile = StudentProfile.from_dict(raw_profile)
        recommendations = rank_programmes(profile, programmes, method=method, limit=3)
        ids = [item.programme.programme_id for item in recommendations]
        expected = truth[profile.profile_id]
        hits = len(set(ids) & expected)
        success = hits >= 2
        successes += int(success)
        relevant += hits
        returned += len(ids)
        for item in recommendations:
            if not evaluate_hard_constraints(profile, item.programme).eligible:
                violations += 1
        cases.append(
            {
                "profile_id": profile.profile_id,
                "recommendations": ids,
                "hits": hits,
                "success": success,
            }
        )
    count = len(profiles)
    return {
        "method": method,
        "profiles": count,
        "profile_success_rate_at_3": round(successes / count, 4),
        "precision_at_3": round(relevant / max(returned, 1), 4),
        "hard_constraint_violation_rate": round(violations / max(returned, 1), 4),
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=ROOT / "eval" / "test_profiles.jsonl")
    parser.add_argument("--truth", type=Path, default=ROOT / "eval" / "ground_truth.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "eval" / "results" / "evaluation_results.json")
    args = parser.parse_args()
    profiles = read_jsonl(args.profiles)
    truth_rows = read_jsonl(args.truth)
    truth = {row["profile_id"]: set(row["suitable_programmes"]) for row in truth_rows}
    missing = {row["profile_id"] for row in profiles} - set(truth)
    if missing:
        raise ValueError(f"Missing ground truth for: {sorted(missing)}")
    result = {
        "benchmark_status": "second-pass author-reviewed labels; self-evaluation, not independent ground truth",
        "rule": evaluate("rule", profiles, truth),
        "hybrid": evaluate("hybrid", profiles, truth),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    summary = {name: {k: v for k, v in values.items() if k != "cases"} for name, values in result.items() if isinstance(values, dict)}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
