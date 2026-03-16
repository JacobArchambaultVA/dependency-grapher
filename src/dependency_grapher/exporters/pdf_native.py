from __future__ import annotations

import math
from pathlib import Path

from dependency_grapher.models import DependencyGraph

from .base import GraphExporter


class NativePdfExporter(GraphExporter):
    format_name = "pdf"

    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from matplotlib.patches import FancyArrowPatch
        except ImportError as exc:
            raise RuntimeError(
                "Native PDF export requires matplotlib. "
                "Install with: pip install matplotlib"
            ) from exc

        labels = {
            node_key: graph.nodes[node_key].path.name
            for node_key in graph.sorted_nodes()
        }
        root_nodes = graph.root_nodes()

        positions = _compute_positions(graph)
        if not positions:
            raise ValueError("No .csproj files were found to render.")

        xs = [pos[0] for pos in positions.values()]
        ys = [pos[1] for pos in positions.values()]
        x_span = max(xs) - min(xs) if len(xs) > 1 else 1.0
        y_span = max(ys) - min(ys) if len(ys) > 1 else 1.0

        fig_width = max(8.0, min(24.0, 4.0 + x_span * 2.5))
        fig_height = max(6.0, min(18.0, 4.0 + y_span * 1.8))
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        # Draw directed edges first so nodes render on top.
        for source, target in graph.edges():
            x1, y1 = positions[source]
            x2, y2 = positions[target]
            arrow = FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=1.2,
                color="#4B5563",
                connectionstyle="arc3,rad=0.05",
                shrinkA=16,
                shrinkB=16,
            )
            ax.add_patch(arrow)

        for node_key in graph.sorted_nodes():
            x, y = positions[node_key]
            face_color = _node_face_color(graph, node_key, root_nodes)
            ax.text(
                x,
                y,
                labels[node_key],
                ha="center",
                va="center",
                fontsize=10,
                color="#111827",
                bbox={
                    "boxstyle": "round,pad=0.4",
                    "facecolor": face_color,
                    "edgecolor": "#374151",
                    "linewidth": 1.0,
                },
                zorder=3,
            )

        margin_x = 1.0
        margin_y = 1.0
        ax.set_xlim(min(xs) - margin_x, max(xs) + margin_x)
        ax.set_ylim(min(ys) - margin_y, max(ys) + margin_y)
        ax.axis("off")
        fig.tight_layout()
        fig.savefig(output_path, format="pdf")
        plt.close(fig)


def _compute_positions(graph: DependencyGraph) -> dict[str, tuple[float, float]]:
    nodes = graph.sorted_nodes()
    indegree: dict[str, int] = {node: 0 for node in nodes}
    dependents: dict[str, set[str]] = {node: set() for node in nodes}

    for source, target in graph.edges():
        indegree[target] += 1
        dependents[source].add(target)

    queue = [node for node in nodes if indegree[node] == 0]
    topo: list[str] = []

    while queue:
        queue.sort()
        current = queue.pop(0)
        topo.append(current)
        for nxt in sorted(dependents[current]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(topo) != len(nodes):
        return _circular_positions(nodes)

    level: dict[str, int] = {node: 0 for node in nodes}
    for node in topo:
        for nxt in dependents[node]:
            level[nxt] = max(level[nxt], level[node] + 1)

    columns: dict[int, list[str]] = {}
    for node in nodes:
        columns.setdefault(level[node], []).append(node)

    positions: dict[str, tuple[float, float]] = {}
    for col in sorted(columns.keys()):
        col_nodes = sorted(columns[col])
        n = len(col_nodes)
        for i, node in enumerate(col_nodes):
            y = -(i - (n - 1) / 2.0)
            x = float(col)
            positions[node] = (x, y)

    return positions


def _circular_positions(nodes: list[str]) -> dict[str, tuple[float, float]]:
    n = len(nodes)
    if n == 0:
        return {}

    radius = max(2.0, n / 2.5)
    positions: dict[str, tuple[float, float]] = {}
    for i, node in enumerate(nodes):
        angle = (2.0 * math.pi * i) / n
        positions[node] = (radius * math.cos(angle), radius * math.sin(angle))
    return positions


def _node_face_color(graph: DependencyGraph, node_key: str, root_nodes: set[str]) -> str:
    if graph.is_test_project(node_key):
        return "#BBF7D0"
    if node_key in root_nodes:
        return "#FEF08A"
    return "#E5E7EB"
