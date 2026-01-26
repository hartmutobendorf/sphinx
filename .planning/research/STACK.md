# Sphinx Extension Stack Research

## Core APIs
To build a D2 diagram extension, we need to interact with the following core Sphinx and Docutils APIs:

### 1. Application API (`sphinx.application`)
The entry point `setup(app)` function uses this API to register the extension components.
- `app.add_directive(name, cls)`: Registers the `.. d2::` reStructuredText directive.
- `app.add_node(node, html=(visit, depart), latex=(...))`: Registers a custom Docutils node to represent the D2 diagram in the internal document tree (doctree).
- `app.add_config_value(name, default, rebuild)`: Registers configuration options in `conf.py` (e.g., `d2_command`, `d2_graph_attributes`).
- `app.connect(event, callback)`: Crucial for hooking into build phases (e.g., `builder-inited` check that D2 is installed).

### 2. Docutils Nodes (`docutils.nodes`)
We will need to define a custom node (e.g., `d2_node`) that inherits from `docutils.nodes.Element` or `General`.
- During the **Parsing** phase, the directive produces this custom node containing the D2 code.
- During the **Resolution/Writing** phase, this node is transformed into a standard `docutils.nodes.image` node referencing the generated output file.

### 3. Directives (`docutils.parsers.rst.Directive`)
The class handling the parsing of the RST block.
- `run()` method processes the content.
- `option_spec` defines valid options like `:format:`, `:caption:`, etc.
- `has_content = True` allows inline D2 code.
- Arguments can be used to pass a filename instead of inline code.

## External CLI Invocation
Interacting with the `d2` binary requires robust subprocess handling.
- **Library**: `subprocess` standard library.
- **Safety**: Avoid `shell=True` to prevent injection vulnerabilities. Use list arguments `['d2', 'args', ...]`.
- **Environment**: Ensure the subprocess inherits necessary environment variables (PATH) to find the binary.
- **Error Handling**: Capture `stderr` to display D2 compilation errors as Sphinx warnings (`logger.warning`).

## Relevant Existing Extensions
- `sphinx.ext.graphviz`: The gold standard template for this. It handles code-to-image conversion, caching, and multiple output formats.
- `sphinxcontrib-mermaid`: Another similar example using an external CLI (mmdc).
