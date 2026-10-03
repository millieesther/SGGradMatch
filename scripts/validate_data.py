"""Validate catalogue completeness, balance and source metadata.

Run this check after every manual data refresh and before evaluation or demo.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sggradmatch.data import load_programmes  # noqa: E402


def main() -> None:
    programmes = load_programmes(ROOT / "data" / "processed" / "programmes.csv")
    errors: list[str] = []
    for item in programmes:
        parsed = urlparse(item.source_url)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{item.programme_id}: invalid source URL")
        if item.university not in {"NUS", "NTU", "SMU"}:
            errors.append(f"{item.programme_id}: unexpected university")
        if not item.domains or not item.curriculum:
            errors.append(f"{item.programme_id}: missing retrieval text")
    if errors:
        raise SystemExit("\n".join(errors))
    counts = {name: sum(p.university == name for p in programmes) for name in ("NUS", "NTU", "SMU")}
    print(f"Validated {len(programmes)} programmes: {counts}")


if __name__ == "__main__":
    main()
