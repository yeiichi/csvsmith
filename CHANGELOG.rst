v0.7.0
======

Released: 2026-04-02

CSVSmith v0.7.0 introduces a major package reorganization that separates
command-oriented tools from shared utilities. This release updates module
locations, import paths, and tests to reflect the new structure, improving
maintainability and making the project layout clearer for future development.

Changed
-------

- Reorganized tool modules into ``csvsmith.tools``.
- Moved shared helper modules into ``csvsmith.utils``.
- Updated imports, package exports, and tests to match the new layout.
- Renamed modules and functions for clearer intent and consistency.

Notes
-----

This release focuses on structural cleanup and API layout improvements. Users
may need to update import paths to match the new module organization.