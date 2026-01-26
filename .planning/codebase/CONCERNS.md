# Concerns

## Technical Debt
- **Docutils Dependency:** Pinned to `<0.23` (in `pyproject.toml`). Upgrading `docutils` often breaks Sphinx due to internal changes in `docutils`.
- **Legacy Code:** Some modules carry legacy baggage from early Sphinx versions.
- **Global State:** While `Sphinx` app is encapsulated, there are some reliance on module-level globals in older parts or strictness in `conftest.py` about "cleaning up global state".

## Deprecations
- **Upcoming Removals:** `sphinx.deprecation` defines `RemovedInSphinx10Warning` and `RemovedInSphinx11Warning`, indicating a long-term roadmap for API cleanup.
- **Extensions:** Some older extensions or hooks might be deprecated.

## Maintainability
- **Complexity:** The "Builder" and "Environment" interaction is complex and stateful (pickled).
- **Test Suite Size:** Large test suite with integration tests that involve file I/O (building docs), which can be slow.

## Security
- **Pickle:** The build environment uses `pickle`. While generally trusted for local builds, processing untrusted pickle data is a known Python risk (though less relevant here as it's self-generated).
- **External Requests:** Link checker and `requests` usage need standard network security practices.
