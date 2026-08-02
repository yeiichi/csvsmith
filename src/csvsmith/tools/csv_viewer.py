from __future__ import annotations

import csv
import operator
from pathlib import Path
from typing import Any, Callable, TextIO


OPERATORS: dict[str, Callable[[Any, Any], bool]] = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


class DataFrame:
    """A lightweight in-memory CSV table for inspection and simple filtering."""

    def __init__(self, data: dict[str, list[Any]]) -> None:
        self._data = data
        self.columns = list(data)

    @classmethod
    def from_csv(
        cls,
        filepath: str | Path,
        *,
        convert_types: bool = True,
    ) -> DataFrame:
        """Read a CSV file into a column-oriented ``DataFrame``."""
        with Path(filepath).open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames or []
            data: dict[str, list[Any]] = {column: [] for column in fieldnames}

            for row in reader:
                for column in fieldnames:
                    value = row.get(column)
                    if convert_types:
                        value = infer_type(value)
                    data[column].append(value)

        return cls(data)

    def render(self, *, start: int = 0, end: int | None = None) -> str:
        """Return rows from ``start`` up to ``end`` formatted as a text table."""
        start = max(start, 0)
        end = len(self) if end is None else min(end, len(self))
        if start >= end or not self.columns:
            return ""

        row_indexes = range(start, end)
        widths = {column: len(column) for column in self.columns}
        for column in self.columns:
            for index in row_indexes:
                widths[column] = max(widths[column], len(str(self._data[column][index])))

        lines = [
            " | ".join(f"{column:<{widths[column]}}" for column in self.columns),
            "-+-".join("-" * widths[column] for column in self.columns),
        ]
        for index in row_indexes:
            lines.append(
                " | ".join(
                    f"{str(self._data[column][index]):<{widths[column]}}"
                    for column in self.columns
                )
            )

        return "\n".join(lines)

    def show(
        self,
        *,
        start: int = 0,
        end: int | None = None,
        file: TextIO | None = None,
    ) -> None:
        """Print rows from ``start`` up to ``end`` as a text table."""
        rendered = self.render(start=start, end=end)
        if rendered:
            print(rendered, file=file)

    def head(self, n: int = 5) -> str:
        """Return the first ``n`` rows formatted as a text table."""
        return self.render(end=n)

    def select(self, columns: list[str]) -> DataFrame:
        """Return a new ``DataFrame`` with the selected columns."""
        missing = [column for column in columns if column not in self._data]
        if missing:
            raise KeyError(", ".join(missing))
        return DataFrame({column: self._data[column] for column in columns})

    def filter(self, condition_func: Callable[[dict[str, Any]], bool]) -> DataFrame:
        """Return rows for which ``condition_func`` evaluates to true."""
        filtered_data: dict[str, list[Any]] = {column: [] for column in self.columns}

        for index in range(len(self)):
            row = {column: self._data[column][index] for column in self.columns}
            if condition_func(row):
                for column in self.columns:
                    filtered_data[column].append(self._data[column][index])

        return DataFrame(filtered_data)

    def __getitem__(self, column_name: str) -> list[Any]:
        return self._data[column_name]

    def __setitem__(self, column_name: str, values: list[Any]) -> None:
        if len(values) != len(self):
            raise ValueError(
                f"Length of values ({len(values)}) does not match "
                f"DataFrame length ({len(self)})"
            )
        self._data[column_name] = list(values)
        if column_name not in self.columns:
            self.columns.append(column_name)

    def __len__(self) -> int:
        if not self.columns:
            return 0
        return len(self._data[self.columns[0]])

    def __repr__(self) -> str:
        return f"<DataFrame with {len(self)} rows and {len(self.columns)} columns>"


def infer_type(value: str | None) -> int | float | str | None:
    """Convert strings to ``int`` or ``float`` when possible."""
    if value is None:
        return None

    stripped = value.strip()
    try:
        return int(stripped)
    except ValueError:
        pass

    try:
        return float(stripped)
    except ValueError:
        return stripped


def build_filter(column: str, op: str, raw_value: str) -> Callable[[dict[str, Any]], bool]:
    """Build a row predicate from a column, operator, and comparison value."""
    if op not in OPERATORS:
        allowed = ", ".join(OPERATORS)
        raise ValueError(f"Unsupported operator {op!r}. Use one of: {allowed}.")

    expected = infer_type(raw_value)
    compare = OPERATORS[op]

    def row_matches(row: dict[str, Any]) -> bool:
        if column not in row:
            raise KeyError(column)

        actual = row[column]
        try:
            return compare(actual, expected)
        except TypeError:
            return compare(str(actual), str(expected))

    return row_matches
