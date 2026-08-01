import csv
from decimal import Decimal

import pytest

from csvsmith.tools.knapsack_csv import (
    find_knapsack_indices,
    mark_knapsack_csv,
    read_column_values,
    run_knapsack,
)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as outfile:
        csv.writer(outfile).writerows(rows)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as infile:
        return list(csv.DictReader(infile))


def test_run_knapsack_returns_indices_for_best_sum():
    best_sum, indices = run_knapsack([6, 4, 5, 3], 10)

    assert best_sum == 10
    assert indices == [0, 1]


def test_find_knapsack_indices_parses_grouped_decimal_values(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(
        source,
        [
            ["id", "value"],
            ["1", "905.722"],
            ["2", "961.687"],
            ["3", "1,074.301"],
            ["4", "713.513"],
        ],
    )

    assert find_knapsack_indices(source, "value", "2,036") == [1, 2]


def test_mark_knapsack_csv_adds_marker_column(tmp_path):
    source = tmp_path / "sample.csv"
    output = tmp_path / "marked.csv"
    write_csv(
        source,
        [
            ["id", "value"],
            ["1", "905.722"],
            ["2", "961.687"],
            ["3", "1,074.301"],
            ["4", "713.513"],
        ],
    )

    result = mark_knapsack_csv(
        source,
        "value",
        "2,036",
        output,
        mark_column="selected",
        mark_value="knapsack",
    )

    rows = read_csv(output)
    assert result.best_sum == Decimal("2035.988")
    assert result.selected_indices == [1, 2]
    assert result.mark_column == "selected"
    assert [row["selected"] for row in rows] == ["", "knapsack", "knapsack", ""]


def test_mark_knapsack_csv_uses_default_output_and_column(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["id", "value"], ["1", "10"], ["2", "20"]])

    result = mark_knapsack_csv(source, "value", 10)

    assert result.output_path == tmp_path / "sample.knapsack.csv"
    assert result.mark_column == "value_knapsack"
    assert read_csv(result.output_path)[0]["value_knapsack"] == "yes"


def test_read_column_values_rejects_missing_column(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["id", "value"], ["1", "10"]])

    with pytest.raises(ValueError, match="Column not found"):
        read_column_values(source, "missing")


def test_mark_knapsack_csv_rejects_invalid_numbers(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["id", "value"], ["1", "not-a-number"]])

    with pytest.raises(ValueError, match="Could not parse row 1"):
        mark_knapsack_csv(source, "value", 10)


def test_mark_knapsack_csv_rejects_existing_marker_column(tmp_path):
    source = tmp_path / "sample.csv"
    write_csv(source, [["id", "value", "value_knapsack"], ["1", "10", ""]])

    with pytest.raises(ValueError, match="already exists"):
        mark_knapsack_csv(source, "value", 10)
