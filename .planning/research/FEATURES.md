# Feature Requirements: Sphinx D2 Plugin

## Core Directive: `.. d2::`

The plugin must provide a directive similar to `.. graphviz::`.

### Syntax
```rst
.. d2:: [optional filename]
   :option: value

   x -> y: label
```

### Options
1.  **`:format:`**: Output format override (svg, png, pdf). Default should come from `conf.py`.
2.  **`:layout:`**: D2 layout engine (dagre, elk).
3.  **`:theme:`**: D2 theme ID (e.g., 0, 1, 100).
4.  **`:caption:`**: Standard figure caption.
5.  **`:alt:`**: Alt text for accessibility.
6.  **`:align:`**: Image alignment (left, center, right).
7.  **`:sketch:`**: Enable sketch mode (hand-drawn look).
8.  **`:scale:`**: Image scaling percentage.

## Configuration (`conf.py`)
Users should be able to control global defaults:
- `d2_command`: Path to d2 executable (default: 'd2').
- `d2_output_format`: Global default format (default: 'svg').
- `d2_theme_id`: Default theme.
- `d2_layout_engine`: Default layout.

## Comparison with `sphinx.ext.graphviz`

| Feature | `sphinx.ext.graphviz` | `sphinx.ext.d2` (Target) |
| :--- | :--- | :--- |
| **Input** | DOT language | D2 language |
| **Rendering** | `dot` CLI | `d2` CLI |
| **Output** | PNG, SVG, PDF | SVG, PNG, PDF |
| **Map Files** | Supports clickable image maps | D2 supports SVG interaction, map support harder to implement initially |
| **Code Inclusion** | Inline or via file argument | Inline or via file argument |

## Output Formats
- **HTML Builder**: Prefer **SVG** for quality and interactivity (tooltips, links). PNG as fallback.
- **LaTeX/PDF Builder**: Prefer **PDF** (vector) or **PNG** (high res). SVG often needs conversion for LaTeX.
