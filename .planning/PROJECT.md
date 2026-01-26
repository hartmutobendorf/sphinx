# Sphinx D2 Plugin

## What This Is

A Sphinx extension that allows users to embed D2 (Declarative Diagramming) diagrams directly within their reStructuredText or Markdown documentation. It compiles D2 code blocks into images (SVG/PNG) during the Sphinx build process, integrating seamlessly with existing documentation workflows.

## Core Value

Seamless, zero-friction integration of D2 diagrams into Sphinx-generated documentation.

## Requirements

### Validated

- ✓ Sphinx Extension API — Core extension system functional
- ✓ Document Processing — Build pipeline (Read -> Transform -> Write) active
- ✓ Testing Infrastructure — Pytest/Tox setup available

- ✓ `.. d2::` Directive — Support parsing D2 code blocks in rst
- ✓ Diagram Rendering — invoke `d2` CLI to generate images
- ✓ Output Support — Handle HTML (SVG) and LaTeX/PDF (PDF/PNG) outputs
- ✓ Configuration — Support D2 themes and layout engines via `conf.py`

### Active

(None - fully shipped)

### Out of Scope

- Live Interactive Editor — Users write code, not drag-and-drop (v1)
- D2 Installation Management — User must provide `d2` binary (v1)

## Context

**Ecosystem**:
- Builds on Sphinx 7.x/8.x
- Requires external `d2` CLI tool installed
- Follows standard Sphinx extension patterns (similar to Graphviz or Mermaid extensions)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| External CLI | Use installed `d2` binary rather than bundling | — Pending |
| SVG Preference | Prefer SVG for web for quality/scaling | — Pending |

---
*Last updated: January 26, 2026 after initialization*
