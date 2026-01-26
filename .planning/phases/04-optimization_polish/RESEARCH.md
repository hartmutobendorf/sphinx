# Phase 4: Optimization & Polish - Research

## Context
This phase focuses on optimizing the `sphinxcontrib-d2` extension and adding polish features like caching, proper figure handling, and accessibility options (alt text).

## 1. Caching Strategy
To avoid unnecessary re-rendering of D2 diagrams, we need a robust caching strategy that generates a unique hash for each diagram configuration.

### Inputs for Hashing
The hash should depend on everything that affects the output image. If any of these change, the diagram must be re-rendered.

*   **Code Content**: The D2 code itself (`full_code` which includes `d2_config` content).
*   **D2 Command**: The executable path (`d2_cmd`). If the user switches D2 versions/executables, we should re-render.
*   **Options**: The directive options (e.g., `theme`, `layout` if supported in future).
*   **Builder Config**: 
    *   `d2_font`
    *   `d2_mono_font`
*   **Output Format**: `svg` or `pdf`.

### Implementation Location
The check should happen in `render_d2`.

```python
# Proposed Hash Construction
hashopts = (
    full_code + 
    str(options) + 
    str(d2_cmd) + 
    str(self.builder.config.d2_font) + 
    str(self.builder.config.d2_mono_font) + 
    format
)
hashed = hashlib.sha1(hashopts.encode('utf-8')).hexdigest()
```

### Verification
*   Current implementation checks `os.path.exists(output_path)`.
*   This logic remains valid: calculate hash -> determine filename -> if file exists, skip generation.

## 2. Figure Integration
Sphinx standardizes how figures with captions are handled. `sphinx.ext.graphviz` provides a reference implementation.

### D2Directive.run logic
If the `caption` option is present, we should wrap the `d2_node` in a `nodes.figure`.

**Structure:**
*   **Without Caption**: Returns `[d2_node]`.
*   **With Caption**: Returns `[nodes.figure]`.
    *   `nodes.figure` contains:
        1.  `d2_node`
        2.  `nodes.caption` (containing parsed caption text)

### Implementation Detail
Reference `sphinx.ext.graphviz.figure_wrapper`:
1.  Create `nodes.figure`.
2.  Move `align` attribute from `d2_node` to `figure` (if we support `align`).
3.  Parse caption text into `nodes.caption`.
4.  Add `d2_node` and `caption` to `figure`.

```python
# Pseudo-code update for D2Directive.run
if 'caption' not in self.options:
    self.add_name(node)
    return [node]
else:
    figure = figure_wrapper(self, node, self.options['caption'])
    self.add_name(figure)
    return [figure]
```

## 3. Alt Text
For accessibility, the `alt` option should be passed to the HTML output.

### Data Flow
1.  **Directive**: User provides `.. d2:: ... :alt: My Diagram`.
2.  **Node Creation**: `node['alt']` attribute should be set in `D2Directive.run`.
    *   Currently, D2Directive sets `node['options'] = self.options`.
    *   We should explicitly set `node['alt'] = self.options.get('alt')`.
3.  **HTML Visitor**: `html_visit_d2` retrieves `alt`.
    *   `node.get('alt', '')` works correctly if `node['alt']` is set.
    *   Current code uses `node.get('alt', '')` inside `make_img`.

### Action Item
Update `D2Directive.run` to explicitly copy `alt` from options to the node attribute:
```python
if 'alt' in self.options:
    node['alt'] = self.options['alt']
```

## Summary of Changes
1.  **`sphinxcontrib/d2/__init__.py`**:
    *   Update `render_d2` to include `options` and `d2_cmd` in hash.
    *   Update `D2Directive.run` to handle `caption` by wrapping in `nodes.figure`.
    *   Update `D2Directive.run` to set `node['alt']`.
    *   (Helper) Add `figure_wrapper` function (adapted from graphviz).
