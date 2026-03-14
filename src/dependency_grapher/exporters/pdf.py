from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from dependency_grapher.models import DependencyGraph

from .base import GraphExporter
from .dot import DotExporter
from .pdf_native import NativePdfExporter


class PdfExporter(GraphExporter):
    format_name = "pdf"

    def export(self, graph: DependencyGraph, output_path: Path) -> None:
        dot_exporter = DotExporter()
        native_exporter = NativePdfExporter()

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as temp_file:
            dot_path = Path(temp_file.name)

        try:
            dot_exporter.export(graph, dot_path)
            try:
                completed = subprocess.run(
                    ["dot", "-Tpdf", str(dot_path), "-o", str(output_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
            except FileNotFoundError as exc:
                # Gracefully fallback to a pure-Python renderer.
                native_exporter.export(graph, output_path)
                return

            if completed.returncode != 0:
                native_exporter.export(graph, output_path)
                return
        finally:
            if dot_path.exists():
                dot_path.unlink()
