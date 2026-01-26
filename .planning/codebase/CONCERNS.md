# Concerns & Notes

## Architecture
- **Complexity**: The event system and direct mutation of the Docutils node tree can be complex to debug.
- **Legacy**: The codebase has evolved over many years ("Gracefully adapted from the TextPress system"). Some parts might carry historical debt.
- **Docutils Coupling**: Deep coupling with Docutils means upstream changes can have significant impact.

## Development
- **Testing Performance**: Full test suite can be slow due to the nature of filesystem I/O involved in building docs.
- **Type Safety**: While `mypy` is used, the dynamic nature of Python and the extension system can acts as a limit to strict typing coverage.

## Dependencies
- **Exact Pinnings**: Use of `pyproject.toml` helps, but extensions often have conflicting requirements for `docutils` versions.
