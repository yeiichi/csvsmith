..
    version list

v0.9.0
======

Released: 2026-06-21

CSVSmith v0.9.0 adds the dense CSV concentration and rehydration workflow for
deduplicating repeated values before downstream processing.

Added
-----

- Added the ``concentrate_csv`` and ``rehydrate_csv`` Python APIs.
- Added the ``concentrate`` and ``rehydrate`` CLI subcommands.
- Added versioned map metadata, safe token prefixes, path-collision checks,
  and atomic output writes.
- Added default output paths for the concentrated CSV and JSON map.
- Added reporting for potential repeated-operation reduction among mapped
  values.

Changed
-------

- Expanded the README, Quickstart, CLI reference, recipes, and tool
  documentation around the main csvsmith workflows.
- Added Python Semantic Release configuration with support for ``0.x``
  versions.

v0.8.0
======

Released: 2026-04-16

CSVSmith v0.8.0 adds the ``strict-concat`` tool and API for concatenating CSV
files with identical headers. This release also includes documentation
and CLI support for the new feature.

Added
-----

- Added ``strict_concat_rows`` and ``save_csv`` to the ``csvsmith.tools.strict_concat`` module.
- Exposed ``strict_concat_rows`` and ``save_csv`` at the top-level package API.
- Added the ``strict-concat`` CLI subcommand.
- Bumped the package version to ``0.8.0``.

v0.7.3
======

Released: 2026-04-10

- Minor bug fixes and internal improvements.

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
