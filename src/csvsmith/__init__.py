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
- StringDistance
- Relation
- Result
- analyze_pair

Compatibility aliases:
- CSVCleaner

Submodules:
- csvsmith.clean_numeric
- csvsmith.string_distance
- csvsmith.row_dedup
- csvsmith.classify
- csvsmith.filter_rows
- csvsmith.excel2csv
- csvsmith.move_files
- csvsmith.cli (CLI entrypoint)
"""

__version__ = "0.6.0"

from .tools.clean_numeric import clean_numeric
from .tools.row_dedup import (
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from .utils.io import (
    count_duplicates_sorted,
    read_csv_rows,
    write_csv_rows,
)
from .tools.classify import CSVClassifier
from .tools.filter_rows import DropRowsBySubstring, CSVCleaner
from .tools.excel2csv import excel_to_csv
from .tools.move_files import move_by_suffix
from .utils.distance import StringDistance, Relation, Result, analyze_pair

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
    "StringDistance",
    "Relation",
    "Result",
    "analyze_pair",
    "clean_numeric",
]
