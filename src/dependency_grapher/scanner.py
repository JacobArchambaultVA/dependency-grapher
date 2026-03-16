from __future__ import annotations

from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from .models import ProjectNode


def scan_csproj_directory(directory: Path) -> dict[str, ProjectNode]:
    directory = directory.resolve()
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    project_files = sorted(directory.rglob("*.csproj"))
    nodes: dict[str, ProjectNode] = {}
    project_references: dict[str, list[Path]] = {}

    for project_file in project_files:
        key = project_key(project_file, root=directory)
        references, is_test = parse_project_metadata(project_file)
        nodes[key] = ProjectNode(name=key, path=project_file.resolve(), is_test=is_test)
        project_references[key] = references

    path_to_key = {node.path: key for key, node in nodes.items()}

    for key, node in nodes.items():
        references = project_references[key]
        for ref in references:
            normalized = (node.path.parent / ref).resolve()
            dep_key = path_to_key.get(normalized)
            if dep_key:
                node.dependencies.add(dep_key)

    return nodes


def project_key(path: Path, root: Path) -> str:
    """Build a stable key from path relative to the scan root, without extension."""
    relative = path.resolve().relative_to(root.resolve())
    return relative.with_suffix("").as_posix()


def parse_project_references(project_file: Path) -> Iterable[Path]:
    references, _ = parse_project_metadata(project_file)
    return references


def parse_project_metadata(project_file: Path) -> tuple[list[Path], bool]:
    try:
        tree = ElementTree.parse(project_file)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Invalid XML in {project_file}: {exc}") from exc

    root = tree.getroot()
    references: list[Path] = []
    is_test = False

    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "ProjectReference":
            include = element.attrib.get("Include")
            if include:
                references.append(Path(include))
            continue

        if tag == "IsTestProject" and _to_bool(element.text):
            is_test = True
            continue

        if tag == "PackageReference":
            include = (element.attrib.get("Include") or "").strip().lower()
            if include in _TEST_PACKAGE_REFERENCES:
                is_test = True

    return references, is_test


_TEST_PACKAGE_REFERENCES = {
    "microsoft.net.test.sdk",
    "mstest.testframework",
    "mstest.testadapter",
    "xunit",
    "xunit.runner.visualstudio",
    "nunit",
    "nunit3testadapter",
    "fluentassertions",
    "coverlet.collector",
}


def _to_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"true", "1", "yes"}
