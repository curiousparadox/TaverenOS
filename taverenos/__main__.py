from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .processor import parse_export, to_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert ChatGPT exports to Obsidian notes")
    parser.add_argument("input", help="Path to text or JSON export. Use '-' for stdin")
    parser.add_argument("--output", "-o", default="vault", help="Obsidian vault directory")
    parser.add_argument("--thread", default="default", help="Thread identifier")
    args = parser.parse_args(argv)

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(args.input).read_text()

    messages = parse_export(raw)
    output_path = to_markdown(messages, Path(args.output), args.thread)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
