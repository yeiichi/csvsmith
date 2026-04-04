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

__version__ = "0.7.2"

from .tools.classify import CSVClassifier
from .tools.excel2csv import excel_to_csv
from .tools.filter_rows import DropRowsBySubstring
from .tools.find_matches_in_csv import find_matches_in_csv
from .tools.move_files import move_by_suffix
from .tools.row_dedup import (
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from .utils.clean_numeric import clean_numeric
from .utils.distance import StringDistance, Relation, Result, analyze_pair
from .utils.io import (
    count_duplicates_sorted,
    read_csv_rows,
    write_csv_rows,
)

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
    "find_matches_in_csv",
    "StringDistance",
    "Relation",
    "Result",
    "analyze_pair",
    "clean_numeric",
]
