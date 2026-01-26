# Tech Stack

## Core Technologies
- **Language:** Python 3.12+
- **Secondary:** JavaScript (for themes and search)
- **Runtime:** CPython, PyPy
- **Build System:** Flit (`flit_core`)

## Key Libraries & Dependencies
- **Core:**
  - `docutils` (>=0.21, <0.23): Parsing and document model
  - `Jinja2` (>=3.1): Templating
  - `Pygments` (>=2.17): Syntax highlighting
  - `babel` (>=2.13): Internationalization
  - `alabaster` (>=0.7.14): Default theme
  - `imagesize`: Image handling
  - `snowballstemmer`: Search stemming
  - `requests`: HTTP requests
  - `packaging`: Version handling

- **Development:**
  - `tox`: Test environment management
  - `pytest`: Testing framework
  - `ruff`: Linting and formatting
  - `mypy`: Static type checking
  - `bindep`: Binary dependency handling

## Configuration
- **Project:** `pyproject.toml` (PEP 621 metadata, tool configs)
- **Tox:** `tox.ini` (test environments)
- **Linting:** `.ruff.toml` (if exists, implied by grep) or in `pyproject.toml`
- **Docs:** `doc/conf.py`

## Infrastructure
- **CI/CD:** GitHub Actions (implied)
- **Docs Hosting:** ReadTheDocs (implied by tox env)
