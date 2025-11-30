"""Command-line interface for the Argos toolkit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable

from argos import __version__


@dataclass(frozen=True)
class ArgosInfo:
    """Simple container for Argos metadata."""

    name: str
    version: str
    description: str


DEFAULT_DESCRIPTION = "Argos is a lightweight toolkit starter."
DEFAULT_INFO = ArgosInfo(name="Argos", version=__version__, description=DEFAULT_DESCRIPTION)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=DEFAULT_DESCRIPTION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello = subparsers.add_parser("hello", help="Print a friendly greeting.")
    hello.add_argument("--name", help="Optional person or team to greet.")

    subparsers.add_parser("info", help="Display Argos metadata.")

    return parser


def format_greeting(name: str | None = None) -> str:
    audience = name or "there"
    return f"Hello, {audience}! Welcome to Argos."


def format_info(info: ArgosInfo = DEFAULT_INFO) -> str:
    return f"{info.name} v{info.version} — {info.description}"


def handle_args(args: argparse.Namespace) -> str:
    if args.command == "hello":
        return format_greeting(args.name)
    if args.command == "info":
        return format_info()
    raise ValueError(f"Unknown command: {args.command}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    output = handle_args(args)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
