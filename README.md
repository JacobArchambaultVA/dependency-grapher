# dependency-grapher

Generates a project dependency graph from `.csproj` files found in one directory.

## Highlights

- Scans only one directory for `*.csproj` files.
- Builds an internal graph model first (format-agnostic).
- Exports via pluggable exporters (`pdf`, `pdf-native`, `dot`, `json`).
- Validates the graph as a DAG by default.

## Requirements

- Python 3.10+
- `matplotlib` for native PDF rendering (Graphviz-free)
- Optional: Graphviz installed and available on `PATH` for higher quality `dot` layout in `--format pdf`

## Install

```bash
pip install -e .
```

If you only want native PDF rendering (no Graphviz), this is sufficient.

## Usage

```bash
dependency-grapher <directory-with-csproj> --format pdf --output graph.pdf
```

Examples:

```bash
# Default output is dependency-graph.pdf in current directory
dependency-grapher ./src/MySolution

# DOT output
dependency-grapher ./src/MySolution --format dot --output graph.dot

# JSON output
dependency-grapher ./src/MySolution --format json --output graph.json

# Force pure-Python PDF rendering (no Graphviz)
dependency-grapher ./src/MySolution --format pdf-native --output graph.pdf

# Allow cyclic graphs (skips DAG validation)
dependency-grapher ./src/MySolution --allow-cycles
```

## PDF Behavior

- `--format pdf`: tries Graphviz `dot` first, then automatically falls back to native matplotlib rendering if Graphviz is unavailable.
- `--format pdf-native`: always uses native matplotlib rendering.

## Extending Output Formats

Add a new exporter implementing `GraphExporter` in `src/dependency_grapher/exporters/`, then register it in `registry.py`.
