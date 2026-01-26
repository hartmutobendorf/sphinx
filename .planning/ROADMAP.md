# Project Roadmap: Sphinx D2 Plugin

## Phase 1: Core Foundation
**Goal:** Users can generate SVG diagrams from rst code.

- [ ] **CORE-01**: `.. d2::` directive parses inline D2 code
- [ ] **CORE-02**: `.. d2::` directive supports `file` option for external source files
- [ ] **CORE-03**: Extension correctly detects and invokes `d2` binary via subprocess
- [ ] **CORE-04**: Build fails gracefully with clear error if `d2` is missing
- [ ] **REND-01**: Supports SVG output for HTML builders

**Success Criteria:**
- `d2` directive is registered and recognized.
- Inline and external d2 files render to SVG in HTML docs.
- Helper handles subprocess calls safely.

## Phase 2: Configuration
**Goal:** Users can customize themes, fonts, and execution paths.

- [ ] **CONF-01**: `d2_command` config for custom binary path
- [ ] **CONF-02**: `d2_theme` config for global theme setting
- [ ] **CONF-03**: Directive supports local `theme` override
- [ ] **CONF-04**: `d2_font` and `d2_mono_font` configs for custom fonts

**Success Criteria:**
- User can set paths in `conf.py`.
- Themes apply correctly globally and locally.
- Fonts are passed to the d2 CLI.

## Phase 3: Print Support
**Goal:** Support LaTeX/PDF output formats.

- [ ] **REND-02**: Supports PNG/PDF output for LaTeX/PDF builders

**Success Criteria:**
- `make latexpdf` works without errors.
- Diagrams appear correctly in PDF output.

## Phase 4: Optimization & Polish
**Goal:** Production-ready performance and standard figure features.

- [ ] **REND-03**: Caches generated images (SHA1) to speed up subsequent builds
- [ ] **FIG-01**: Support `:caption:`, `:alt:`, and `:align:` options

**Success Criteria:**
- Builds are significantly faster on re-run for unchanged diagrams.
- Figures integrate naturally with standard Sphinx figure styles.
