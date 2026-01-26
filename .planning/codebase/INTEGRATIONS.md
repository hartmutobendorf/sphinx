# Integrations

## External Services
- **PyPI:** Package distribution (Project name "Sphinx")
- **GitHub:** Source control and issue tracking
- **ReadTheDocs:** Documentation hosting (detected via `READTHEDOCS` env var in `tox.ini`)

## External APIs
- **Requests:** Used for link checking and other HTTP interactions (`sphinx.util.requests`)

## System Integrations
- **TeX Live:** Required for LaTeX PDF output (managed via `bindep` and system package managers like `rpm`, `dpkg`)
- **Graphviz:** Optional dependency for graphing (often used with `sphinx.ext.graphviz`)
- **ImageMagick:** Optional for image conversion (implied by `sphinx.ext.imgconverter`)

## Package Managers
- **pip/flit:** Python package management
- **npm:** JavaScript dependency management (for testing and themes)
