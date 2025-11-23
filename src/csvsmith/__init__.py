"""
csvsmith: small, focused CSV utilities.

Current submodules:
- csvsmith.duplicates
- csvsmith.cli (CLI entrypoint)
"""

from .duplicates import (
    count_duplicates_sorted,
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)

__all__ = [
    "count_duplicates_sorted",
    "add_row_digest",
    "find_duplicate_rows",
    "dedupe_with_report",
]
