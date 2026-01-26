# Research: Phase 2 - Configuration

## Context
Phase 2 focuses on enabling configuration options for the D2 Sphinx extension, specifically allowing users to customize the D2 executable path, themes, and fonts via `conf.py` and directive options.

## 1. D2 CLI Options

Research confirms the following CLI arguments for `d2`:

*   **Theme**: `d2` uses the `--theme` flag.
    *   It accepts an integer ID (e.g., `0`, `1`, `100`).
*   **Fonts**: `d2` allows specifying font files via CLI flags.
    *   `--font-regular <path>`: Regular font.
    *   `--font-italic <path>`: Italic font.
    *   `--font-bold <path>`: Bold font.
    *   `--font-mono <path>`: Monospace font (used for code snippets within diagrams).

These flags expect file paths to `.ttf` or `.otf` files.

## 2. Argument Precedence

The implementation will follow standard Sphinx extension precedence:

1.  **Directive Option**: Values specified in the RST directive (`.. d2:: :theme: 100`) take highest precedence.
2.  **Global Configuration**: Values specified in `conf.py` (e.g., `d2_theme = 100`) are used if no directive option is present.
3.  **Default Behavior**: If neither is specified, the CLI flag is omitted, allowing `d2` to use its built-in defaults.

**Note**: Requirements specify a `theme` directive option. Font configurations are currently scoped to Global Configuration (`conf.py`) only via `d2_font` and `d2_mono_font`.

## 3. Recommended Implementation Strategy

### Updates to `sphinxcontrib/d2/__init__.py`

#### 1. Configuration Values (`setup` function)
Register new configuration values with `app.add_config_value`.

*   `d2_theme`: default `None` (allows D2 default or directive override)
*   `d2_font`: default `None` (Maps to `--font-regular`)
*   `d2_mono_font`: default `None` (Maps to `--font-mono`)
*   `d2_bold_font`: default `None` (For completeness, maps to `--font-bold`)
*   `d2_italic_font`: default `None` (For completeness, maps to `--font-italic`)

#### 2. Directive Options (`D2Directive` class)
Update `option_spec` to include:
*   `'theme': directives.unchanged` (Allows integers or strings, though D2 expects integers/mapped names)

#### 3. Command Construction (`html_visit_d2` function)
Refactor the command construction to dynamically build the list based on precedence.

```python
def html_visit_d2(self, node):
    config = self.builder.config
    options = node['options']
    
    cmd = [config.d2_command]

    # Theme: Directive > Config
    # Check if 'theme' is in options, otherwise use config.d2_theme
    theme = options.get('theme', config.d2_theme)
    if theme is not None:
        cmd.extend(['--theme', str(theme)])

    # Fonts: Config only (as per current requirements)
    if config.d2_font:
        cmd.extend(['--font-regular', config.d2_font])
    if config.d2_mono_font:
        cmd.extend(['--font-mono', config.d2_mono_font])
    # Add support for bold/italic if we decide to expose them
    
    # Input/Output arguments
    cmd.extend(['-', '-'])

    # ... execution ...
```

### Validation
*   Ensure `d2_command` logic remains robust.
*   Verify that passing `None` as config values results in clean command without empty flags.
