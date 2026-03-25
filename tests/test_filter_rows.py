from pathlib import Path

import pytest

from csvsmith.filter_rows import DropRowsBySubstring


def test_write_filtered_rows_keeps_header_and_filters_matching_rows(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "id,name,notes\n"
        "1,Alice,ok\n"
        "2,Bob,contains spam here\n"
        "3,Carol,ok\n",
        encoding="utf-8",
    )

    cleaner = DropRowsBySubstring(csv_path, column_name="notes", unwanted_text="spam")
    cleaner.write_filtered_rows()

    output_path = tmp_path / "input.filtered.csv"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == (
        "id,name,notes\n"
        "1,Alice,ok\n"
        "3,Carol,ok\n"
    )


def test_iter_kept_rows_keeps_header_and_skips_matching_rows(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "id,name,notes\n"
        "1,Alice,ok\n"
        "2,Bob,contains spam here\n"
        "3,Carol,ok\n",
        encoding="utf-8",
    )

    cleaner = DropRowsBySubstring(csv_path, column_name="notes", unwanted_text="spam")
    rows = list(cleaner.iter_kept_rows())

    assert rows == [
        ["id", "name", "notes"],
        ["1", "Alice", "ok"],
        ["3", "Carol", "ok"],
    ]


def test_case_insensitive_matching_when_disabled_case_sensitivity(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "id,name,notes\n"
        "1,Alice,Spam message\n"
        "2,Bob,ok\n",
        encoding="utf-8",
    )

    cleaner = DropRowsBySubstring(
        csv_path,
        column_name="notes",
        unwanted_text="spam",
        case_sensitive=False,
    )
    rows = list(cleaner.iter_kept_rows())

    assert rows == [
        ["id", "name", "notes"],
        ["2", "Bob", "ok"],
    ]


def test_short_rows_do_not_crash_and_are_kept_when_column_is_missing(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "id,name,notes\n"
        "1,Alice,ok\n"
        "2,Bob\n"
        "3,Carol,ok\n",
        encoding="utf-8",
    )

    cleaner = DropRowsBySubstring(csv_path, column_name="notes", unwanted_text="spam")
    rows = list(cleaner.iter_kept_rows())

    assert rows == [
        ["id", "name", "notes"],
        ["1", "Alice", "ok"],
        ["2", "Bob"],
        ["3", "Carol", "ok"],
    ]


def test_missing_column_name_raises_value_error(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("id,name\n1,Alice\n", encoding="utf-8")

    cleaner = DropRowsBySubstring(csv_path, column_name="notes", unwanted_text="spam")

    with pytest.raises(ValueError, match="Column not found in CSV header"):
        list(cleaner.iter_kept_rows())


def test_write_filtered_rows_raises_if_output_would_overwrite_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("id,name\n1,Alice\n", encoding="utf-8")

    cleaner = DropRowsBySubstring(csv_path, column_name="name", unwanted_text="x")

    monkeypatch.setattr(cleaner, "FILTERED_SUFFIX", ".csv")

    with pytest.raises(ValueError, match="Output path would overwrite the input file"):
        cleaner.write_filtered_rows()


def test_empty_lines_are_skipped(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "id,name,notes\n"
        "\n"
        "1,Alice,ok\n"
        "\n"
        "2,Bob,ok\n",
        encoding="utf-8",
    )

    cleaner = DropRowsBySubstring(csv_path, column_name="notes", unwanted_text="spam")
    rows = list(cleaner.iter_kept_rows())

    assert rows == [
        ["id", "name", "notes"],
        ["1", "Alice", "ok"],
        ["2", "Bob", "ok"],
    ]