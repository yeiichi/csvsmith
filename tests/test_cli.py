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
