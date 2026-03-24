import pytest

from csvsmith.cli import build_parser


def test_cli_parses_excel_to_csv_command():
    parser = build_parser()
    args = parser.parse_args(["excel-to-csv", "input.xlsx"])

    assert args.command == "excel-to-csv"
    assert args.input == "input.xlsx"
    assert args.output is None
    assert args.sheet_name is None


def test_cli_parses_excel_to_csv_command_with_options():
    parser = build_parser()
    args = parser.parse_args(
        [
            "excel-to-csv",
            "input.xlsx",
            "-o",
            "output/result.csv",
            "--sheet-name",
            "Details",
        ]
    )

    assert args.command == "excel-to-csv"
    assert args.input == "input.xlsx"
    assert args.output == "output/result.csv"
    assert args.sheet_name == "Details"


def test_cli_parses_clean_command():
    parser = build_parser()
    args = parser.parse_args(["clean", "input.csv", "notes", "spam"])

    assert args.command == "clean"
    assert args.input == "input.csv"
    assert args.column_name == "notes"
    assert args.unwanted_text == "spam"
    assert args.case_insensitive is False
    assert args.drop_header is False


def test_cli_parses_clean_command_with_options():
    parser = build_parser()
    args = parser.parse_args(
        [
            "clean",
            "input.csv",
            "notes",
            "spam",
            "--case-insensitive",
            "--drop-header",
        ]
    )

    assert args.command == "clean"
    assert args.input == "input.csv"
    assert args.column_name == "notes"
    assert args.unwanted_text == "spam"
    assert args.case_insensitive is True
    assert args.drop_header is True


def test_cli_parses_row_duplicates_command():
    parser = build_parser()
    args = parser.parse_args(["row-duplicates", "input.csv", "--subset", "id,name"])

    assert args.command == "row-duplicates"
    assert args.input == "input.csv"
    assert args.subset == "id,name"


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


def test_cli_requires_a_subcommand():
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])
