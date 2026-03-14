from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Set


@dataclass(slots=True)
class ProjectNode:
    name: str
    path: Path
    dependencies: Set[str] = field(default_factory=set)


@dataclass(slots=True)
class DependencyGraph:
    nodes: Dict[str, ProjectNode]

    def edges(self) -> Iterable[tuple[str, str]]:
        for source, node in self.nodes.items():
            for target in sorted(node.dependencies):
                if target in self.nodes:
                    yield source, target

    def sorted_nodes(self) -> list[str]:
        return sorted(self.nodes.keys())

    def detect_cycles(self) -> list[list[str]]:
        visited: set[str] = set()
        stack: set[str] = set()
        path: list[str] = []
        cycles: list[list[str]] = []

        def dfs(node: str) -> None:
            visited.add(node)
            stack.add(node)
            path.append(node)

            for dep in self.nodes[node].dependencies:
                if dep not in self.nodes:
                    continue
                if dep not in visited:
                    dfs(dep)
                elif dep in stack:
                    try:
                        start = path.index(dep)
                    except ValueError:
                        start = 0
                    cycles.append(path[start:] + [dep])

            stack.remove(node)
            path.pop()

        for node in self.sorted_nodes():
            if node not in visited:
                dfs(node)

        return cycles
