import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Optional, Sequence


from . import __version__
from .tools.classify import CSVClassifier
from .tools.dense_csv import concentrate_csv, rehydrate_csv
from .tools.excel2csv import excel_to_csv
from .utils.clean_numeric import clean_currency_numeric, clean_numeric
from .tools.filter_rows import DropRowsBySubstring
from .tools.move_files import move_by_suffix, normalize_suffixes
from .tools.row_dedup import (
    dedupe_with_report,
    find_duplicate_rows,
)
from .tools.strict_concat import save_csv, strict_concat_rows
from .tools.find_matches_in_csv import find_matches_in_csv
from .utils.distance import analyze_pair
from .utils.io import read_csv_rows, write_csv_rows


def cmd_row_duplicates(args: argparse.Namespace) -> int:
    rows = read_csv_rows(args.input)
    subset = args.subset.split(",") if args.subset else None
    dupes = find_duplicate_rows(rows, subset=subset)

    if not dupes:
        print("No duplicate rows found.")
    else:
        print(f"Found {len(dupes)} duplicate rows:")
        fieldnames = list(dupes[0].keys())
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dupes)
    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    rows = read_csv_rows(args.input)
    subset = args.subset.split(",") if args.subset else None
    exclude = args.exclude.split(",") if args.exclude else None

    deduped_rows, report = dedupe_with_report(
        rows, subset=subset, exclude=exclude, keep=args.keep
    )

    output_path = Path(args.output) if args.output else Path(args.input).with_suffix(".deduped.csv")
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv_rows(output_path, deduped_rows, fieldnames=fieldnames)
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


def cmd_move_files(args: argparse.Namespace) -> int:
    suffixes = normalize_suffixes(args.suffixes.split(",") if args.suffixes else [])
    moved_count = move_by_suffix(args.source, args.dest, suffixes=suffixes)
    print(f"Moved {moved_count} file(s).")
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


def cmd_drop_rows(args: argparse.Namespace) -> int:
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

    output_path = input_path.with_suffix(DropRowsBySubstring.FILTERED_SUFFIX)
    print(f"Wrote filtered CSV to: {output_path}")
    return 0


def cmd_string_distance(args: argparse.Namespace) -> int:
    res = analyze_pair(args.string_a, args.string_b, args.ignore_case)

    print(f"{'Classification':<18}: {res.get_relation_string()}")
    print(f"{'D-Levenshtein Dist':<18}: {res.damerau_levenshtein_distance} changes")
    print(f"{'Jaro-Winkler':<18}: {res.jaro_winkler_score:.4f}")
    print(f"{'Similarity':<18}: {res.similarity_percentage:.2f}%")
    return 0


def cmd_clean_numeric(args: argparse.Namespace) -> int:
    try:
        cleaned = clean_numeric(
            args.value,
            sep=args.sep,
            decimal=args.decimal,
            relaxed=args.relaxed,
        )
        print(cleaned)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


def cmd_clean_currency_numeric(args: argparse.Namespace) -> int:
    try:
        cleaned = clean_currency_numeric(
            args.value,
            sep=args.sep,
            decimal=args.decimal,
            relaxed=args.relaxed,
        )
        print(cleaned)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


def cmd_find_matches(args: argparse.Namespace) -> int:
    results = find_matches_in_csv(
        args.input,
        args.target,
        ignore_case=args.ignore_case,
        ignore_whitespace=args.ignore_whitespace,
        nfkc=not args.no_nfkc,
    )

    if not results:
        print("No matches found.")
    else:
        print(json.dumps(results, indent=2))
    return 0


