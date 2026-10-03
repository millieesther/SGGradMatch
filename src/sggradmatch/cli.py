"""Command-line interface for loading one profile and printing recommendations.

The CLI exposes the same pipeline as the web demo and supports both the
rule-only baseline and hybrid ranking method.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import recommend


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Recommend selected Singapore master's programmes")
    command.add_argument("profile", type=Path, help="Path to a student-profile JSON file")
    command.add_argument("--method", choices=["rule", "hybrid"], default="hybrid")
    command.add_argument("--use-openai", action="store_true")
    command.add_argument("--programmes", default=None)
    return command


def main() -> None:
    args = parser().parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    result = recommend(
        profile,
        method=args.method,
        use_openai=args.use_openai,
        programme_path=args.programmes,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
