from importlib.metadata import version

import pytest

import csvsmith
from csvsmith.cli import build_parser, main


def test_package_version_matches_metadata():
    assert csvsmith.__version__ == version("csvsmith")


def test_main_help():
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0


def test_cli_parses_drop_rows_command_with_options():
    parser = build_parser()
    args = parser.parse_args(
        [
            "drop-rows",
            "input.csv",
            "notes",
            "spam",
            "--case-insensitive",
            "--drop-header",
        ]
    )

    assert args.command == "drop-rows"
    assert args.input == "input.csv"
    assert args.column_name == "notes"
    assert args.unwanted_text == "spam"
    assert args.case_insensitive is True
    assert args.drop_header is True


def test_cli_parses_classify_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "classify",
            "src_dir",
            "dst_dir",
            "--mode",
            "relaxed",
            "--match",
            "subset",
            "--auto",
            "--dry-run",
        ]
    )

    assert args.command == "classify"
    assert args.source == "src_dir"
    assert args.dest == "dst_dir"
    assert args.mode == "relaxed"
    assert args.match == "subset"
    assert args.auto is True
    assert args.dry_run is True


def test_cli_parses_dedupe_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "dedupe",
            "input.csv",
            "-o",
            "out.csv",
            "--subset",
            "id",
            "--exclude",
            "date",
            "--keep",
            "last",
            "--report",
            "rep.json",
        ]
    )

    assert args.command == "dedupe"
    assert args.input == "input.csv"
    assert args.output == "out.csv"
    assert args.subset == "id"
    assert args.exclude == "date"
    assert args.keep == "last"
    assert args.report == "rep.json"


def test_cli_parses_move_files_command():
    parser = build_parser()
    args = parser.parse_args(["move-files", "src_dir", "dst_dir"])

    assert args.command == "move-files"
    assert args.source == "src_dir"
    assert args.dest == "dst_dir"
    assert args.suffixes is None


def test_cli_parses_move_files_command_with_suffixes():
    parser = build_parser()
    args = parser.parse_args(
        [
            "move-files",
            "src_dir",
            "dst_dir",
            "--suffixes",
            ".csv,.pdf",
        ]
    )

    assert args.command == "move-files"
    assert args.source == "src_dir"
    assert args.dest == "dst_dir"
    assert args.suffixes == ".csv,.pdf"


def test_cli_parses_move_files_command_with_suffixes_without_dots():
    parser = build_parser()
    args = parser.parse_args(
        [
            "move-files",
            "src_dir",
            "dst_dir",
            "--suffixes",
            "csv,pdf",
        ]
    )

    assert args.command == "move-files"
    assert args.source == "src_dir"
    assert args.dest == "dst_dir"
    assert args.suffixes == "csv,pdf"


def test_cli_parses_clean_numeric_command():
    parser = build_parser()
    args = parser.parse_args(["clean-numeric", "1,234.56", "--sep", ",", "--decimal", "."])

    assert args.command == "clean-numeric"
    assert args.value == "1,234.56"
    assert args.sep == ","
    assert args.decimal == "."


def test_cli_parses_clean_currency_numeric_command():
    parser = build_parser()
    args = parser.parse_args(
        ["clean-currency-numeric", "$1,234.56", "--sep", ",", "--decimal", "."]
    )

    assert args.command == "clean-currency-numeric"
    assert args.value == "$1,234.56"
    assert args.sep == ","
    assert args.decimal == "."


def test_cli_parses_clean_numeric_command_with_relaxed_mode():
    parser = build_parser()
    args = parser.parse_args(["clean-numeric", "not-a-number", "--relaxed"])

    assert args.command == "clean-numeric"
    assert args.value == "not-a-number"
    assert args.relaxed is True


def test_cli_parses_string_distance_command():
    parser = build_parser()
    args = parser.parse_args(["string-distance", "a", "b", "--ignore-case"])

    assert args.command == "string-distance"
    assert args.string_a == "a"
    assert args.string_b == "b"
    assert args.ignore_case is True


