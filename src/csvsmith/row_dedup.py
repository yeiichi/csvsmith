"""
Row-deduplication helpers for csvsmith.

Includes:
- count_duplicates_sorted: generic iterable duplicate counter
- add_row_digest: add a SHA-256 digest per row to a DataFrame
- find_duplicate_rows: return only rows that have duplicates
- dedupe_with_report: drop duplicates and report duplicate groups
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from typing import Iterable, List, Tuple, Hashable, Sequence, Optional

import pandas as pd


def count_duplicates_sorted(
    items: Iterable[Hashable],
    threshold: int = 2,
    reverse: bool = True,
) -> List[Tuple[Hashable, int]]:
    """
    Count occurrences in an iterable and return items whose frequency
    is at or above `threshold`, sorted by count.
    """
    counter = Counter(items)
    duplicates = [(k, v) for k, v in counter.items() if v >= threshold]
    duplicates.sort(key=lambda x: x[1], reverse=reverse)
    return duplicates


def add_row_digest(
    df: pd.DataFrame,
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
    colname: str = "row_digest",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Add a SHA-256 digest for each row of a DataFrame.
    """
    if subset is None:
        cols = list(df.columns)
    else:
        cols = list(subset)

    if exclude:
        exclude_set = set(exclude)
        cols = [c for c in cols if c not in exclude_set]

    concatted = df[cols].astype("string").fillna("").agg("\x1f".join, axis=1)
    digests = concatted.map(lambda s: sha256(s.encode("utf-8")).hexdigest())

    if inplace:
        df[colname] = digests
        return df

    df2 = df.copy()
    df2[colname] = digests
    return df2


def find_duplicate_rows(
    df: pd.DataFrame,
    *,
    subset: Optional[Sequence[Hashable]] = None,
) -> pd.DataFrame:
    """
    Return only rows that participate in duplicates.
    """
    mask = df.duplicated(subset=subset, keep=False)
    return df[mask]


def dedupe_with_report(
    df: pd.DataFrame,
    *,
    subset: Optional[Sequence[Hashable]] = None,
    exclude: Optional[Sequence[Hashable]] = None,
    keep: str = "first",
    digest_col: str = "row_digest",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Drop duplicate rows and return a report of duplicate groups.
    """
    if subset is None:
        cols = list(df.columns)
    else:
        cols = list(subset)

    if exclude:
        exclude_set = set(exclude)
        cols = [c for c in cols if c not in exclude_set]

    subset_for_dupes: Optional[Sequence[Hashable]]
    subset_for_dupes = cols if cols else None

    work = add_row_digest(
        df,
        subset=subset_for_dupes,
        exclude=None,
        colname=digest_col,
        inplace=False,
    )

    grouped = work.groupby(digest_col, dropna=False)
    sizes = grouped.size().rename("count")
    indices_map = {k: list(v) for k, v in grouped.indices.items()}
    indices = pd.Series(indices_map, name="indices")

    report = (
        pd.concat([sizes, indices], axis=1)
        .reset_index()
        .rename(columns={"index": digest_col})
    )

    report = (
        report[report["count"] > 1]
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )

    df_deduped = df.drop_duplicates(subset=subset_for_dupes, keep=keep)
    return df_deduped, report