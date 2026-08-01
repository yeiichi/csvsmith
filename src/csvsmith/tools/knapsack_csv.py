from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from ..utils.clean_numeric import clean_numeric


DEFAULT_MARK_VALUE = "yes"


@dataclass(frozen=True)
class KnapsackCSVResult:
    """Summary of a CSV knapsack marking operation."""

    best_sum: Decimal
    selected_indices: list[int]
    output_path: Path
    mark_column: str


def _decimal_places(value: Decimal) -> int:
    exponent = value.as_tuple().exponent
    return abs(exponent) if exponent < 0 else 0


def _parse_decimal(value: Any) -> Decimal:
    cleaned = clean_numeric(value)
    return Decimal(str(cleaned))


def _scale_decimals(values: list[Decimal], capacity: Decimal) -> tuple[list[int], int, int]:
    scale_places = max([_decimal_places(value) for value in values] + [_decimal_places(capacity)])
    scale = 10**scale_places
    scaled_values = [int(value * scale) for value in values]
    scaled_capacity = int(capacity * scale)
    return scaled_values, scaled_capacity, scale


def run_knapsack(values: list[int], capacity: int) -> tuple[int, list[int]]:
    """Return the largest reachable sum and selected value indices."""
    if capacity < 0:
        raise ValueError("capacity must be non-negative")

    filtered = [(index, value) for index, value in enumerate(values) if 0 < value <= capacity]
    reachable = [False] * (capacity + 1)
    parent = [-1] * (capacity + 1)
    reachable[0] = True

    for filtered_index, (_, value) in enumerate(filtered):
        for subtotal in range(capacity, value - 1, -1):
            if not reachable[subtotal] and reachable[subtotal - value]:
                reachable[subtotal] = True
                parent[subtotal] = filtered_index

    best_sum = next(subtotal for subtotal in range(capacity, -1, -1) if reachable[subtotal])
    selected_indices: list[int] = []
    subtotal = best_sum
    while subtotal > 0:
        filtered_index = parent[subtotal]
        if filtered_index == -1:
            break
        original_index, value = filtered[filtered_index]
        selected_indices.append(original_index)
        subtotal -= value

    return best_sum, sorted(selected_indices)


def read_column_values(csv_path: str | Path, target_column: str) -> list[Decimal]:
    """Read and normalize numeric values from a CSV column."""
    csv_path = Path(csv_path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            raise ValueError(f"Empty CSV: {csv_path}")
        if target_column not in reader.fieldnames:
            raise ValueError(f"Column not found in CSV header: {target_column!r}")

        values = []
        for row_index, row in enumerate(reader, start=1):
            try:
                values.append(_parse_decimal(row[target_column]))
            except ValueError as exc:
                value = row[target_column]
                raise ValueError(
                    f"Could not parse row {row_index} column {target_column!r}: {value!r}"
                ) from exc

    return values


def find_knapsack_indices(
    csv_path: str | Path,
    target_column: str,
    capacity: int | float | str | Decimal,
) -> list[int]:
    """Return row indices whose target values maximize a sum not exceeding capacity."""
    values = read_column_values(csv_path, target_column)
    capacity_value = _parse_decimal(capacity)
    if capacity_value < 0:
        raise ValueError("capacity must be non-negative")

    scaled_values, scaled_capacity, _ = _scale_decimals(values, capacity_value)
    _, selected_indices = run_knapsack(scaled_values, scaled_capacity)
    return selected_indices


def mark_knapsack_csv(
    csv_path: str | Path,
    target_column: str,
    capacity: int | float | str | Decimal,
    output_path: str | Path | None = None,
    *,
    mark_column: str | None = None,
    mark_value: str = DEFAULT_MARK_VALUE,
) -> KnapsackCSVResult:
    """Write a CSV copy with a marker column for selected knapsack rows."""
    csv_path = Path(csv_path)
    output_path = (
        Path(output_path)
        if output_path
        else csv_path.with_name(f"{csv_path.stem}.knapsack.csv")
    )
    mark_column = mark_column or f"{target_column}_knapsack"

    with csv_path.open("r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            raise ValueError(f"Empty CSV: {csv_path}")
        if target_column not in reader.fieldnames:
            raise ValueError(f"Column not found in CSV header: {target_column!r}")
        if mark_column in reader.fieldnames:
            raise ValueError(f"Output mark column already exists: {mark_column!r}")
        rows = list(reader)

    values = []
    for row_index, row in enumerate(rows, start=1):
        try:
            values.append(_parse_decimal(row[target_column]))
        except ValueError as exc:
            value = row[target_column]
            raise ValueError(
                f"Could not parse row {row_index} column {target_column!r}: {value!r}"
            ) from exc

    capacity_value = _parse_decimal(capacity)
    if capacity_value < 0:
        raise ValueError("capacity must be non-negative")

    scaled_values, scaled_capacity, scale = _scale_decimals(values, capacity_value)
    best_sum, selected_indices = run_knapsack(scaled_values, scaled_capacity)
    selected_index_set = set(selected_indices)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [*reader.fieldnames, mark_column]
    with output_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row_index, row in enumerate(rows):
            output_row = dict(row)
            output_row[mark_column] = mark_value if row_index in selected_index_set else ""
            writer.writerow(output_row)

    return KnapsackCSVResult(
        best_sum=Decimal(best_sum) / Decimal(scale),
        selected_indices=selected_indices,
        output_path=output_path,
        mark_column=mark_column,
    )
