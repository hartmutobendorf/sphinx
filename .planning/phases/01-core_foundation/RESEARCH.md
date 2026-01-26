# Phase 1 Research: Core Foundation

## Research Findings

### 1. Directive Implementation
*   **Base Class**: `sphinx.util.docutils.SphinxDirective`.
*   **Content Access**:
    *   `self.content`: A `StringList` of the block content.
    *   `self.arguments`: List of arguments (if any).
    *   `self.options`: Dictionary of options.
*   **Minimal Structure**:
    ```python
    from sphinx.util.docutils import SphinxDirective
    from docutils import nodes

    class D2Directive(SphinxDirective):
        has_content = True
        required_arguments = 0
        optional_arguments = 0  # Or 1 if allowing filename as arg
        option_spec = {
            'file': directives.unchanged,
            'alt': directives.unchanged,
            # ... other options
        }

        def run(self):
            # Logic to handle content or file
            node = d2_node()
            # ... process content ...
            return [node]
    ```

### 2. File Option
*   **Handling**: Use `self.env.relfn2path(path)` to resolve paths relative to the source file.
*   **Duplicate Handling**: The `graphviz` extension handles both content and filename arguments. It actively checks if both are provided and warns.
*   **Implementation**:
    ```python
    if 'file' in self.options:
        rel_filename, filename = self.env.relfn2path(self.options['file'])
        self.env.note_dependency(rel_filename)
        # Read file content...
    ```

### 3. Subprocess Safety
*   **Pattern**: Use `subprocess.run` with a list of arguments to avoid shell injection.
*   **Standard Practice**:
    ```python
    import subprocess
    cmd = ['d2', '-', '-'] # Read from stdin, write to stdout (or temp file)
    try:
        ret = subprocess.run(
            cmd,
            input=self.content.encode(),
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        # Handle error
    except OSError:
        # Handle d2 missing
    ```
*   **Config**: Allow configuring `d2` executable path via `app.add_config_value`.

### 4. SVG Embedding
*   **Sphinx Standard**: The `graphviz` extension uses `nodes.figure` simply wrapping a custom node `graphviz` which is then visited by specific translators.
*   **HTML Output**:
    *   `graphviz` extension manually appends HTML in `html_visit_graphviz`.
    *   It uses `<object data="..." type="image/svg+xml">` for SVGs. This is generally preferred over `<img>` for SVGs if interaction or styling is needed, though `<img>` is safer and simpler for static images.
    *   Since D2 generates static diagrams (mostly), `<img>` might be sufficient, but `<object>` or inline `<svg>` (using `nodes.raw`) allows for better CSS integration if D2 exports classes.
    *   **Recommendation**: Follow `graphviz` pattern: Generate the file to `_images` (or build dir), then link it.
*   **Mechanism**:
    1.  Directive returns a custom `d2` node containing the code.
    2.  Register a `html_visit_d2` function.
    3.  In the visitor, run `d2` to generate the SVG file in the output directory.
    4.  Generate `<object>` or `<img>` tag pointing to that file.

### 5. Extension Setup
*   **Boilerplate**:
    ```python
    def setup(app):
        app.add_directive('d2', D2Directive)
        app.add_node(d2_node, html=(html_visit_d2, None))
        app.add_config_value('d2_command', 'd2', 'env')
        # ...
        return {'version': '0.1', 'parallel_read_safe': True}
    ```

## Recommended Implementation Strategy

1.  **Define Extension Structure**:
    *   Create a module (e.g., `sphinxcontrib.d2` or inside local source).
    *   Define `D2Error` exception.

2.  **Create Directive (`D2Directive`)**:
    *   Inputs: D2 code buffer OR `file` option.
    *   Logic:
        *   Validate options.
        *   Resolve file path if `file` option used.
        *   Create a custom `d2_node` storing the D2 source code and options.

3.  **Implement Builder/Visitor Logic**:
    *   Create `render_d2` function:
        *   Check for `d2` executable.
        *   Compute hash of content to use as filename (caching).
        *   Run `subprocess.run(['d2', ...])`.
        *   Return output filename.
    *   Create `html_visit_d2`:
        *   Call `render_d2` to get SVG path.
        *   Embed using `<object>` tag (consistent with Graphviz).

4.  **Configuration**:
    *   `d2_command`: Path to d2 binary.
    *   `d2_api_options`: List of allowed options (if we want to restrict).

5.  **Fail Safe**:
    *   Wrap subprocess calls in `try/except`.
    *   If `d2` missing, warn and potentially skip node or render error message in place.

