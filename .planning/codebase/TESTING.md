# Testing Strategy

## Frameworks
- **Python**: `pytest`
- **JavaScript**: `jasmine` (via `jasmine-browser-runner`)
- **Orchestration**: `tox`

## Test Organization
- **Unit Tests**: Test individual components (parsers, utils).
- **Integration/Functional Tests**: Most tests involve running a minimal Sphinx build.
    - Located in `tests/`.
    - Use `tests/roots/test-*` directories as sample input projects.
    - The `app` fixture (from `sphinx.testing.fixtures`) is central. It creates a temporary Sphinx application instance pointing to a test root.

## Running Tests
- **All envs**: `tox`
- **Specific env**: `tox -e py312`
- **Directly (dev)**: `pytest` (requires dependencies installed in current env).
- **Linting**: `tox -e lint` or `tox -e ruff`.

## Key Fixtures
- `app`: Provides a `SphinxTestApp` instance.
- `rootdir`: Path to the directory containing test roots.
- `make_app`: Factory to create apps with specific configs.
