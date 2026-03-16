# dependency-grapher

Generates a project dependency graph from `.csproj` files found under a directory (recursive).

## Highlights

- Recursively scans subdirectories for `*.csproj` files.
- Builds an internal graph model first (format-agnostic).
- Exports via pluggable exporters (`pdf`, `pdf-native`, `dot`, `json`).
- Validates the graph as a DAG by default.

Node IDs are based on paths relative to the scan root (without `.csproj`) so same-named projects in different folders are handled correctly.

## Requirements

- Python 3.10+
- `matplotlib` for PDF rendering

## Install

```bash
pip install -e .
```

If you only want native PDF rendering (no Graphviz), this is sufficient.

## Usage

```bash
dependency-grapher <directory-with-csproj> --format pdf --output graph.pdf
```

When `--output` is omitted, the default filename is based on output extension (for example, both `pdf` and `pdf-native` default to `dependency-graph.pdf`).

Examples:

```bash
# Default output is dependency-graph.pdf in current directory
dependency-grapher ./src/MySolution

# DOT output
dependency-grapher ./src/MySolution --format dot --output graph.dot

# JSON output
dependency-grapher ./src/MySolution --format json --output graph.json

# Native matplotlib PDF rendering
dependency-grapher ./src/MySolution --format pdf-native --output graph.pdf

# Allow cyclic graphs (skips DAG validation)
dependency-grapher ./src/MySolution --allow-cycles

# Example generating a series of PDF graphs for a set of repos
for repo in ../*ped-services*/; do   [ -d "$repo" ] || continue;   name="$(basename "$repo")";   dependency-grapher "$repo" --format pdf-native --output "${name}.pdf"; done
```


## PDF Behavior

- `--format pdf`: uses native matplotlib rendering.
- `--format pdf-native`: alias for native matplotlib rendering.

## Extending Output Formats

Add a new exporter implementing `GraphExporter` in `src/dependency_grapher/exporters/`, then register it in `registry.py`.
