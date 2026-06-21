import csv
import json
from pathlib import Path

import pytest

from csvsmith.tools.dense_csv import (
    MAP_FORMAT,
    MAP_VERSION,
    TOKEN_PREFIX,
    concentrate_csv,
    generate_hash,
    rehydrate_csv,
)


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as outfile:
        csv.writer(outfile).writerows(rows)


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as infile:
        return list(csv.reader(infile))


def test_concentrate_and_rehydrate_round_trip(tmp_path):
    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    restored = tmp_path / "restored.csv"
    repeated = "A long repeated description " * 5
    rows = [
        ["id", "description"],
        ["1", repeated],
        ["2", "unique"],
        ["3", repeated],
    ]
    write_csv(source, rows)

    concentrate_result = concentrate_csv(source, concentrated, map_path)

    token = f"{TOKEN_PREFIX}{generate_hash(repeated)}"
    assert read_csv(concentrated) == [
        ["id", "description"],
        ["1", token],
        ["2", "unique"],
        ["3", token],
    ]
    assert concentrate_result.row_count == 3
    assert concentrate_result.transformed_cell_count == 2
    assert concentrate_result.mapped_value_count == 1

    map_data = json.loads(map_path.read_text(encoding="utf-8"))
    assert map_data["format"] == MAP_FORMAT
    assert map_data["version"] == MAP_VERSION
    assert map_data["header"] == ["id", "description"]
    assert map_data["columns"] == [
        {"index": 0, "name": "id"},
        {"index": 1, "name": "description"},
    ]

    rehydrate_result = rehydrate_csv(concentrated, map_path, restored)

    assert read_csv(restored) == rows
    assert rehydrate_result.row_count == 3
    assert rehydrate_result.restored_cell_count == 2


def test_concentrate_only_selected_repeated_columns(tmp_path):
    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    write_csv(
        source,
        [
            ["id", "description"],
            ["same-id", "same-description"],
            ["same-id", "same-description"],
        ],
    )

    concentrate_csv(
        source,
        concentrated,
        map_path,
        columns=["description"],
    )

    rows = read_csv(concentrated)
    assert rows[1][0] == "same-id"
    assert rows[2][0] == "same-id"
    assert rows[1][1].startswith(TOKEN_PREFIX)
    assert rows[2][1] == rows[1][1]


def test_concentrate_respects_min_occurrences(tmp_path):
    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    rows = [["value"], ["same"], ["same"]]
    write_csv(source, rows)

    result = concentrate_csv(
        source,
        concentrated,
        map_path,
        min_occurrences=3,
    )

    assert read_csv(concentrated) == rows
    assert result.transformed_cell_count == 0
    assert result.mapped_value_count == 0


@pytest.mark.parametrize(
    ("input_name", "output_name", "map_name"),
    [
        ("data.csv", "data.csv", "map.json"),
        ("data.csv", "out.csv", "data.csv"),
        ("data.csv", "out.csv", "out.csv"),
    ],
)
def test_concentrate_rejects_path_collisions_without_truncating_input(
    tmp_path,
    input_name,
    output_name,
    map_name,
):
    source = tmp_path / input_name
    original = "value\noriginal\n"
    source.write_text(original, encoding="utf-8")

    with pytest.raises(ValueError, match="must all be different"):
        concentrate_csv(
            source,
            tmp_path / output_name,
            tmp_path / map_name,
        )

    assert source.read_text(encoding="utf-8") == original


def test_concentrate_rejects_missing_and_ambiguous_columns(tmp_path):
    missing_source = tmp_path / "missing.csv"
    duplicate_source = tmp_path / "duplicate.csv"
    write_csv(missing_source, [["id"], ["1"]])
    write_csv(duplicate_source, [["name", "name"], ["A", "B"]])

    with pytest.raises(ValueError, match="Columns not found"):
        concentrate_csv(
            missing_source,
            tmp_path / "missing-out.csv",
            tmp_path / "missing-map.json",
            columns=["description"],
        )

    with pytest.raises(ValueError, match="duplicated"):
        concentrate_csv(
            duplicate_source,
            tmp_path / "duplicate-out.csv",
            tmp_path / "duplicate-map.json",
            columns=["name"],
        )


