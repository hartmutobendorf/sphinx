# Common Pitfalls & Risks

## 1. Missing Executable
- **Issue**: User installs extension but doesn't have `d2` installed.
- **Mitigation**:
  - Check for `d2` existence during `builder-inited` event.
  - Fail gracefully with a clear error message: "d2 command cannot be run".

## 2. Build Performance (Blocking)
- **Issue**: D2 compilation can be slow. Re-rendering 100 diagrams on every "make html" will kill iteration speed.
- **Mitigation**: 
  - **Aggressive Caching**: Must implement content-hashing. Only run `d2` if the content hash changes.
  - **Parallelism**: Sphinx supports parallel builds (`-j auto`). Ensure file writing is atomic or thread-safe to avoid race conditions if multiple workers try to generate the same diagram (unlikely if hased by content).

## 3. Platform Differences (Windows vs Linux)
- **Issue**: File paths (backslashes) and executable extensions (`.exe`).
- **Mitigation**:
  - Use `os.path.join` and `pathlib`.
  - Use `shutil.which` to find the executable.

## 4. Security (Shell Injection)
- **Issue**: Passing unsanitized user input to a shell command.
- **Mitigation**:
  - **NEVER use `shell=True`** in `subprocess`.
  - Always pass arguments as a list: `['d2', '--theme', '0', 'in.d2', 'out.svg']`.

## 5. Dependency Tracking
- **Issue**: User uses `.. d2:: filename.d2`. They edit `filename.d2`, but Sphinx says "build succeeded, no changes".
- **Mitigation**:
  - Use `env.note_dependency(abspath)` in the directive when reading external files. This tells Sphinx to invalidate the document if that external file changes.

## 6. Output Format Incompatibility
- **Issue**: SVG works great in HTML but fails in LaTeX/PDF generation unless converted.
- **Mitigation**:
  - Detect builder type (`app.builder.name`).
  - Default to PNG or PDF for LaTeX builder if SVG is not supported or requires `spinx.ext.imgconverter` (which requires ImageMagick). Simpler to ask D2 for PDF/PNG directly for Latex builds.
