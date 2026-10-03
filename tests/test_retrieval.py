from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sggradmatch.retrieval import TfidfIndex, tokenize  # noqa: E402


class RetrievalTests(unittest.TestCase):
    def test_tokenizer_normalises_case(self) -> None:
        self.assertEqual(tokenize("Machine Learning"), ["machine", "learning"])

    def test_relevant_document_scores_higher(self) -> None:
        index = TfidfIndex(["machine learning artificial intelligence", "finance accounting markets"])
        scores = index.similarities("AI machine learning engineer")
        self.assertGreater(scores[0], scores[1])


if __name__ == "__main__":
    unittest.main()

