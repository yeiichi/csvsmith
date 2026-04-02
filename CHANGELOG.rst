v0.7.1
======

Released: 2026-04-03

CSVSmith v0.7.1 exposes ``find_matches_in_csv`` at the top-level package API
and refreshes the README to document the existing CLI and Python usage.

Changed
-------

- Exposed ``find_matches_in_csv`` as a top-level package API.
- Documented the existing ``find-matches`` CLI subcommand in the README.
- Refreshed the README with badges and updated usage examples.
- Bumped the package version to ``0.7.1``.

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