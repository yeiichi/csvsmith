import csv
from pathlib import Path

import pytest

from csvsmith.cli import main
from csvsmith.tools.csv_viewer import DataFrame, build_filter, infer_type


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as outfile:
        csv.writer(outfile).writerows(rows)


def test_dataframe_reads_csv_and_infers_numeric_types(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["name", "value"], ["Alice", "12"], ["Bob", "13.5"]])

    df = DataFrame.from_csv(source)

    assert df.columns == ["name", "value"]
    assert df["name"] == ["Alice", "Bob"]
    assert df["value"] == [12, 13.5]
    assert repr(df) == "<DataFrame with 2 rows and 2 columns>"


def test_dataframe_reads_utf8_bom_csv_headers(tmp_path):
    source = tmp_path / "sample.csv"
    with source.open("w", encoding="utf-8-sig", newline="") as outfile:
        csv.writer(outfile).writerows([["name", "value"], ["Alice", "12"]])

    df = DataFrame.from_csv(source)

    assert df.columns == ["name", "value"]
    assert df["name"] == ["Alice"]


def test_dataframe_can_keep_values_as_strings(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["id"], ["001"]])

    df = DataFrame.from_csv(source, convert_types=False)

    assert df["id"] == ["001"]


def test_dataframe_render_select_and_head(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(
        source,
        [
            ["name", "score", "city"],
            ["Alice", "10", "Tokyo"],
            ["Bob", "8", "Osaka"],
        ],
    )

    df = DataFrame.from_csv(source).select(["name", "score"])

    assert df.head(1) == "name  | score\n------+------\nAlice | 10   "
    assert df.render(start=1) == "name | score\n-----+------\nBob  | 8    "


def test_dataframe_filter_supports_numeric_comparisons(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["name", "score"], ["Alice", "10"], ["Bob", "8"]])

    df = DataFrame.from_csv(source).filter(build_filter("score", ">", "8"))

    assert df["name"] == ["Alice"]


def test_dataframe_to_csv_returns_csv_string(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(
        source,
        [
            ["name", "score", "note"],
            ["Alice", "10", "Hello, Tokyo"],
            ["Bob", "8", "Line\nbreak"],
        ],
    )

    df = DataFrame.from_csv(source).filter(build_filter("score", ">", "7"))

    assert (
        df.to_csv()
        == 'name,score,note\r\nAlice,10,"Hello, Tokyo"\r\nBob,8,"Line\nbreak"\r\n'
    )


def test_dataframe_to_csv_writes_csv_file(tmp_path):
    source = tmp_path / "sample.csv"
    output = tmp_path / "exports" / "filtered.csv"
    write_csv(
        source,
        [
            ["name", "score", "note"],
            ["Alice", "10", "Hello, Tokyo"],
            ["Bob", "8", "Line\nbreak"],
        ],
    )

    df = DataFrame.from_csv(source).filter(build_filter("score", ">", "8"))

    result = df.to_csv(output)

    assert result == output
    assert output.read_text(encoding="utf-8") == "name,score,note\nAlice,10,\"Hello, Tokyo\"\n"


def test_dataframe_to_csv_round_trips_with_from_csv(tmp_path):
    source = tmp_path / "sample.csv"
    output = tmp_path / "output.csv"
    write_csv(source, [["id", "name"], ["001", "Alice"], ["002", "Bob"]])

    DataFrame.from_csv(source, convert_types=False).to_csv(output)

    round_tripped = DataFrame.from_csv(output, convert_types=False)
    assert round_tripped.columns == ["id", "name"]
    assert round_tripped["id"] == ["001", "002"]
    assert round_tripped["name"] == ["Alice", "Bob"]


def test_view_command_filters_and_selects_columns(tmp_path, capsys):
    source = tmp_path / "sample.csv"
    write_csv(
        source,
        [
            ["name", "score", "city"],
            ["Alice", "10", "Tokyo"],
            ["Bob", "8", "Osaka"],
        ],
    )

    exit_code = main(
        [
            "view",
            str(source),
            "--columns",
            "name,score",
            "--filter",
            "score",
            ">",
            "8",
        ]
    )

    assert exit_code == 0
    assert capsys.readouterr().out == "name  | score\n------+------\nAlice | 10   \n"


def test_dataframe_select_rejects_missing_columns(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["name"], ["Alice"]])

    with pytest.raises(KeyError, match="score"):
        DataFrame.from_csv(source).select(["score"])


def test_build_filter_rejects_unknown_operator():
    with pytest.raises(ValueError, match="Unsupported operator"):
        build_filter("score", "~", "10")


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        (" 12 ", 12),
        ("12.5", 12.5),
        ("Alice", "Alice"),
        (None, None),
    ],
)
def test_infer_type(raw_value, expected):
    assert infer_type(raw_value) == expected
