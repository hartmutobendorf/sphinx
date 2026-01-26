# Phase 3: Print Support Research

## Findings

### 1. D2 Formats
*   **Native PDF Support**: Yes, `d2` supports PDF export natively.
    *   Command: `d2 input.d2 output.pdf`
    *   Verification: Successfully ran `d2 - test_output.pdf` in the current environment.
*   **Dependencies**: The current environment has a `d2` binary that supports PDF export. No additional Python dependencies (like Playwright wrappers) seem necessary for the plugin itself, relying on the external `d2` tool.

### 2. Sphinx LaTeX
*   **Image Embedding**: Sphinx's LaTeX writer uses `\sphinxincludegraphics`.
    *   Reference: `sphinx.writers.latex.LaTeXWriter.visit_image`
    *   The command generated is typically: `\sphinxincludegraphics[options]{{base_filename}{extension}}`.
*   **Strategy**:
    *   Generate a `.pdf` file using `d2`.
    *   Use `\sphinxincludegraphics` to include the generated PDF.
    *   LaTeX usually handles PDF images well via `graphicx` (which Sphinx uses).

### 3. Visitor Logic
*   **Current State**: `render_d2` hardcodes `.svg` output and generates both light and dark variants.
*   **New Logic (`latex_visit_d2`)**:
    *   Needs to generate a single PDF (likely "light" theme or configurable).
    *   Needs to output LaTeX code instead of HTML `<img>` tags.
    *   Code Structure:
        ```python
        def latex_visit_d2(self, node):
            # Render PDF
            fname = render_d2_pdf(self, node['code'], node['options'])
            # Generate LaTeX
            cmd = r'\sphinxincludegraphics{%s}' % fname
            self.body.append(cmd)
        ```
*   **Refactoring**:
    *   Option A: Extend `render_d2` to handle formats.
    *   Option B: Create specific `render_d2_pdf` helper.
    *   Given the existing `render_d2` is tied to generating light/dark pairs for HTML, a dedicated `render_d2_pdf` or a more flexible `render_d2` is needed. For PDF, we typically don't need the dark mode variant.

## Strategy for Implementation

1.  **Update `render_d2`** or create `render_d2_for_latex` to support PDF generation.
    *   Adjust command to `d2 ... output.pdf`.
    *   Handle options (fonts, themes) appropriate for print.
2.  **Implement `latex_visit_d2`**.
    *   Call the render function.
    *   Append `\sphinxincludegraphics` to `self.body`.
3.  **Register the visitor**.
    *   Update `setup(app)` to add `latex=(latex_visit_d2, None)` to the `d2_node` definition.

