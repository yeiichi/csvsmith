"""
csvsmith: small, focused CSV utilities.

Public API:
- count_duplicates_sorted
- add_row_digest
- find_duplicate_rows
- dedupe_with_report
- CSVClassifier
- CSVCleaner
- excel_to_csv

Submodules:
- csvsmith.row_dedup
- csvsmith.classify
- csvsmith.csv_cleaner
- csvsmith.excel2csv
- csvsmith.cli (CLI entrypoint)
"""

__version__ = "0.2.2"

from .row_dedup import (
    count_duplicates_sorted,
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from .classify import CSVClassifier
from .filter_rows import DropRowsBySubstring, CSVCleaner

__all__ = ["DropRowsBySubstring", "CSVCleaner"]
