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
- strict_concat_rows
- save_csv
- concentrate_csv
- rehydrate_csv
- create_sample_csv
- strip_utf8_bom
- DataFrame
- build_filter
- infer_type
- find_knapsack_indices
- mark_knapsack_csv

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
- csvsmith.strict_concat
- csvsmith.cli (CLI entrypoint)
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("csvsmith")
except PackageNotFoundError:
    __version__ = "0.0.0"

from .tools.classify import CSVClassifier
from .tools.csv_viewer import DataFrame, build_filter, infer_type
from .tools.dense_csv import (
    ConcentrateResult,
    RehydrateResult,
    concentrate_csv,
    rehydrate_csv,
)
from .tools.excel2csv import excel_to_csv
from .tools.filter_rows import DropRowsBySubstring
from .tools.find_matches_in_csv import find_matches_in_csv
from .tools.knapsack_csv import (
    KnapsackCSVResult,
    find_knapsack_indices,
    mark_knapsack_csv,
)
from .tools.move_files import move_by_suffix
from .tools.row_dedup import (
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from .tools.sample_csv import SampleCSVResult, create_sample_csv
from .tools.strip_bom import StripBomResult, strip_utf8_bom
from .tools.strict_concat import save_csv, strict_concat_rows
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
    "strict_concat_rows",
    "save_csv",
    "ConcentrateResult",
    "RehydrateResult",
    "concentrate_csv",
    "rehydrate_csv",
    "SampleCSVResult",
    "create_sample_csv",
    "StripBomResult",
    "strip_utf8_bom",
    "DataFrame",
    "build_filter",
    "infer_type",
    "KnapsackCSVResult",
    "find_knapsack_indices",
    "mark_knapsack_csv",
]
