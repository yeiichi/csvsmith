from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

DEFAULT_SUFFIXES = {".csv", ".pdf"}


def normalize_suffixes(suffixes: Iterable[str]) -> set[str]:
    return {
        s.lower() if s.startswith(".") else f".{s.lower()}"
        for s in suffixes
    }


def move_by_suffix(
        src_dir: Path | str,
        dst_dir: Path | str,
        suffixes: Iterable[str] = DEFAULT_SUFFIXES,
) -> int:
    """
    Move files from ``src_dir`` to ``dst_dir`` when their suffix matches.

    Suffix matching is case-insensitive and accepts values with or without a
    leading dot (for example, ``"csv"`` and ``".csv"`` are treated the same).

    Args:
        src_dir: Source directory to scan for files.
        dst_dir: Destination directory where matching files are moved.
        suffixes: File suffixes to match against.

    Returns:
        The number of files moved.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    allowed_suffixes = normalize_suffixes(suffixes)

    moved_files_count = 0

    for source_file in src_dir.iterdir():
        if not source_file.is_file():
            continue

        source_suffix = source_file.suffix.lower()
        if source_suffix not in allowed_suffixes:
            continue

        destination_file = dst_dir / source_file.name
        shutil.move(source_file, destination_file)
        moved_files_count += 1

    return moved_files_count
