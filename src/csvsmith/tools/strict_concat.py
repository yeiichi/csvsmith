import csv
from collections.abc import Iterable
from pathlib import Path


def find_csvs(csv_dir: Path | str) -> list[Path]:
    """
    Find all CSV files in the specified directory.

    This function searches for all files with a ``.csv`` extension in the given
    directory and returns a sorted list of their paths.

    :param csv_dir: The directory to search for CSV files. This can be provided
        as either a ``Path`` object or a string representing the path to the
        directory.
    :type csv_dir: Path | str
    :return: Sorted list of paths to all ``.csv`` files found in the specified
        directory.
    :rtype: list[Path]
    """
    return sorted(Path(csv_dir).glob("*.csv"))


def read_header(csv_path: Path) -> list[str]:
    """
    Reads the header row of a given CSV file.

    This function opens a CSV file located at the specified path, reads its first
    row, and returns it as a list of strings. The file is assumed to be encoded
    in UTF-8 with optional BOM (Byte Order Mark). If the CSV file is empty, a
    ValueError is raised indicating the problem. The CSV file is expected to be
    opened in read mode with no newline translation.

    :param csv_path: The path to the CSV file to read the header from.
    :type csv_path: Path
    :return: A list of strings representing the header row of the CSV file.
    :rtype: list[str]
    :raises ValueError: If the CSV file is empty and no header can be retrieved.
    """
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration as e:
            raise ValueError(f"Empty CSV: {csv_path}") from e


def _validate_headers_match(csv_paths: list[Path]) -> list[str]:
    """
    Validates that the headers of all provided CSV files match each other. The function compares the
    header of each CSV file in the input list against the header of the first file. If a mismatch
    is encountered, a ValueError is raised indicating the problematic file. The function returns
    the header of the first file if all headers are consistent.

    :param csv_paths: A list of Path objects representing the file paths to the CSV files to validate.
    :type csv_paths: list[Path]
    :return: A list of strings representing the matched header of the first CSV file.
    :rtype: list[str]
    """
    expected_header = read_header(csv_paths[0])
    for csv_path in csv_paths[1:]:
        if read_header(csv_path) != expected_header:
            raise ValueError(f"Header mismatch: {csv_path}")
    return expected_header


def strict_concat_rows(csv_dir: Path | str) -> list[list[str]]:
    """
    Concatenates rows from multiple CSV files into a list of lists of strings, ensuring
    the headers across all CSV files match. The output includes a new column indicating
    the file stem.

    :param csv_dir: Directory containing the CSV files or a specific path to a CSV file.
    :type csv_dir: Path | str
    :return: A list of lists, where each inner list represents a row from the concatenated
        CSV files. The first row contains the headers, including a "file_stem" column.
    :rtype: list[list[str]]
    :raises FileNotFoundError: If no CSV files are found in the provided directory.
    """
    csv_paths = find_csvs(csv_dir)
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {csv_dir}")
    
    expected_header = _validate_headers_match(csv_paths)
    out_rows: list[list[str]] = [["file_stem", *expected_header]]
    
    for csv_path in csv_paths:
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                out_rows.append([csv_path.stem, *row])
    return out_rows


def save_csv(rows: Iterable[list[str]], out_path: Path | str) -> None:
    """Write rows to out_path."""
    out_path = Path(out_path)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)