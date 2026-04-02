from pathlib import Path

from csvsmith.tools.move_files import move_by_suffix, normalize_suffixes


def test_normalize_suffixes_adds_leading_dot_and_lowercases() -> None:
    assert normalize_suffixes({"CSV", ".Pdf", "txt"}) == {".csv", ".pdf", ".txt"}


def test_move_by_suffix_moves_only_matching_files(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    (src_dir / "report.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (src_dir / "notes.pdf").write_text("pdf content", encoding="utf-8")
    (src_dir / "image.png").write_text("image content", encoding="utf-8")

    moved_count = move_by_suffix(src_dir, dst_dir)

    assert moved_count == 2
    assert not (src_dir / "report.csv").exists()
    assert not (src_dir / "notes.pdf").exists()
    assert (src_dir / "image.png").exists()
    assert (dst_dir / "report.csv").exists()
    assert (dst_dir / "notes.pdf").exists()
    assert not (dst_dir / "image.png").exists()


def test_move_by_suffix_is_case_insensitive(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    (src_dir / "DATA.CSV").write_text("a,b\n1,2\n", encoding="utf-8")
    (src_dir / "summary.PdF").write_text("pdf content", encoding="utf-8")

    moved_count = move_by_suffix(src_dir, dst_dir, suffixes={".csv", ".pdf"})

    assert moved_count == 2
    assert (dst_dir / "DATA.CSV").exists()
    assert (dst_dir / "summary.PdF").exists()


def test_move_by_suffix_accepts_suffixes_without_leading_dot(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    (src_dir / "sales.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (src_dir / "manual.pdf").write_text("pdf content", encoding="utf-8")

    moved_count = move_by_suffix(src_dir, dst_dir, suffixes={"csv", "pdf"})

    assert moved_count == 2
    assert (dst_dir / "sales.csv").exists()
    assert (dst_dir / "manual.pdf").exists()


def test_move_by_suffix_returns_zero_when_no_files_match(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()

    (src_dir / "image.png").write_text("image content", encoding="utf-8")
    (src_dir / "readme.txt").write_text("text content", encoding="utf-8")

    moved_count = move_by_suffix(src_dir, dst_dir)

    assert moved_count == 0
    assert (src_dir / "image.png").exists()
    assert (src_dir / "readme.txt").exists()
    assert not any(dst_dir.iterdir())
