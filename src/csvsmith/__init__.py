"""
csvsmith: small, focused CSV utilities.

Public API:
- count_duplicates_sorted
- add_row_digest
- find_duplicate_rows
- dedupe_with_report
- read_csv_rows
- write_csv_rows
- CSVClassifier
- DropRowsBySubstring
- excel_to_csv
- move_by_suffix

Compatibility aliases:
- CSVCleaner

Submodules:
- csvsmith.row_dedup
- csvsmith.classify
- csvsmith.filter_rows
- csvsmith.excel2csv
- csvsmith.move_files
- csvsmith.cli (CLI entrypoint)
"""

__version__ = "0.2.3"

from .row_dedup import (
    count_duplicates_sorted,
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
    read_csv_rows,
    write_csv_rows,
)
from .classify import CSVClassifier
from .filter_rows import DropRowsBySubstring, CSVCleaner
from .excel2csv import excel_to_csv
from .move_files import move_by_suffix

__all__ = [
    "count_duplicates_sorted",
    "add_row_digest",
    "find_duplicate_rows",
    "dedupe_with_report",
    "read_csv_rows",
    "write_csv_rows",
    "CSVClassifier",
    "DropRowsBySubstring",
    "excel_to_csv",
    "move_by_suffix",
]