def cmd_strict_concat(args: argparse.Namespace) -> int:
    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"Error: input directory not found: {input_dir}", file=sys.stderr)
        return 1

    try:
        rows = strict_concat_rows(input_dir)
        save_csv(rows, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Wrote concatenated CSV to: {args.output}")
    return 0


def cmd_concentrate(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    output_path = (
        Path(args.output)
        if args.output
        else input_path.with_name(f"{input_path.stem}.dense.csv")
    )
    map_path = (
        Path(args.map)
        if args.map
        else input_path.with_name(f"{input_path.stem}.dense-map.json")
    )
    columns = (
        [column.strip() for column in args.columns.split(",") if column.strip()]
        if args.columns
        else None
    )
    try:
        result = concentrate_csv(
            input_path,
            output_path,
            map_path,
            columns=columns,
            min_occurrences=args.min_occurrences,
        )
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(
        f"Wrote concentrated CSV to: {result.output_csv_path} "
        f"({result.transformed_cell_count} cells, "
        f"{result.mapped_value_count} mapped values)"
    )
    if result.transformed_cell_count:
        avoided_operations = (
            result.transformed_cell_count - result.mapped_value_count
        )
        reduction_percentage = (
            avoided_operations / result.transformed_cell_count * 100
        )
        print(
            "Potential repeated-operation reduction for mapped values: "
            f"{avoided_operations}/{result.transformed_cell_count} "
            f"({reduction_percentage:.1f}%)"
        )
    print(f"Wrote dense CSV map to: {result.output_map_path}")
    return 0


def cmd_rehydrate(args: argparse.Namespace) -> int:
    try:
        result = rehydrate_csv(args.input, args.map, args.output)
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(
        f"Wrote rehydrated CSV to: {result.output_csv_path} "
        f"({result.restored_cell_count} cells restored)"
    )
    return 0


def _add_find_matches_parser(subparsers) -> None:
    parser = subparsers.add_parser("find-matches", help="Find matches in a CSV file.")
    parser.add_argument("input", help="Input CSV file.")
    parser.add_argument("target", help="Target string to find.")
    parser.add_argument("--ignore-case", action="store_true", help="Ignore case.")
    parser.add_argument("--ignore-whitespace", action="store_true", help="Ignore whitespace.")
    parser.add_argument("--no-nfkc", action="store_true", help="Disable NFKC normalization.")
    parser.set_defaults(func=cmd_find_matches)


def _add_strict_concat_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "strict-concat",
        help="Concatenate CSVs in a directory only when all headers match exactly.",
    )
    parser.add_argument("input_dir", help="Directory containing CSV files to concatenate.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path.")
    parser.set_defaults(func=cmd_strict_concat)


def _add_concentrate_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "concentrate",
        help="Replace repeated CSV values with deterministic tokens.",
    )
    parser.add_argument("input", help="Input CSV file.")
    parser.add_argument(
        "-o",
        "--output",
        help="Output CSV file (default: <input-stem>.dense.csv).",
    )
    parser.add_argument(
        "-m",
        "--map",
        help="Output JSON map file (default: <input-stem>.dense-map.json).",
    )
    parser.add_argument(
        "--columns",
        help="Comma-separated column names to concentrate (default: all columns).",
    )
    parser.add_argument(
        "--min-occurrences",
        type=int,
        default=2,
        help="Minimum repetitions required before replacing a value (default: 2).",
    )
    parser.set_defaults(func=cmd_concentrate)


def _add_rehydrate_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "rehydrate",
        help="Restore a concentrated CSV using its JSON map.",
    )
    parser.add_argument("input", help="Concentrated CSV file.")
    parser.add_argument("-m", "--map", required=True, help="Dense CSV JSON map file.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file.")
    parser.set_defaults(func=cmd_rehydrate)


def _add_row_duplicates_parser(subparsers) -> None:
    parser = subparsers.add_parser("row-duplicates", help="Find duplicate rows in a CSV.")
    parser.add_argument("input", help="Input CSV file.")
    parser.add_argument("--subset", help="Comma-separated column names to consider.")
    parser.set_defaults(func=cmd_row_duplicates)


def _add_dedupe_parser(subparsers) -> None:
    parser = subparsers.add_parser("dedupe", help="Remove duplicate rows and save a report.")
    parser.add_argument("input", help="Input CSV file.")
    parser.add_argument("-o", "--output", help="Output CSV file.")
    parser.add_argument("--subset", help="Comma-separated column names to consider.")
    parser.add_argument("--exclude", help="Comma-separated column names to exclude.")
    parser.add_argument(
        "--keep",
        choices=["first", "last", "False"],
        default="first",
        help="Which duplicate to keep.",
    )
    parser.add_argument("--report", help="Path to save the deduplication report (JSON).")
    parser.set_defaults(func=cmd_dedupe)


