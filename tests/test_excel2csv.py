from pathlib import Path

from openpyxl import Workbook

from csvsmith.excel2csv import excel_to_csv


def _create_workbook(path: Path) -> None:
    workbook = Workbook()

    summary = workbook.active
    summary.title = "Summary"
    summary.append(["name", "count", "note"])
    summary.append(["alpha", 1, None])
    summary.append([None, 2, "done"])

    details = workbook.create_sheet("Details")
    details.append(["id", "value"])
    details.append([10, "x"])

    workbook.save(path)
    workbook.close()


def test_excel_to_csv_uses_default_output_path(tmp_path: Path) -> None:
    excel_path = tmp_path / "input.xlsx"
    _create_workbook(excel_path)

    result = excel_to_csv(excel_path)

    assert result == tmp_path / "input.csv"
    assert result.read_text(encoding="utf-8") == (
        "name,count,note\n"
        "alpha,1,\n"
        ",2,done\n"
    )


def test_excel_to_csv_writes_to_custom_path(tmp_path: Path) -> None:
    excel_path = tmp_path / "input.xlsx"
    csv_path = tmp_path / "output" / "result.csv"
    _create_workbook(excel_path)

    result = excel_to_csv(excel_path, csv_path)

    assert result == csv_path
    assert csv_path.read_text(encoding="utf-8") == (
        "name,count,note\n"
        "alpha,1,\n"
        ",2,done\n"
    )


def test_excel_to_csv_creates_parent_directories_for_custom_path(tmp_path: Path) -> None:
    excel_path = tmp_path / "input.xlsx"
    csv_path = tmp_path / "nested" / "deeper" / "result.csv"
    _create_workbook(excel_path)

    result = excel_to_csv(excel_path, csv_path)

    assert result == csv_path
    assert csv_path.exists()
    assert csv_path.parent.exists()
    assert csv_path.read_text(encoding="utf-8") == (
        "name,count,note\n"
        "alpha,1,\n"
        ",2,done\n"
    )


def test_excel_to_csv_can_select_a_named_sheet(tmp_path: Path) -> None:
    excel_path = tmp_path / "input.xlsx"
    _create_workbook(excel_path)

    result = excel_to_csv(excel_path, sheet_name="Details")

    assert result == tmp_path / "input.csv"
    assert result.read_text(encoding="utf-8") == (
        "id,value\n"
        "10,x\n"
    )
