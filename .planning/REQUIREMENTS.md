# Requirements

## v1 Requirements

### Core Integration
- [ ] **CORE-01**: `.. d2::` directive parses inline D2 code
- [ ] **CORE-02**: `.. d2::` directive supports `file` option for external source files
- [ ] **CORE-03**: Extension correctly detects and invokes `d2` binary via subprocess
- [ ] **CORE-04**: Build fails gracefully with clear error if `d2` is missing

### Rendering & Output
- [ ] **REND-01**: Supports SVG output for HTML builders
- [ ] **REND-02**: Supports PNG/PDF output for LaTeX/PDF builders
- [ ] **REND-03**: Caches generated images (SHA1) to speed up subsequent builds

### Configuration
- [ ] **CONF-01**: `d2_command` config for custom binary path
- [ ] **CONF-02**: `d2_theme` config for global theme setting
- [ ] **CONF-03**: Directive supports local `theme` override
- [ ] **CONF-04**: `d2_font` and `d2_mono_font` configs for custom fonts

### Standard Figure Support
- [ ] **FIG-01**: Support `:caption:`, `:alt:`, and `:align:` options

## v2 Requirements (Deferred)
- [ ] Interactive editor integration
- [ ] Bundled d2 binary installation

## Out of Scope
- Live preview while typing (requires JS runtime integration)
- Complex multi-page diagrams (D2 restriction/scope)

## Traceability

| ID | Phase | Description |
| :--- | :--- | :--- |
| **CORE-01** | Phase 1 | Inline D2 code parsing |
| **CORE-02** | Phase 1 | External file support |
| **CORE-03** | Phase 1 | Subprocess invocation |
| **CORE-04** | Phase 1 | Error handling |
| **REND-01** | Phase 1 | SVG Output |
| **CONF-01** | Phase 2 | Binary path config |
| **CONF-02** | Phase 2 | Global theme config |
| **CONF-03** | Phase 2 | Local theme override |
| **CONF-04** | Phase 2 | Font configuration |
| **REND-02** | Phase 3 | PDF/PNG Output |
| **REND-03** | Phase 4 | Caching |
| **FIG-01** | Phase 4 | Standard figure options |
