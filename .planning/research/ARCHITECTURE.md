# Architecture: Read-Transform-Write Pipeline

The architecture follows the standard Sphinx extension lifecycle for image generation logic.

## 1. Parsing Phase (The Directive)
- **Class**: `D2Directive(SphinxDirective)`
- **Action**: 
  - Reads the D2 code from the directive content OR reads the external file specified as an argument.
  - If reading an external file, register it as a dependency in `env.note_dependency` so Sphinx rebuilds if the file changes.
  - Creates a `d2_node` (custom node).
  - Stores the code, options, and file paths on the node attributes.
- **Output**: The doctree contains `d2_node` instances.

## 2. Transformation/Resolution Phase (The Transform)
*Note: Often this logic is placed in the Writer/Visitor methods or a post-transform.*

For simplicity and caching, use **`sphinx.ext.graphviz` approach**:
- Keep `d2_node` in the tree until the Writer visits it.
- **OR** use a `PostTransform` to generate images before writing. The standard approach is usually to handle generation in the node visitor method (`visit_d2_node`).

## 3. Rendering Logic (Image Generation)
This is the heavy lifting, usually encapsulated in a helper function `render_d2(self, code, options, format, prefix)`.

**Steps**:
1.  **Hash Calculation**: Compute SHA1 of the (D2 code + options).
2.  **Cache Check**: Check `_build/doctrees/...` or specific output dir. If a file with `hash.fmt` exists, skip generation.
3.  **File Generation**:
    - Write D2 code to a temp file (if needed by CLI) or pipe via stdin.
    - Invoke `subprocess.run(['d2', ...])`.
    - Arguments: output file path.
4.  **Error Handling**: If `d2` returns exit code != 0, raise `D2Error` and log warning.

## 4. Writing Phase (The Builder)
- **HTML Builder**:
  - `visit_d2_node`: Calls `render_d2` -> returns filename.
  - Replaces `d2_node` context with an `<img>` tag or `<object>` (for SVG) pointing to the generated asset.
- **LaTeX Builder**:
  - `visit_d2_node`: Calls `render_d2` (preferring PDF/PNG).
  - Generates `\includegraphics{...}`.

## Directory Structure
- Generated images should go into `_images/` in the output directory.
- Sphinx `builder.images` API handles copying/tracking these assets.
