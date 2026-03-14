from __future__ import annotations

from pathlib import Path

from .models import DependencyGraph
from .scanner import scan_csproj_directory


def build_dependency_graph(directory: Path, allow_cycles: bool = False) -> DependencyGraph:
    nodes = scan_csproj_directory(directory)
    graph = DependencyGraph(nodes=nodes)

    if not allow_cycles:
        cycles = graph.detect_cycles()
        if cycles:
            formatted = "\n".join(" -> ".join(cycle) for cycle in cycles)
            raise ValueError(
                "Dependency graph contains cycles and is not a DAG:\n"
                f"{formatted}"
            )

    return graph
