from __future__ import annotations

from dependency_grapher.exporters.base import GraphExporter
from dependency_grapher.exporters.dot import DotExporter
from dependency_grapher.exporters.json_exporter import JsonExporter
from dependency_grapher.exporters.pdf_native import NativePdfExporter


def get_exporter(format_name: str) -> GraphExporter:
    native_pdf = NativePdfExporter()
    exporters: dict[str, GraphExporter] = {
        DotExporter.format_name: DotExporter(),
        JsonExporter.format_name: JsonExporter(),
        "pdf": native_pdf,
        NativePdfExporter.format_name: native_pdf,
    }

    try:
        return exporters[format_name.lower()]
    except KeyError as exc:
        supported = ", ".join(sorted(exporters.keys()))
        raise ValueError(
            f"Unsupported output format '{format_name}'. Supported: {supported}"
        ) from exc
