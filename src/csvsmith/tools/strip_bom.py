from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


UTF8_BOM = b"\xef\xbb\xbf"


@dataclass(frozen=True)
class StripBomResult:
    input_path: Path
    output_path: Path
    removed: bool


def default_output_path(csv_path: str | Path) -> Path:
    """Return the default output path for a BOM-stripped CSV."""
    path = Path(csv_path)
    return path.with_name(f"{path.stem}.no-bom{path.suffix}")


def strip_utf8_bom(
    csv_path: str | Path,
    output_path: str | Path | None = None,
    *,
    in_place: bool = False,
) -> StripBomResult:
    """Remove a leading UTF-8 BOM from a CSV file while preserving all other bytes."""
    input_path = Path(csv_path)
    if in_place and output_path is not None:
        raise ValueError("--in-place cannot be used with --output")

    if in_place:
        resolved_output_path = input_path
    elif output_path:
        resolved_output_path = Path(output_path)
    else:
        resolved_output_path = default_output_path(input_path)

    data = input_path.read_bytes()
    removed = data.startswith(UTF8_BOM)
    output_data = data[len(UTF8_BOM) :] if removed else data

    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_output_path.write_bytes(output_data)

    return StripBomResult(
        input_path=input_path,
        output_path=resolved_output_path,
        removed=removed,
    )
