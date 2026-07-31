import csv

import pytest

from csvsmith.tools.sample_csv import (
    FIELDNAMES,
    build_rows,
    create_date_series,
    create_sample_csv,
    random_item_value,
)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as infile:
        return list(csv.DictReader(infile))


def test_build_rows_uses_expected_shape_and_seed():
    rows = build_rows(row_count=2, start="2026-01-15", seed=123)

    assert list(rows[0]) == FIELDNAMES
    assert rows[0]["id"] == "1"
    assert rows[0]["date"] == "2026-01-15"
    assert rows[1]["id"] == "2"
    assert rows[1]["date"] == "2026-01-16"
    assert rows == build_rows(row_count=2, start="2026-01-15", seed=123)
    assert rows[0]["amount"].startswith("$ ")


def test_create_sample_csv_writes_file(tmp_path):
    output = tmp_path / "nested" / "sample.csv"

    result = create_sample_csv(
        row_count=3,
        start="2026-02-01",
        output_path=output,
        seed=7,
    )

    assert result.row_count == 3
    assert result.output_path == output
    rows = read_csv(output)
    assert len(rows) == 3
    assert rows[0]["date"] == "2026-02-01"


def test_create_sample_csv_allows_header_only_file(tmp_path):
    output = tmp_path / "sample.csv"

    result = create_sample_csv(row_count=0, output_path=output)

    assert result.row_count == 0
    assert output.read_text(encoding="utf-8") == ",".join(FIELDNAMES) + "\n"


def test_kanji_item_charset_uses_non_ascii_characters():
    value = random_item_value(item_charset="kanji", rng=__import__("random").Random(1))

    assert 3 <= len(value) <= 8
    assert all(ord(character) > 127 for character in value)


@pytest.mark.parametrize("row_count", [-1])
def test_rejects_negative_row_count(row_count):
    with pytest.raises(ValueError, match="row_count must be non-negative"):
        create_date_series(row_count)


def test_rejects_unknown_item_charset():
    with pytest.raises(ValueError, match="item_charset"):
        build_rows(row_count=1, item_charset="emoji")
