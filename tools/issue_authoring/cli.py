"""Command-line interface for the validated Issue authoring workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .workflow import DraftValidationError, GithubPublisher, prepare_drafts, render_preview


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and preview AI-authored GitHub Issue drafts."
    )
    parser.add_argument("drafts", nargs="+", type=Path, help="JSON draft file(s)")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Publish after validation. Without this flag the command is read-only.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        drafts = prepare_drafts(args.drafts)
    except DraftValidationError as error:
        print(error, file=sys.stderr)
        return 2

    if not args.apply:
        print(render_preview(drafts), end="")
        return 0

    try:
        urls = GithubPublisher().publish_many(drafts)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 3
    for url in urls:
        print(f"APPLIED {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