def _add_classify_parser(subparsers) -> None:
    parser = subparsers.add_parser("classify", help="Categorize CSV files based on headers.")
    parser.add_argument("source", help="Source directory containing CSV files.")
    parser.add_argument("dest", help="Destination directory for categorized files.")
    parser.add_argument("--mode", choices=["strict", "relaxed"], default="strict")
    parser.add_argument("--match", choices=["exact", "subset"], default="exact")
    parser.add_argument("--auto", action="store_true", help="Automatically create categories.")
    parser.add_argument("--dry-run", action="store_true", help="Do not move files, only report.")
    parser.set_defaults(func=cmd_classify)


def _add_move_files_parser(subparsers) -> None:
    parser = subparsers.add_parser("move-files", help="Move files by suffix.")
    parser.add_argument("source", help="Source directory containing files.")
    parser.add_argument("dest", help="Destination directory for moved files.")
    parser.add_argument(
        "--suffixes",
        help="Comma-separated suffixes to move (for example: csv,pdf or .csv,.pdf).",
    )
    parser.set_defaults(func=cmd_move_files)


def _add_excel_to_csv_parser(subparsers) -> None:
    parser = subparsers.add_parser("excel-to-csv", help="Convert an Excel worksheet to CSV.")
    parser.add_argument("input", help="Input Excel file.")
    parser.add_argument("-o", "--output", help="Output CSV file.")
    parser.add_argument("--sheet-name", help="Worksheet name to convert.")
    parser.set_defaults(func=cmd_excel_to_csv)


def _add_drop_rows_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "drop-rows",
        help="Remove rows whose selected column contains unwanted text.",
    )
    parser.add_argument("input", help="Input CSV file.")
    parser.add_argument("column_name", help="Column name to inspect.")
    parser.add_argument("unwanted_text", help="Substring that triggers row removal.")
    parser.add_argument(
        "--case-insensitive",
        action="store_true",
        help="Perform case-insensitive matching.",
    )
    parser.add_argument("--drop-header", action="store_true", help="Do not preserve the header row.")
    parser.set_defaults(func=cmd_drop_rows)


def _add_string_distance_parser(subparsers) -> None:
    parser = subparsers.add_parser("string-distance", help="Analyze distance between two strings.")
    parser.add_argument("string_a", help="First string.")
    parser.add_argument("string_b", help="Second string.")
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Ignore case for distance calculation.",
    )
    parser.set_defaults(func=cmd_string_distance)


def _add_clean_numeric_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "clean-numeric", help="Clean and convert a numeric string to float."
    )
    parser.add_argument("value", help="Numeric value to clean.")
    parser.add_argument("--sep", default=",", help="Group separator (default: ,).")
    parser.add_argument("--decimal", default=".", help="Decimal separator (default: .).")
    parser.add_argument(
        "--relaxed",
        action="store_true",
        help="Return the original input when it is not numeric.",
    )
    parser.set_defaults(func=cmd_clean_numeric)


def _add_clean_currency_numeric_parser(subparsers) -> None:
    parser = subparsers.add_parser(
        "clean-currency-numeric",
        help="Clean and convert a currency-prefixed numeric string to float.",
    )
    parser.add_argument("value", help="Numeric value to clean.")
    parser.add_argument("--sep", default=",", help="Group separator (default: ,).")
    parser.add_argument("--decimal", default=".", help="Decimal separator (default: .).")
    parser.add_argument(
        "--relaxed",
        action="store_true",
        help="Return the original input when it is not numeric.",
    )
    parser.set_defaults(func=cmd_clean_currency_numeric)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csvsmith",
        description="Lightweight CSV utilities for data integrity, deduplication, and organization.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_row_duplicates_parser(subparsers)
    _add_find_matches_parser(subparsers)
    _add_strict_concat_parser(subparsers)
    _add_concentrate_parser(subparsers)
    _add_rehydrate_parser(subparsers)
    _add_dedupe_parser(subparsers)
    _add_classify_parser(subparsers)
    _add_move_files_parser(subparsers)
    _add_excel_to_csv_parser(subparsers)
    _add_drop_rows_parser(subparsers)
    _add_string_distance_parser(subparsers)
    _add_clean_numeric_parser(subparsers)
    _add_clean_currency_numeric_parser(subparsers)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
