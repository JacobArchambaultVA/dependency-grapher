from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from dependency_grapher.models import DependencyGraph


class GraphExporter(ABC):
    format_name: str

    @abstractmethod
    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        raise NotImplementedError
