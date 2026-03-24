from __future__ import annotations

import csv
from pathlib import Path
from typing import Generator


class DropRowsBySubstring:
    """
    Clean CSV rows by removing rows whose selected column contains a target substring.
    """

    CLEAN_SUFFIX = ".clean.csv"

    def __init__(
        self,
        csv_path: Path | str,
        column_name: str,
        unwanted_text: str,
        *,
        case_sensitive: bool = True,
        keep_header: bool = True,
    ) -> None:
        self.csv_path = Path(csv_path)
        self.column_name = str(column_name)
        self.unwanted_text = str(unwanted_text)
        self.case_sensitive = case_sensitive
        self.keep_header = keep_header

    def _find_column_index(self, header: list[str]) -> int:
        try:
            return header.index(self.column_name)
        except ValueError as exc:
            raise ValueError(f"Column not found in CSV header: {self.column_name!r}") from exc

    def _row_contains_unwanted_text(self, row: list[str], column_index: int) -> bool:
        if column_index >= len(row):
            return False

        cell_value = row[column_index]
        needle = self.unwanted_text

        if not self.case_sensitive:
            return needle.casefold() in cell_value.casefold()

        return needle in cell_value

    def _row_is_kept(self, row: list[str], column_index: int) -> bool:
        return not self._row_contains_unwanted_text(row, column_index)

    def _iter_rows_to_write(self) -> Generator[list[str], None, None]:
        with self.csv_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            header = next(reader, None)
            if header is None:
                return

            column_index = self._find_column_index(header)

            if self.keep_header:
                yield header

            for row in reader:
                if not row:
                    continue
                if self._row_is_kept(row, column_index):
                    yield row

    def iter_kept_rows(self) -> Generator[list[str], None, None]:
        yield from self._iter_rows_to_write()

    def write_filtered_rows(self) -> None:
        output_path = self.csv_path.with_suffix(self.CLEAN_SUFFIX)
        if output_path == self.csv_path:
            raise ValueError("Output path would overwrite the input file")

        with output_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            for row in self._iter_rows_to_write():
                writer.writerow(row)


CSVCleaner = DropRowsBySubstring


def main(csv_path: Path | str, column_name: str, unwanted_text: str) -> None:
    cleaner = DropRowsBySubstring(csv_path, column_name, unwanted_text)
    cleaner.write_filtered_rows()
