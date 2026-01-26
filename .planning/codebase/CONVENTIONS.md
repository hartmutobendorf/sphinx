# Conventions

## Coding Style
- **Python:**
  - Follows PEP 8.
  - Enforced by `ruff` (configuration in `pyproject.toml` / `.ruff.toml`).
  - Formatting via `ruff format`.
- **Typing:**
  - Strongly typed codebase.
  - Checked by `mypy` and `pyright`.
  - Usage of `typing.TYPE_CHECKING` for circular import avoidance.
- **Imports:**
  - Sorted via `ruff` properties (isort equivalent).
  - `from __future__ import annotations` used consistently.

## Naming
- Classes: CapWords (CamelCase).
- Functions/Methods: snake_case.
- Private members: `_leading_underscore`.
- Constants: UPPER_CASE.

## Documentation
- **Docstrings:** reStructuredText format.
- **Style:** Google or Sphinx style (generally Sphinx style given it's the project itself).

## Error Handling
- Custom exceptions defined in `sphinx.errors`.
- `SphinxError` is the base class.

## Event System
- Usage of string literals for event names (e.g., `'builder-inited'`).
- Event handlers connect via `app.connect()`.
