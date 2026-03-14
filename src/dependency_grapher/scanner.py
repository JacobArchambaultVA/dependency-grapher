from __future__ import annotations

from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from .models import ProjectNode


def scan_csproj_directory(directory: Path) -> dict[str, ProjectNode]:
    directory = directory.resolve()
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    project_files = sorted(directory.glob("*.csproj"))
    nodes: dict[str, ProjectNode] = {}

    for project_file in project_files:
        key = project_key(project_file)
        nodes[key] = ProjectNode(name=key, path=project_file.resolve())

    path_to_key = {node.path: key for key, node in nodes.items()}

    for key, node in nodes.items():
        references = parse_project_references(node.path)
        for ref in references:
            normalized = (node.path.parent / ref).resolve()
            dep_key = path_to_key.get(normalized)
            if dep_key:
                node.dependencies.add(dep_key)

    return nodes


def project_key(path: Path) -> str:
    return path.stem


def parse_project_references(project_file: Path) -> Iterable[Path]:
    try:
        tree = ElementTree.parse(project_file)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Invalid XML in {project_file}: {exc}") from exc

    root = tree.getroot()
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag != "ProjectReference":
            continue

        include = element.attrib.get("Include")
        if include:
            yield Path(include)
