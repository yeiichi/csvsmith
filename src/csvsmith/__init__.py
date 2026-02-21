"""
csvsmith: small, focused CSV utilities.

Public API:
- count_duplicates_sorted
- add_row_digest
- find_duplicate_rows
- dedupe_with_report
- CSVClassifier

Submodules:
- csvsmith.duplicates
- csvsmith.classify
- csvsmith.cli (CLI entrypoint)
"""

__version__ = "0.2.1"

from .duplicates import (
    count_duplicates_sorted,
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from .classify import CSVClassifier

__all__ = [
    "count_duplicates_sorted",
    "add_row_digest",
    "find_duplicate_rows",
    "dedupe_with_report",
    "CSVClassifier",
]