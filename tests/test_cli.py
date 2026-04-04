import pytest
from csvsmith.cli import build_parser, main


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