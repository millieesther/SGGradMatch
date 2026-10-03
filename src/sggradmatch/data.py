"""Load and validate the curated programme catalogue from CSV.

This module converts catalogue rows into typed ``Programme`` records. It does
not scrape university websites or infer missing values.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .models import Programme


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_programme_path() -> Path:
    return repository_root() / "data" / "processed" / "programmes.csv"


def load_programmes(path: str | Path | None = None) -> list[Programme]:
    """Return catalogue records from ``path`` or the repository default."""
    source = Path(path) if path else default_programme_path()
    with source.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    programmes = [Programme.from_row(row) for row in rows]
    ids = [item.programme_id for item in programmes]
    if len(ids) != len(set(ids)):
        raise ValueError("programme_id values must be unique")
    if not programmes:
        raise ValueError("programme dataset is empty")
    return programmes
