# dependency-grapher

Generates a project dependency graph from `.csproj` files found under a directory (recursive).

## Highlights

- Recursively scans subdirectories for `*.csproj` files.
- Builds an internal graph model first (format-agnostic).
- Exports via pluggable exporters (`pdf`, `dot`, `json`).
- Validates the graph as a DAG by default.

Node IDs are based on paths relative to the scan root (without `.csproj`) so same-named projects in different folders are handled correctly.

## Requirements

- Python 3.10+
- `matplotlib` for PDF rendering

## Install

Create and activate a local virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Git Bash on Windows
```

PowerShell alternative:

```powershell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -e .
```

## Usage

```bash
dependency-grapher <directory-with-csproj> --format pdf --output graph.pdf
```

When `--output` is omitted, the default filename is based on output extension (for example, `pdf` defaults to `dependency-graph.pdf`).

Examples:

```bash
# Default output is dependency-graph.pdf in current directory
dependency-grapher ./src/MySolution

# DOT output
dependency-grapher ./src/MySolution --format dot --output graph.dot

# JSON output
dependency-grapher ./src/MySolution --format json --output graph.json

# Native matplotlib PDF rendering
dependency-grapher ./src/MySolution --format pdf --output graph.pdf

# Allow cyclic graphs (skips DAG validation)
dependency-grapher ./src/MySolution --allow-cycles

# Example generating a series of PDF graphs for a set of repos
for repo in ../*ped-services*/; do   [ -d "$repo" ] || continue;   name="$(basename "$repo")";   dependency-grapher "$repo" --format pdf --output "${name}.pdf"; done

# Example merging a series of generated PDF graphs in a folder, e.g., from the output of the command immediately above
python -m pip install -q pypdf && python -c "from pypdf import PdfWriter; import glob,sys; files=sorted(glob.glob('*.pdf')); sys.exit('No PDF files found') if not files else None; w=PdfWriter(); [w.append(f) for f in files]; w.write('merged.pdf'); print(f'Merged {len(files)} files into merged.pdf')"
```


## PDF Behavior

- `--format pdf`: uses native matplotlib rendering.

## Extending Output Formats

Add a new exporter implementing `GraphExporter` in `src/dependency_grapher/exporters/`, then register it in `registry.py`.
