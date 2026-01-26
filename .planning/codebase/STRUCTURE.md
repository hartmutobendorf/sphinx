# Directory Structure

## Root Directory
- `sphinx/`: Main source code package
- `tests/`: Test suite
- `doc/`: Documentation for Sphinx itself
- `utils/`: Maintainer and release scripts
- `gsd/`: "Get Shit Done" workflows (not part of package)
- `pyproject.toml`: Project configuration
- `tox.ini`: Tox configuration

## Key Source Locations (`sphinx/`)
- `application.py`: `Sphinx` class (App entry point)
- `cmd/`: Command line interface handlers (`build.py`, `quickstart.py`)
- `builders/`: Output builders (`html/__init__.py`, `latex/__init__.py`)
- `directives/`: Standard ReST directives
- `domains/`: Language support (`python.py`, `c.py`, `cpp.py`)
- `environment/`: Build environment and collectors
- `ext/`: Built-in extensions (`autodoc`, `napoleon`, `intersphinx`)
- `locale/`: Translations
- `parsers.py`: Interface for parsers (ReST, Markdown)
- `registry.py`: Component registry
- `util/`: Shared utilities
- `writers/`: Docutils writers

## Test Structure (`tests/`)
- `conftest.py`: Pytest fixtures
- `roots/`: Test data (sample documentation projects) used by tests
- `test_*.py`: Unit and integration tests
- `js/`: JavaScript tests (Jasmine)

## Documentation (`doc/`)
- `conf.py`: Sphinx configuration for its own docs
- `*.rst`: ReST source files
- `_static/`: Static assets
- `_templates/`: HTML templates
