from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dependency_grapher.builder import build_dependency_graph
from dependency_grapher.exporters import get_exporter


def default_extension(format_name: str) -> str:
    extension_map = {
        "pdf": "pdf",
        "pdf-native": "pdf",
        "dot": "dot",
        "json": "json",
    }
    return extension_map.get(format_name, format_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a dependency graph from .csproj files under a directory (recursive)."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Root directory to recursively scan for .csproj files.",
    )
    parser.add_argument(
        "--format",
        choices=["pdf", "pdf-native", "dot", "json"],
        default="pdf",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file path. Defaults to dependency-graph.<extension> in the current working directory.",
    )
    parser.add_argument(
        "--allow-cycles",
        action="store_true",
        help="Allow cyclic dependencies instead of enforcing DAG validation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        extension = default_extension(args.format)
        output_path = args.output or (Path.cwd() / f"dependency-graph.{extension}")
        output_path = output_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        graph = build_dependency_graph(args.directory, allow_cycles=args.allow_cycles)
        exporter = get_exporter(args.format)
        exporter.export(graph, output_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Generated {args.format.upper()} graph at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