def test_rehydrate_only_changes_recorded_columns(tmp_path):
    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    restored = tmp_path / "restored.csv"
    repeated = "repeated"
    write_csv(
        source,
        [
            ["plain", "dense"],
            [generate_hash(repeated), repeated],
            [generate_hash(repeated), repeated],
        ],
    )

    concentrate_csv(
        source,
        concentrated,
        map_path,
        columns=["dense"],
    )
    rehydrate_csv(concentrated, map_path, restored)

    assert read_csv(restored) == read_csv(source)


def test_rehydrate_rejects_wrong_header_and_invalid_map(tmp_path):
    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    restored = tmp_path / "restored.csv"
    write_csv(source, [["value"], ["same"], ["same"]])
    concentrate_csv(source, concentrated, map_path)

    write_csv(concentrated, [["different"], ["same"]])
    with pytest.raises(ValueError, match="header does not match"):
        rehydrate_csv(concentrated, map_path, restored)

    map_path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        rehydrate_csv(source, map_path, restored)


def test_rehydrate_rejects_invalid_map_values(tmp_path):
    source = tmp_path / "source.csv"
    map_path = tmp_path / "dense-map.json"
    restored = tmp_path / "restored.csv"
    write_csv(source, [["value"], ["plain"]])
    map_path.write_text(
        json.dumps(
            {
                "format": MAP_FORMAT,
                "version": MAP_VERSION,
                "algorithm": "sha256",
                "token_prefix": TOKEN_PREFIX,
                "header": ["value"],
                "columns": [{"index": 0, "name": "value"}],
                "values": {"0" * 64: "value with a different digest"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="map values are invalid"):
        rehydrate_csv(source, map_path, restored)


def test_failed_concentrate_does_not_replace_existing_outputs(tmp_path):
    source = tmp_path / "empty.csv"
    output = tmp_path / "output.csv"
    map_path = tmp_path / "map.json"
    source.write_text("", encoding="utf-8")
    output.write_text("existing output", encoding="utf-8")
    map_path.write_text("existing map", encoding="utf-8")

    with pytest.raises(ValueError, match="Empty CSV"):
        concentrate_csv(source, output, map_path)

    assert output.read_text(encoding="utf-8") == "existing output"
    assert map_path.read_text(encoding="utf-8") == "existing map"


def test_dense_csv_cli_round_trip(tmp_path, capsys):
    from csvsmith.cli import main

    source = tmp_path / "source.csv"
    concentrated = tmp_path / "concentrated.csv"
    map_path = tmp_path / "dense-map.json"
    restored = tmp_path / "restored.csv"
    rows = [["value"], ["same"], ["same"]]
    write_csv(source, rows)

    concentrate_exit_code = main(
        [
            "concentrate",
            str(source),
            "-o",
            str(concentrated),
            "-m",
            str(map_path),
        ]
    )
    rehydrate_exit_code = main(
        [
            "rehydrate",
            str(concentrated),
            "-m",
            str(map_path),
            "-o",
            str(restored),
        ]
    )

    assert concentrate_exit_code == 0
    assert rehydrate_exit_code == 0
    assert read_csv(restored) == rows
    captured = capsys.readouterr()
    assert "Wrote concentrated CSV to:" in captured.out
    assert (
        "Potential repeated-operation reduction for mapped values: 1/2 (50.0%)"
        in captured.out
    )
    assert "Wrote rehydrated CSV to:" in captured.out


def test_concentrate_cli_uses_input_derived_output_paths(tmp_path, capsys):
    from csvsmith.cli import main

    source = tmp_path / "source.export.csv"
    rows = [["value"], ["same"], ["same"]]
    write_csv(source, rows)

    exit_code = main(["concentrate", str(source)])

    concentrated = tmp_path / "source.export.dense.csv"
    map_path = tmp_path / "source.export.dense-map.json"
    assert exit_code == 0
    assert concentrated.exists()
    assert map_path.exists()
    captured = capsys.readouterr()
    assert str(concentrated) in captured.out
    assert str(map_path) in captured.out
    assert (
        "Potential repeated-operation reduction for mapped values: 1/2 (50.0%)"
        in captured.out
    )


def test_dense_csv_cli_reports_api_errors(tmp_path, capsys):
    from csvsmith.cli import main

    source = tmp_path / "source.csv"
    write_csv(source, [["value"], ["same"], ["same"]])

    exit_code = main(
        [
            "concentrate",
            str(source),
            "-o",
            str(source),
            "-m",
            str(tmp_path / "map.json"),
        ]
    )

    assert exit_code == 1
    assert "must all be different" in capsys.readouterr().err