def test_cli_parses_find_matches_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "find-matches",
            "input.csv",
            "target",
            "--ignore-case",
            "--ignore-whitespace",
            "--no-nfkc",
        ]
    )

    assert args.command == "find-matches"
    assert args.input == "input.csv"
    assert args.target == "target"
    assert args.ignore_case is True
    assert args.ignore_whitespace is True
    assert args.no_nfkc is True


def test_cli_parses_strip_bom_command():
    parser = build_parser()
    args = parser.parse_args(["strip-bom", "input.csv", "-o", "output.csv"])

    assert args.command == "strip-bom"
    assert args.input == "input.csv"
    assert args.output == "output.csv"
    assert args.in_place is False


def test_cli_parses_strip_bom_command_in_place():
    parser = build_parser()
    args = parser.parse_args(["strip-bom", "input.csv", "--in-place"])

    assert args.command == "strip-bom"
    assert args.input == "input.csv"
    assert args.output is None
    assert args.in_place is True


def test_cli_parses_strict_concat_command():
    parser = build_parser()
    args = parser.parse_args(["strict-concat", "input_dir", "-o", "output.csv"])

    assert args.command == "strict-concat"
    assert args.input_dir == "input_dir"
    assert args.output == "output.csv"


def test_cli_parses_concentrate_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "concentrate",
            "input.csv",
            "-o",
            "dense.csv",
            "-m",
            "dense-map.json",
            "--columns",
            "description,notes",
            "--min-occurrences",
            "3",
        ]
    )

    assert args.command == "concentrate"
    assert args.input == "input.csv"
    assert args.output == "dense.csv"
    assert args.map == "dense-map.json"
    assert args.columns == "description,notes"
    assert args.min_occurrences == 3


def test_cli_parses_concentrate_command_with_default_output_paths():
    parser = build_parser()
    args = parser.parse_args(["concentrate", "input.csv"])

    assert args.command == "concentrate"
    assert args.input == "input.csv"
    assert args.output is None
    assert args.map is None


def test_cli_parses_rehydrate_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "rehydrate",
            "dense.csv",
            "-m",
            "dense-map.json",
            "-o",
            "restored.csv",
        ]
    )

    assert args.command == "rehydrate"
    assert args.input == "dense.csv"
    assert args.map == "dense-map.json"
    assert args.output == "restored.csv"


def test_cli_parses_sample_csv_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "sample-csv",
            "-o",
            "sample.csv",
            "--rows",
            "12",
            "--start",
            "2026-01-01",
            "--item-charset",
            "mix",
            "--seed",
            "42",
        ]
    )

    assert args.command == "sample-csv"
    assert args.output == "sample.csv"
    assert args.rows == 12
    assert args.start == "2026-01-01"
    assert args.item_charset == "mix"
    assert args.seed == 42


def test_cli_parses_view_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "view",
            "sample.csv",
            "--head",
            "3",
            "--page-size",
            "10",
            "--columns",
            "date,value",
            "--filter",
            "value",
            ">",
            "700",
            "--no-convert-types",
        ]
    )

    assert args.command == "view"
    assert args.input == "sample.csv"
    assert args.head == 3
    assert args.page_size == 10
    assert args.columns == "date,value"
    assert args.filter == ["value", ">", "700"]
    assert args.no_convert_types is True


def test_cli_parses_knapsack_command():
    parser = build_parser()
    args = parser.parse_args(
        [
            "knapsack",
            "sample.csv",
            "value",
            "2,036",
            "-o",
            "marked.csv",
            "--mark-column",
            "selected",
            "--mark-value",
            "knapsack",
        ]
    )

    assert args.command == "knapsack"
    assert args.input == "sample.csv"
    assert args.target_column == "value"
    assert args.capacity == "2,036"
    assert args.output == "marked.csv"
    assert args.mark_column == "selected"
    assert args.mark_value == "knapsack"
