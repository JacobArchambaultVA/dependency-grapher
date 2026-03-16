from __future__ import annotations

from pathlib import Path

from dependency_grapher.models import DependencyGraph

from .base import GraphExporter


class DotExporter(GraphExporter):
    format_name = "dot"

    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        lines = ["digraph Dependencies {", "  rankdir=LR;"]

        for node_key in graph.sorted_nodes():
            label = graph.nodes[node_key].path.name.replace('"', r'\"')
            lines.append(f'  "{label}" ;')

        for source, target in graph.edges():
            source_label = graph.nodes[source].path.name.replace('"', r'\"')
            target_label = graph.nodes[target].path.name.replace('"', r'\"')
            lines.append(f'  "{source_label}" -> "{target_label}";')

        lines.append("}")
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
