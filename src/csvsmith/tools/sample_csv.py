from __future__ import annotations

import csv
import random
import string
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


MEAN = 1000.0
UPPER_BOUND = 1500.0

CATEGORIES = ["cat_1", "cat_2", "cat_3", "cat_4", "cat_5"]
DEFAULT_ROW_COUNT = 16
DEFAULT_OUTPUT_PATH = "sample.csv"
DEFAULT_ITEM_CHARSET = "ascii"
FIELDNAMES = ["id", "date", "category", "item_1", "item_2", "value", "amount"]

ASCII_CHARS = string.ascii_letters + string.digits
KANJI_CHARS = (
    "日月火水木金土山川田人大小中上下左右本学校会社電車駅東京大阪京都"
)


@dataclass(frozen=True)
class SampleCSVResult:
    """Summary of a generated sample CSV file."""

    row_count: int
    output_path: Path


def create_date_series(row_count: int, start: str | None = None) -> list[date]:
    """Return consecutive dates beginning at ``start`` or today."""
    if row_count < 0:
        raise ValueError("row_count must be non-negative")

    start_date = datetime.fromisoformat(start).date() if start else date.today()
    return [start_date + timedelta(days=offset) for offset in range(row_count)]


def _characters_for_charset(item_charset: str) -> str:
    if item_charset == "ascii":
        return ASCII_CHARS
    if item_charset == "kanji":
        return KANJI_CHARS
    if item_charset == "mix":
        return ASCII_CHARS + KANJI_CHARS

    raise ValueError("item_charset must be one of: ascii, kanji, mix")


def random_item_value(
    *,
    item_charset: str = DEFAULT_ITEM_CHARSET,
    rng: random.Random | None = None,
) -> str:
    """Return a random item string containing 3 to 8 characters."""
    rng = rng or random
    characters = _characters_for_charset(item_charset)
    length = rng.randint(3, 8)
    return "".join(rng.choice(characters) for _ in range(length))


def sample_positive_gaussian_values(
    row_count: int,
    *,
    mean: float = MEAN,
    approx_upper_bound: float = UPPER_BOUND,
    rng: random.Random | None = None,
) -> list[float]:
    """Return positive sample values using a bounded Gaussian-like distribution."""
    if row_count < 0:
        raise ValueError("row_count must be non-negative")
    if mean <= 0:
        raise ValueError("mean must be positive")
    if approx_upper_bound <= mean:
        raise ValueError("approx_upper_bound must be greater than mean")

    rng = rng or random
    standard_deviation = (approx_upper_bound - mean) / 3
    values: list[float] = []
    while len(values) < row_count:
        value = rng.gauss(mean, standard_deviation)
        if value > 0:
            values.append(round(value, 3))
    return values


def build_rows(
    row_count: int = DEFAULT_ROW_COUNT,
    start: str | None = None,
    item_charset: str = DEFAULT_ITEM_CHARSET,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    """Build sample CSV rows containing dates, categories, strings, and amounts."""
    if row_count < 0:
        raise ValueError("row_count must be non-negative")

    rng = random.Random(seed) if seed is not None else random
    dates = create_date_series(row_count=row_count, start=start)
    values = sample_positive_gaussian_values(row_count, rng=rng)

    rows = []
    for index, row_date in enumerate(dates):
        item_1 = random_item_value(item_charset=item_charset, rng=rng)
        item_2 = random_item_value(item_charset=item_charset, rng=rng)
        value = values[index]

        rows.append(
            {
                "id": str(index + 1),
                "date": row_date.strftime("%Y-%m-%d"),
                "category": rng.choice(CATEGORIES),
                "item_1": item_1,
                "item_2": item_2,
                "value": value,
                "amount": f"$ {value:,.2f}",
            }
        )

    return rows


def write_csv(
    rows: list[dict[str, Any]],
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """Write sample rows to a CSV file and return the output path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def create_sample_csv(
    row_count: int = DEFAULT_ROW_COUNT,
    start: str | None = None,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    item_charset: str = DEFAULT_ITEM_CHARSET,
    seed: int | None = None,
) -> SampleCSVResult:
    """Create a sample CSV file and return generation metadata."""
    rows = build_rows(
        row_count=row_count,
        start=start,
        item_charset=item_charset,
        seed=seed,
    )
    written_path = write_csv(rows=rows, output_path=output_path)
    return SampleCSVResult(row_count=len(rows), output_path=written_path)
