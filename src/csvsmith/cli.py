#!/usr/bin/env python3
"""
csvsmith CLI

Duplicate-related helpers on CSV files.

Subcommands:
  - row-duplicates: show only rows that are duplicated
  - dedupe: drop duplicates and write both deduped CSV and a report CSV
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence, Optional, List

import pandas as pd

from .duplicates import find_duplicate_rows, dedupe_with_report


def _parse_cols(cols: Optional[Sequence[str]]) -> Optional[List[str]]:
    """
    Normalize column list arguments from CLI.

    We accept:
      --subset col1 col2 col3
      --exclude colA colB
    or omit entirely.
    """
    if cols is None:
        return None
    if len(cols) == 0:
        return None
    return list(cols)


def _effective_subset(
    df: pd.DataFrame,
    subset: Optional[Sequence[str]],
    exclude: Optional[Sequence[str]],
) -> Optional[List[str]]:
    """
    Compute the effective subset of columns to use for duplicate detection,
    given a requested subset and/or exclude list.

    Logic:
      - if subset is None: start from all columns
      - else: start from subset
      - then remove any columns in exclude
    """
    if subset is None:
        cols = list(df.columns)
    else:
        cols = list(subset)

    if exclude:
        exclude_set = set(exclude)
        cols = [c for c in cols if c not in exclude_set]

    if not cols:
        return None

    return cols


def cmd_row_duplicates(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    df = pd.read_csv(input_path)
    subset = _parse_cols(args.subset)
    exclude = _parse_cols(args.exclude)

    eff_subset = _effective_subset(df, subset=subset, exclude=exclude)

    dup_df = find_duplicate_rows(df, subset=eff_subset)

    if args.output:
        output_path = Path(args.output)
        dup_df.to_csv(output_path, index=False)
    else:
        dup_df.to_csv(sys.stdout, index=False)

    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    df = pd.read_csv(input_path)
    subset = _parse_cols(args.subset)
    exclude = _parse_cols(args.exclude)

    deduped, report = dedupe_with_report(
        df,
        subset=subset,
        exclude=exclude,
        keep=args.keep,
        digest_col=args.digest_col,
    )

    deduped_path = Path(args.deduped)
    report_path = Path(args.report)

    deduped_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    deduped.to_csv(deduped_path, index=False)
    report.to_csv(report_path, index=False)

    print(f"Wrote deduped CSV to: {deduped_path}")
    print(f"Wrote duplicate report to: {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csvsmith",
        description="Small CSV utilities (duplicates-focused, first iteration).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # row-duplicates
    p_row = subparsers.add_parser(
        "row-duplicates",
        help="Print only rows that have duplicates.",
    )
    p_row.add_argument("input", help="Input CSV file.")
    p_row.add_argument(
        "--subset",
        nargs="*",
        help="Column names to consider when detecting duplicates. "
             "If omitted, all columns are used.",
    )
    p_row.add_argument(
        "--exclude",
        nargs="*",
        help="Column names to exclude from duplicate detection. "
             "Useful for ID columns, timestamps, etc.",
    )
    p_row.add_argument(
        "-o",
        "--output",
        help="Output CSV file for duplicate rows. If omitted, writes to stdout.",
    )
    p_row.set_defaults(func=cmd_row_duplicates)

    # dedupe
    p_dedupe = subparsers.add_parser(
        "dedupe",
        help="Drop duplicates and generate a duplicate-report CSV.",
    )
    p_dedupe.add_argument("input", help="Input CSV file.")
    p_dedupe.add_argument(
        "--subset",
        nargs="*",
        help="Column names to consider when detecting duplicates. "
             "If omitted, all columns are used.",
    )
    p_dedupe.add_argument(
        "--exclude",
        nargs="*",
        help="Column names to exclude from duplicate detection. "
             "Useful for ID columns, timestamps, etc.",
    )
    p_dedupe.add_argument(
        "--keep",
        choices=["first", "last", "False"],
        default="first",
        help='Which duplicate to keep (same as pandas.drop_duplicates). '
             '"False" = drop all occurrences. Default: "first".',
    )
    p_dedupe.add_argument(
        "--digest-col",
        default="row_digest",
        help='Name of digest column used in the report. Default: "row_digest".',
    )
    p_dedupe.add_argument(
        "--deduped",
        required=True,
        help="Path to write the deduplicated CSV.",
    )
    p_dedupe.add_argument(
        "--report",
        required=True,
        help="Path to write the duplicate-report CSV.",
    )
    p_dedupe.set_defaults(func=cmd_dedupe)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        func = args.func
    except AttributeError:
        parser.print_help()
        return 1

    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
