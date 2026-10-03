from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sggradmatch.data import load_programmes  # noqa: E402
from sggradmatch.models import StudentProfile  # noqa: E402
from sggradmatch.pipeline import recommend  # noqa: E402
from sggradmatch.ranking import rank_programmes  # noqa: E402


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.programmes = load_programmes(ROOT / "data" / "processed" / "programmes.csv")
        self.profile = json.loads(
            (ROOT / "examples" / "student_profile.json").read_text(encoding="utf-8")
        )

    def test_dataset_contains_21_programmes(self) -> None:
        self.assertEqual(len(self.programmes), 21)
        self.assertEqual({p.university for p in self.programmes}, {"NUS", "NTU", "SMU"})

    def test_hybrid_returns_three_grounded_programmes(self) -> None:
        result = recommend(self.profile, method="hybrid")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(len(result["recommendations"]), 3)
        valid_ids = {programme.programme_id for programme in self.programmes}
        for item in result["recommendations"]:
            self.assertIn(item["programme_id"], valid_ids)
            self.assertTrue(item["source_url"].startswith("https://"))

    def test_budget_filter_removes_known_over_budget_programmes(self) -> None:
        data = dict(self.profile)
        data["budget_sgd"] = 50000
        profile = StudentProfile.from_dict(data)
        ranked = rank_programmes(profile, self.programmes, method="hybrid", limit=21)
        self.assertTrue(
            all(
                item.programme.tuition_sgd is None
                or item.programme.tuition_sgd <= data["budget_sgd"]
                for item in ranked
            )
        )

    def test_rule_and_hybrid_are_distinct_methods(self) -> None:
        profile = StudentProfile.from_dict(self.profile)
        rule = rank_programmes(profile, self.programmes, method="rule")
        hybrid = rank_programmes(profile, self.programmes, method="hybrid")
        self.assertEqual(len(rule), 3)
        self.assertEqual(len(hybrid), 3)
        self.assertTrue(all(item.method == "rule" for item in rule))
        self.assertTrue(all(item.method == "hybrid" for item in hybrid))


if __name__ == "__main__":
    unittest.main()
