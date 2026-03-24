import argparse
import json
import sys
from pathlib import Path
from typing import Sequence, Optional

import pandas as pd

from .classify import CSVClassifier
from .duplicates import find_duplicate_rows, dedupe_with_report
from .excel2csv import excel_to_csv
from .filter_rows import DropRowsBySubstring


def cmd_row_duplicates(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input)
    subset = args.subset.split(",") if args.subset else None
    dupes = find_duplicate_rows(df, subset=subset)
    if dupes.empty:
        print("No duplicate rows found.")
    else:
        print(f"Found {len(dupes)} duplicate rows:")
        print(dupes.to_csv(index=False))
    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input)
    subset = args.subset.split(",") if args.subset else None
    exclude = args.exclude.split(",") if args.exclude else None

    deduped_df, report = dedupe_with_report(
        df, subset=subset, exclude=exclude, keep=args.keep
    )

    output_path = Path(args.output) if args.output else Path(args.input).with_suffix(".deduped.csv")
    deduped_df.to_csv(output_path, index=False)
    print(f"Wrote deduped CSV to: {output_path}")

    if args.report:
        report_path = Path(args.report)
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Wrote deduplication report to: {report_path}")

    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    classifier = CSVClassifier(
        source_dir=args.source,
        dest_dir=args.dest,
        mode=args.mode,
        match=args.match,
        auto=args.auto,
        dry_run=args.dry_run,
    )
    classifier.run()
    return 0


def cmd_excel_to_csv(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        output_path = excel_to_csv(
            input_path,
            csv_path=args.output,
            sheet_name=args.sheet_name,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Wrote CSV to: {output_path}")
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        cleaner = DropRowsBySubstring(
            input_path,
            column_name=args.column_name,
            unwanted_text=args.unwanted_text,
            case_sensitive=not args.case_insensitive,
            keep_header=not args.drop_header,
        )
        cleaner.write_filtered_rows()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    output_path = input_path.with_suffix(DropRowsBySubstring.CLEAN_SUFFIX)
    print(f"Wrote cleaned CSV to: {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csvsmith",
        description="Small CSV utilities for deduplication and organization.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # row-duplicates
    p_dupes = subparsers.add_parser("row-duplicates", help="Find duplicate rows in a CSV.")
    p_dupes.add_argument("input", help="Input CSV file.")
    p_dupes.add_argument("--subset", help="Comma-separated column names to consider.")
    p_dupes.set_defaults(func=cmd_row_duplicates)

    # dedupe
    p_dedupe = subparsers.add_parser("dedupe", help="Remove duplicate rows and save a report.")
    p_dedupe.add_argument("input", help="Input CSV file.")
    p_dedupe.add_argument("-o", "--output", help="Output CSV file.")
    p_dedupe.add_argument("--subset", help="Comma-separated column names to consider.")
    p_dedupe.add_argument("--exclude", help="Comma-separated column names to exclude.")
    p_dedupe.add_argument("--keep", choices=["first", "last", "False"], default="first",
                          help="Which duplicate to keep.")
    p_dedupe.add_argument("--report", help="Path to save the deduplication report (JSON).")
    p_dedupe.set_defaults(func=cmd_dedupe)

    # classify
    p_classify = subparsers.add_parser("classify", help="Categorize CSV files based on headers.")
    p_classify.add_argument("source", help="Source directory containing CSV files.")
    p_classify.add_argument("dest", help="Destination directory for categorized files.")
    p_classify.add_argument("--mode", choices=["strict", "relaxed"], default="strict")
    p_classify.add_argument("--match", choices=["exact", "subset"], default="exact")
    p_classify.add_argument("--auto", action="store_true", help="Automatically create categories.")
    p_classify.add_argument("--dry-run", action="store_true", help="Do not move files, only report.")
    p_classify.set_defaults(func=cmd_classify)

    # excel-to-csv
    p_excel = subparsers.add_parser("excel-to-csv", help="Convert an Excel worksheet to CSV.")
    p_excel.add_argument("input", help="Input Excel file.")
    p_excel.add_argument("-o", "--output", help="Output CSV file.")
    p_excel.add_argument("--sheet-name", help="Worksheet name to convert.")
    p_excel.set_defaults(func=cmd_excel_to_csv)

    # clean
    p_clean = subparsers.add_parser("clean", help="Remove rows whose selected column contains unwanted text.")
    p_clean.add_argument("input", help="Input CSV file.")
    p_clean.add_argument("column_name", help="Column name to inspect.")
    p_clean.add_argument("unwanted_text", help="Substring that triggers row removal.")
    p_clean.add_argument("--case-insensitive", action="store_true", help="Perform case-insensitive matching.")
    p_clean.add_argument("--drop-header", action="store_true", help="Do not preserve the header row.")
    p_clean.set_defaults(func=cmd_clean)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        # Convert "False" string to False boolean for dedupe keep argument if necessary
        if args.command == "dedupe" and args.keep == "False":
            args.keep = False
        return args.func(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
