from __future__ import annotations

from pathlib import Path

from dependency_grapher.models import DependencyGraph

from .base import GraphExporter


class DotExporter(GraphExporter):
    format_name = "dot"

    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        lines = ["digraph Dependencies {", "  rankdir=LR;"]

        for node_key in graph.sorted_nodes():
            lines.append(f'  "{node_key}";')

        for source, target in graph.edges():
            lines.append(f'  "{source}" -> "{target}";')

        lines.append("}")
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
