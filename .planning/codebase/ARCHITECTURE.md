# Architecture

## High-Level Pattern
Sphinx follows a **Core-Extension** architecture. The core application manages the build process, configuration, and event loop, while most functionality (including language domains and output builders) is implemented as extensions.

## Key Components

### Core Application
- **`sphinx.application.Sphinx`**: The main entry point. Initializes the environment, loads extensions, and orchestrates the build.
- **`sphinx.config.Config`**: Handles configuration (`conf.py`).
- **`sphinx.project.Project`**: Represents the source project.

### The Build Process
1.  **Phase 0: Initialization**: Load config, setup extensions, init environment.
2.  **Phase 1: Reading**: Parse source files (ReST) into Docutils doctrees.
3.  **Phase 2: Consistency Check**: specific to some builders/extensions.
4.  **Phase 3: Resolving**: Cross-references and toctrees are resolved.
5.  **Phase 4: Writing**: `Builder` classes convert the resolved doctrees into output formats (HTML, LaTeX, etc.).

### Build Environment
- **`sphinx.environment.BuildEnvironment`**: Persists the state of the documentation build (pickled to disk). It stores the inventory of cross-references, toctrees, and metadata.

### Extensions System
- **Registry**: `sphinx.registry.SphinxComponentRegistry` manages builders, domains, directives, roles, etc.
- **Events**: `sphinx.events.EventManager` handles a rich event system (e.g., `builder-inited`, `source-read`, `doctree-resolved`) allowing extensions to hook into various stages.

### Domains
- **`sphinx.domains.Domain`**: Abstract base class for language domains (Python, C, C++, etc.). Domains define object types, roles, and directives specific to a language.

## Data Flow
`Source Files (.rst)` -> `Reader (Docutils)` -> `Doctrees (Nodes)` -> `Environment (Pickled State)` -> `Transforms` -> `Writer/Builder` -> `Output Files (.html, .tex)`
