from __future__ import annotations

import csv
from pathlib import Path
from ..utils.io import _open_worksheet, write_worksheet_to_csv


def _resolve_csv_path(excel_path: Path, csv_path: str | Path | None) -> Path:
    """Return the output CSV path, defaulting to the Excel file's stem."""
    return Path(csv_path) if csv_path else excel_path.with_suffix(".csv")


def excel_to_csv(
    excel_path: str | Path,
    csv_path: str | Path | None = None,
    *,
    sheet_name: str | None = None,
) -> Path:
    """Convert one Excel worksheet into a CSV file."""
    excel_path = Path(excel_path)
    csv_path = _resolve_csv_path(excel_path, csv_path)

    with _open_worksheet(excel_path, sheet_name=sheet_name) as worksheet:
        write_worksheet_to_csv(worksheet, csv_path)

    return csv_path