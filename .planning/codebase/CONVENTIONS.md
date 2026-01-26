# Code Conventions

## Python
- **Style Guide**: Follows PEP 8.
- **Linting**: Enforced by `ruff`.
- **Formatting**: Enforced by `ruff format`.
- **Type Hinting**: Extensive use of type hints (`typing` module, `__future__.annotations`). Checked with `mypy` and `pyright`.
- **Imports**: Sorted and organized.
- **Docstrings**: Sphinx-style reST docstrings are used for API documentation.

## JavaScript
- **Formatting**: Enforced by `prettier`.

## Documentation
- Written in reStructuredText (rst).
- Self-hosted in the `doc/` directory.

## Testing
- Tests are located in `tests/`.
- Heavy reliance on `pytest` fixtures.
- Test files generally correspond to module names (e.g., `test_application.py` tests `application.py`).
- "Roots" pattern: `tests/roots/` contains minimal Sphinx projects used as input for functional tests.
