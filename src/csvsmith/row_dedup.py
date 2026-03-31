from __future__ import annotations

import csv
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Hashable, Iterable, Mapping, Optional, Sequence


ROW_SEP = "\x1f"
KEEP_OPTIONS = {"first", "last"}

Row = dict[str, str]
RowLike = Mapping[str, object]


def count_duplicates_sorted(
    items: Iterable[Hashable],
    threshold: int = 2,
    reverse: bool = True,
) -> list[tuple[Hashable, int]]:
    """Count items and return those occurring at least `threshold` times."""
    counter = Counter(items)
    duplicates = [(key, count) for key, count in counter.items() if count >= threshold]
    duplicates.sort(key=lambda x: x[1], reverse=reverse)
    return duplicates


def read_csv_rows(csv_path: Path | str, encoding: str = "utf-8") -> list[Row]:
    """Read a CSV file into a list of row dictionaries."""
    path = Path(csv_path)
    with path.open("r", encoding=encoding, newline="") as fp:
        reader = csv.DictReader(fp)
        return list(reader)


def write_csv_rows(
    csv_path: Path | str,
    rows: Sequence[Mapping[str, object]],
    *,
    fieldnames: Sequence[str],
    encoding: str = "utf-8",
) -> None:
    """Write row dictionaries to a CSV file."""
    path = Path(csv_path)
    with path.open("w", encoding=encoding, newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _normalize_cell(value: object) -> str:
    """Convert a cell value to a stable string for hashing."""
    if value is None:
        return ""
    return str(value)


def _resolve_columns(
    rows: Sequence[RowLike],
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
) -> list[str]:
    """Resolve the effective column list used for comparison."""
    if subset is None:
        if not rows:
            return []
        cols = list(rows[0].keys())
    else:
        cols = [str(col) for col in subset]

    if exclude:
        exclude_set = {str(col) for col in exclude}
        cols = [col for col in cols if col not in exclude_set]

    return cols


def make_row_digest(row: RowLike, *, columns: Sequence[str]) -> str:
    """Build a SHA-256 digest for a row using selected columns."""
    joined = ROW_SEP.join(_normalize_cell(row.get(col, "")) for col in columns)
    return sha256(joined.encode("utf-8")).hexdigest()


def add_row_digest(
    rows: Sequence[RowLike],
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
    colname: str = "row_digest",
    inplace: bool = False,
) -> list[dict[str, object]]:
    """Add a row digest column and return the resulting rows."""
    columns = _resolve_columns(rows, subset=subset, exclude=exclude)

    out = rows if inplace else [dict(row) for row in rows]

    for row in out:
        row[colname] = make_row_digest(row, columns=columns)

    return [dict(row) for row in out]


def find_duplicate_rows(
    rows: Sequence[RowLike],
    *,
    subset: Optional[Sequence[Hashable]] = None,
) -> list[dict[str, object]]:
    """Return only rows that participate in duplicate groups."""
    columns = _resolve_columns(rows, subset=subset)

    grouped: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        digest = make_row_digest(row, columns=columns)
        grouped[digest].append(idx)

    dup_indices = {
        idx
        for indices in grouped.values()
        if len(indices) > 1
        for idx in indices
    }

    return [dict(rows[idx]) for idx in sorted(dup_indices)]


def dedupe_with_report(
    rows: Sequence[RowLike],
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
    keep: str = "first",
    digest_col: str = "row_digest",
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Drop duplicates and return `(deduped_rows, report)`."""
    if keep not in KEEP_OPTIONS:
        raise ValueError(f"keep must be one of {sorted(KEEP_OPTIONS)}")

    columns = _resolve_columns(rows, subset=subset, exclude=exclude)

    grouped: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        digest = make_row_digest(row, columns=columns)
        grouped[digest].append(idx)

    report = [
        {
            digest_col: digest,
            "count": len(indices),
            "indices": indices,
        }
        for digest, indices in grouped.items()
        if len(indices) > 1
    ]
    report.sort(key=lambda x: x["count"], reverse=True)

    kept_indices: set[int] = set()
    for indices in grouped.values():
        kept_indices.add(indices[0] if keep == "first" else indices[-1])

    deduped_rows = [
        dict(row)
        for idx, row in enumerate(rows)
        if idx in kept_indices
    ]

    return deduped_rows, report


def dedupe_csv_file(
    src: Path | str,
    dst: Path | str,
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
    keep: str = "first",
    encoding: str = "utf-8",
) -> list[dict[str, object]]:
    """Deduplicate a CSV file, write the result, and return the report."""
    rows = read_csv_rows(src, encoding=encoding)
    deduped_rows, report = dedupe_with_report(
        rows,
        subset=subset,
        exclude=exclude,
        keep=keep,
    )

    fieldnames = list(rows[0].keys()) if rows else []
    write_csv_rows(dst, deduped_rows, fieldnames=fieldnames, encoding=encoding)
    return report