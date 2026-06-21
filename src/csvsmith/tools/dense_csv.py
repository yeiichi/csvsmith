from __future__ import annotations

import csv
import hashlib
import json
import os
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


MAP_FORMAT = "csvsmith.dense-map"
MAP_VERSION = 1
HASH_ALGORITHM = "sha256"
TOKEN_PREFIX = f"csvsmith:{HASH_ALGORITHM}:"


@dataclass(frozen=True)
class ConcentrateResult:
    """Summary of a completed CSV concentration operation."""

    row_count: int
    transformed_cell_count: int
    mapped_value_count: int
    output_csv_path: Path
    output_map_path: Path


@dataclass(frozen=True)
class RehydrateResult:
    """Summary of a completed CSV rehydration operation."""

    row_count: int
    restored_cell_count: int
    output_csv_path: Path


def generate_hash(text: str) -> str:
    """Return a deterministic SHA-256 hexadecimal digest for text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_distinct_paths(*paths: Path) -> None:
    resolved = [path.expanduser().resolve() for path in paths]
    if len(resolved) != len(set(resolved)):
        raise ValueError("Input, output, and map paths must all be different.")


def _read_header(path: Path, *, encoding: str) -> list[str]:
    with path.open("r", encoding=encoding, newline="") as infile:
        header = next(csv.reader(infile), None)

    if not header:
        raise ValueError(f"Empty CSV: {path}")
    return header


def _resolve_target_columns(
    header: Sequence[str],
    columns: Sequence[str] | None,
) -> list[int]:
    if columns is None:
        return list(range(len(header)))

    requested = list(dict.fromkeys(columns))
    missing = [column for column in requested if column not in header]
    if missing:
        names = ", ".join(repr(column) for column in missing)
        raise ValueError(f"Columns not found in CSV header: {names}")

    duplicate_names = {
        column for column in requested if header.count(column) > 1
    }
    if duplicate_names:
        names = ", ".join(repr(column) for column in sorted(duplicate_names))
        raise ValueError(f"Selected column names are duplicated in the CSV header: {names}")

    return [header.index(column) for column in requested]


def _count_values(
    input_path: Path,
    *,
    target_indices: Sequence[int],
    encoding: str,
) -> Counter[str]:
    counts: Counter[str] = Counter()
    with input_path.open("r", encoding=encoding, newline="") as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            for index in target_indices:
                if index < len(row) and row[index].strip():
                    counts[row[index]] += 1
    return counts


def _temporary_path(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
    )
    os.close(file_descriptor)
    return Path(temporary_name)


def _replace_outputs(
    temporary_outputs: Iterable[tuple[Path, Path]],
) -> None:
    pending = list(temporary_outputs)
    try:
        for temporary_path, destination in pending:
            os.replace(temporary_path, destination)
    finally:
        for temporary_path, _ in pending:
            temporary_path.unlink(missing_ok=True)


def concentrate_csv(
    input_path: Path | str,
    output_csv_path: Path | str,
    output_map_path: Path | str,
    *,
    columns: Sequence[str] | None = None,
    min_occurrences: int = 2,
    encoding: str = "utf-8-sig",
) -> ConcentrateResult:
    """Replace repeated values in selected CSV columns with deterministic tokens.

    The output map is versioned and records the source header and transformed
    column indices so that rehydration can validate its input.
    """
    if min_occurrences < 2:
        raise ValueError("min_occurrences must be at least 2.")

    input_path = Path(input_path)
    output_csv_path = Path(output_csv_path)
    output_map_path = Path(output_map_path)
    _validate_distinct_paths(input_path, output_csv_path, output_map_path)

    header = _read_header(input_path, encoding=encoding)
    target_indices = _resolve_target_columns(header, columns)
    value_counts = _count_values(
        input_path,
        target_indices=target_indices,
        encoding=encoding,
    )
    values_to_map = {
        value
        for value, count in value_counts.items()
        if count >= min_occurrences
    }

    temporary_csv = _temporary_path(output_csv_path)
    try:
        temporary_map = _temporary_path(output_map_path)
    except Exception:
        temporary_csv.unlink(missing_ok=True)
        raise
    value_map: dict[str, str] = {}
    row_count = 0
    transformed_cell_count = 0

    try:
        with input_path.open("r", encoding=encoding, newline="") as infile, (
            temporary_csv.open("w", encoding=encoding, newline="")
        ) as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(next(reader))

            for row in reader:
                row_count += 1
                output_row = list(row)
                for index in target_indices:
                    if index >= len(row) or row[index] not in values_to_map:
                        continue

                    digest = generate_hash(row[index])
                    existing_value = value_map.get(digest)
                    if existing_value is not None and existing_value != row[index]:
                        raise ValueError(f"SHA-256 collision detected for digest: {digest}")

                    value_map[digest] = row[index]
                    output_row[index] = f"{TOKEN_PREFIX}{digest}"
                    transformed_cell_count += 1

                writer.writerow(output_row)

        map_data = {
            "format": MAP_FORMAT,
            "version": MAP_VERSION,
            "algorithm": HASH_ALGORITHM,
            "token_prefix": TOKEN_PREFIX,
            "header": header,
            "columns": [
                {"index": index, "name": header[index]}
                for index in target_indices
            ],
            "values": value_map,
        }
        with temporary_map.open("w", encoding="utf-8") as mapfile:
            json.dump(map_data, mapfile, indent=2, ensure_ascii=False)
            mapfile.write("\n")

        _replace_outputs(
            [
                (temporary_csv, output_csv_path),
                (temporary_map, output_map_path),
            ]
        )
    except Exception:
        temporary_csv.unlink(missing_ok=True)
        temporary_map.unlink(missing_ok=True)
        raise

    return ConcentrateResult(
        row_count=row_count,
        transformed_cell_count=transformed_cell_count,
        mapped_value_count=len(value_map),
        output_csv_path=output_csv_path,
        output_map_path=output_map_path,
    )


def _load_map(map_path: Path) -> Mapping[str, Any]:
    with map_path.open("r", encoding="utf-8") as mapfile:
        data = json.load(mapfile)

    if not isinstance(data, dict):
        raise ValueError("Dense CSV map must be a JSON object.")
    if data.get("format") != MAP_FORMAT or data.get("version") != MAP_VERSION:
        raise ValueError("Unsupported dense CSV map format or version.")
    if data.get("algorithm") != HASH_ALGORITHM:
        raise ValueError("Unsupported dense CSV map hash algorithm.")
    if data.get("token_prefix") != TOKEN_PREFIX:
        raise ValueError("Dense CSV map has an unexpected token prefix.")
    header = data.get("header")
    if not isinstance(header, list) or not all(
        isinstance(column, str) for column in header
    ):
        raise ValueError("Dense CSV map header is invalid.")
    if not isinstance(data.get("columns"), list):
        raise ValueError("Dense CSV map columns are invalid.")
    values = data.get("values")
    if not isinstance(values, dict) or not all(
        isinstance(digest, str)
        and len(digest) == 64
        and all(character in "0123456789abcdef" for character in digest)
        and isinstance(value, str)
        and generate_hash(value) == digest
        for digest, value in values.items()
    ):
        raise ValueError("Dense CSV map values are invalid.")
    return data


def _map_column_indices(
    columns: Sequence[object],
    header: Sequence[str],
) -> list[int]:
    indices: list[int] = []
    for column in columns:
        if not isinstance(column, dict):
            raise ValueError("Dense CSV map contains invalid column metadata.")

        index = column.get("index")
        name = column.get("name")
        if (
            not isinstance(index, int)
            or isinstance(index, bool)
            or not 0 <= index < len(header)
            or name != header[index]
        ):
            raise ValueError("Dense CSV map column metadata does not match its header.")
        indices.append(index)
    if len(indices) != len(set(indices)):
        raise ValueError("Dense CSV map contains duplicate column metadata.")
    return indices


def rehydrate_csv(
    input_csv_path: Path | str,
    map_path: Path | str,
    output_csv_path: Path | str,
    *,
    encoding: str = "utf-8-sig",
) -> RehydrateResult:
    """Restore tokenized cells using a validated dense CSV map."""
    input_csv_path = Path(input_csv_path)
    map_path = Path(map_path)
    output_csv_path = Path(output_csv_path)
    _validate_distinct_paths(input_csv_path, map_path, output_csv_path)

    map_data = _load_map(map_path)
    header = _read_header(input_csv_path, encoding=encoding)
    if header != map_data["header"]:
        raise ValueError("Concentrated CSV header does not match the dense CSV map.")

    target_indices = _map_column_indices(map_data["columns"], header)
    value_map = map_data["values"]
    temporary_csv = _temporary_path(output_csv_path)
    row_count = 0
    restored_cell_count = 0

    try:
        with input_csv_path.open("r", encoding=encoding, newline="") as infile, (
            temporary_csv.open("w", encoding=encoding, newline="")
        ) as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(next(reader))

            for row in reader:
                row_count += 1
                output_row = list(row)
                for index in target_indices:
                    if index >= len(row) or not row[index].startswith(TOKEN_PREFIX):
                        continue

                    digest = row[index][len(TOKEN_PREFIX) :]
                    original_value = value_map.get(digest)
                    if not isinstance(original_value, str):
                        raise ValueError(
                            f"Dense CSV token is missing from the map: {row[index]}"
                        )
                    if generate_hash(original_value) != digest:
                        raise ValueError(f"Dense CSV map has an invalid digest: {digest}")

                    output_row[index] = original_value
                    restored_cell_count += 1

                writer.writerow(output_row)

        _replace_outputs([(temporary_csv, output_csv_path)])
    except Exception:
        temporary_csv.unlink(missing_ok=True)
        raise

    return RehydrateResult(
        row_count=row_count,
        restored_cell_count=restored_cell_count,
        output_csv_path=output_csv_path,
    )
