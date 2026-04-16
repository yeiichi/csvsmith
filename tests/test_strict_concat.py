import csv
from pathlib import Path

import pytest

from csvsmith.tools.strict_concat import strict_concat_rows


def write_csv(path: Path, rows: list[list[str]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def test_strict_concat_happy(tmp_path):
    f1 = tmp_path / "a.csv"
    f2 = tmp_path / "b.csv"

    write_csv(f1, [["id", "name"], ["1", "Alice"]])
    write_csv(f2, [["id", "name"], ["2", "Bob"]])

    rows = strict_concat_rows(tmp_path)

    assert rows == [
        ["file_stem", "id", "name"],
        ["a", "1", "Alice"],
        ["b", "2", "Bob"],
    ]


def test_strict_concat_header_mismatch(tmp_path):
    write_csv(tmp_path / "a.csv", [["id", "name"], ["1", "Alice"]])
    write_csv(tmp_path / "b.csv", [["id", "age"], ["2", "30"]])

    with pytest.raises(ValueError, match="Header mismatch"):
        strict_concat_rows(tmp_path)


def test_strict_concat_empty_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        strict_concat_rows(tmp_path)

    def test_strict_concat_with_non_csv_files(tmp_path):
        # Create sample CSV files.
        write_csv(tmp_path / "a.csv", [["id", "name"], ["1", "Alice"]])
        write_csv(tmp_path / "b.csv", [["id", "name"], ["2", "Bob"]])

        # Create some non-CSV files in the same directory.
        (tmp_path / "file1.txt").write_text("This is a text file.", encoding="utf-8")
        (tmp_path / "file2.doc").write_text("This is a Word document.", encoding="utf-8")

        # Call function and check results ignore non-CSV files.
        rows = strict_concat_rows(tmp_path)
        assert rows == [
            ["file_stem", "id", "name"],
            ["a", "1", "Alice"],
            ["b", "2", "Bob"],
        ]


def test_strict_concat_empty_csv(tmp_path):
    (tmp_path / "a.csv").write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Empty CSV"):
        strict_concat_rows(tmp_path)


def test_header_only_files(tmp_path):
    write_csv(tmp_path / "a.csv", [["id", "name"]])
    write_csv(tmp_path / "b.csv", [["id", "name"]])

    rows = strict_concat_rows(tmp_path)

    assert rows == [["file_stem", "id", "name"]]


def test_strict_concat_cli(tmp_path, capsys):
    from csvsmith.cli import main
    f1 = tmp_path / "a.csv"
    f2 = tmp_path / "b.csv"
    out = tmp_path / "out.csv"

    write_csv(f1, [["id", "name"], ["1", "Alice"]])
    write_csv(f2, [["id", "name"], ["2", "Bob"]])

    exit_code = main(["strict-concat", str(tmp_path), "-o", str(out)])

    assert exit_code == 0
    assert out.exists()
    
    with out.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows == [
        ["file_stem", "id", "name"],
        ["a", "1", "Alice"],
        ["b", "2", "Bob"],
    ]
    
    captured = capsys.readouterr()
    assert "Wrote concatenated CSV to:" in captured.out
