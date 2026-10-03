"""Dependency-free tokenisation, TF-IDF retrieval and term-overlap scoring.

The in-memory index is intentionally small and transparent for the 21-record
course-project catalogue.
"""

from __future__ import annotations

import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+.#-]*")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "for", "from", "in", "into",
    "is", "of", "on", "or", "the", "to", "with", "want", "wants", "seeking",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if token not in STOPWORDS and len(token) > 1
    ]


class TfidfIndex:
    """Build an in-memory TF-IDF index and score queries by cosine similarity."""
    def __init__(self, documents: list[str]):
        self.documents = documents
        tokenized = [tokenize(document) for document in documents]
        document_frequency: Counter[str] = Counter()
        for tokens in tokenized:
            document_frequency.update(set(tokens))
        count = max(len(documents), 1)
        self.idf = {
            token: math.log((count + 1) / (frequency + 1)) + 1
            for token, frequency in document_frequency.items()
        }
        self.vectors = [self._vector(tokens) for tokens in tokenized]

    def _vector(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        total = max(sum(counts.values()), 1)
        return {
            token: (frequency / total) * self.idf.get(token, 0.0)
            for token, frequency in counts.items()
            if token in self.idf
        }

    @staticmethod
    def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        numerator = sum(value * right.get(key, 0.0) for key, value in left.items())
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if not left_norm or not right_norm:
            return 0.0
        return numerator / (left_norm * right_norm)

    def similarities(self, query: str) -> list[float]:
        query_vector = self._vector(tokenize(query))
        return [self._cosine(query_vector, vector) for vector in self.vectors]


def overlap_score(query_terms: list[str], document_terms: list[str]) -> float:
    left = set(tokenize(" ".join(query_terms)))
    right = set(tokenize(" ".join(document_terms)))
    return len(left & right) / max(len(left), 1)
