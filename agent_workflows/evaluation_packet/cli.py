"""CLI adapter for external AI evaluation packet build and verification."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .workflow import (
    GitSourceReader,
    PacketValidationError,
    build_packet_plan,
    render_plan,
    verify_packet,
    write_packet,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify evaluation packets.")
    commands = parser.add_subparsers(dest="command", required=True)

    build = commands.add_parser("build", help="Validate and preview a packet spec.")
    build.add_argument("spec", type=Path)
    build.add_argument("--repo-root", type=Path, default=Path.cwd())
    build.add_argument("--output-root", type=Path, default=Path("evaluation_packets"))
    build.add_argument(
        "--apply",
        action="store_true",
        help="Write the immutable packet. Without this flag the command is read-only.",
    )

    verify = commands.add_parser("verify", help="Verify a packet manifest and hashes.")
    verify.add_argument("packet", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "verify":
            manifest = verify_packet(args.packet)
            print(
                f"VERIFIED {args.packet} commit={manifest['source_commit']} "
                f"files={len(manifest['files']) + 1}"
            )
            return 0

        plan = build_packet_plan(args.spec, GitSourceReader(args.repo_root))
        print(render_plan(plan), end="")
        if not args.apply:
            return 0
        target = write_packet(plan, args.output_root)
        print(f"BUILT {target}")
        return 0
    except (PacketValidationError, FileExistsError, RuntimeError) as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
