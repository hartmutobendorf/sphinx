# Integrations

## Internal Dependencies
- **Docutils**: The core foundation. Sphinx builds heavily on Docutils nodes, parsers, readers, and writers.
- **Jinja2**: Used for all HTML templating.
- **Pygments**: Used for code block syntax highlighting.

## External Services
- **ReadTheDocs**: While not a code dependency, Sphinx is the primary engine for RTD, and configuration often considers RTD environments.
- **PyPI**: Distribution.

## Plugins/Extensions
Sphinx has a massive ecosystem of extensions.
- **Built-in (`sphinx.ext`)**:
    - `autodoc`: Generate docs from docstrings.
    - `intersphinx`: Link to other Sphinx projects.
    - `napoleon`: Support Google/NumPy style docstrings.
    - `graphviz`, `mathjax`, `viewcode`, etc.
- **Third-party**: Configuration typically involves adding packages to the `extensions` list in `conf.py`.
