from __future__ import annotations

import json
from pathlib import Path

from dependency_grapher.models import DependencyGraph

from .base import GraphExporter


class JsonExporter(GraphExporter):
    format_name = "json"

    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        payload = {
            "nodes": [
                {
                    "id": key,
                    "path": str(graph.nodes[key].path),
                }
                for key in graph.sorted_nodes()
            ],
            "edges": [
                {"from": source, "to": target}
                for source, target in graph.edges()
            ],
        }

        output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
