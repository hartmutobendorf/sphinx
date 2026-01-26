# Testing

## Framework
- **Runner:** `pytest`
- **Orchestrator:** `tox` (supports multiple python versions `py312`...`py315`).

## Structure
- **Unit Tests:** Located in `tests/`. Names generally mirror source file names (e.g., `test_application.py` tests `sphinx/application.py`).
- **Integration Tests:** Many tests operate by running a mini-Sphinx build against a sample "root" directory located in `tests/roots/`.
- **Fixtures:** Extensive usage of `pytest` fixtures, specifically `app` fixture which provides a `SphinxTestApp` instance.

## JavaScript Testing
- **Runner:** `jasmine-browser-runner`
- **Config:** `tests/js/jasmine-browser.mjs`
- **Command:** `npm run test`

## Continuous Integration
- Linting (`ruff`, `mypy`, `pyright`) runs as a separate tox environment.
- Documentation building is also tested (`tox -e docs`).
- Binary dependencies checked via `bindep` (`tox -e bindep`).

## Coverage
- `pytest-cov` is likely used (implied standard practice, though not explicitly seen in snippets).
