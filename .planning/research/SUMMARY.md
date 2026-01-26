# Research Summary: Sphinx D2 Plugin

## Overview
This research establishes the requirements and architecture for a Sphinx extension that embeds D2 diagrams. The extension mirrors the functionality of `sphinx.ext.graphviz` but targets the modern D2 declarative diagramming language.

## Key Findings

### 1. Technology Stack
- **Language**: Python (Sphinx Extension API).
- **Core Dependency**: `d2` binary (must be installed by user).
- **Python libraries**: `subprocess` for execution, `hashlib` for caching.

### 2. Primary Features
- **Directive**: `.. d2::` supporting inline code and external files.
- **Functionality**:
  - Output formats: SVG (web), PNG/PDF (print).
  - Support for D2 themes and layout engines.
  - Standard figure features: caption, alt text, alignment.
- **Configuration**: Global `conf.py` settings for command path and defaults.

### 3. Architecture Strategy
1.  **Parse**: `D2Directive` creates a custom `d2_node` containing the code.
2.  **External File Tracking**: Use `env.note_dependency` for file inclusions.
3.  **Transform/Write**: Lazy evaluation.
    - Calculate SHA1 hash of content + options.
    - Check cache to avoid re-running D2 (crucial for performance).
    - If new, run `d2` via `subprocess` (no `shell=True`).
    - Replace `d2_node` with standard `image` node pointing to the artifact.

### 4. Critical Risks & Mitigation
- **Performance**: Solved via content hashing/caching.
- **Dependencies**: Must fail explicitly and clearly if `d2` binary is missing.
- **Security**: Strict `subprocess` usage (list args) to prevent shell injection.
- **OS Support**: Use `pathlib` for agnostic path handling.

## Next Steps
1.  Scaffold the Python package structure (`sphinxcontrib-d2` or similar).
2.  Implement the `setup` function and `D2Directive`.
3.  Implement the rendering logic with `subprocess` and caching.
4.  Add unit tests mocking the `d2` CLI.
