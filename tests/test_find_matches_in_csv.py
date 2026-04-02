import pytest
from csvsmith.tools.find_matches_in_csv import find_matches_in_csv


@pytest.fixture
def sample_csv_file(tmp_path):
    file_content = """name,age,city
John,30,New York
Alice,25,Los Angeles
Bob,35,New York"""
    file_path = tmp_path / "sample.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    return file_path


def test_find_matches_in_csv_key_matches_in_file(sample_csv_file):
    result = find_matches_in_csv(sample_csv_file, "New York")
    assert len(result) == 2
    assert result[0]["match"] == "New York"
    assert result[0]["coords"] == (0, 2)
    assert result[1]["match"] == "New York"
    assert result[1]["coords"] == (2, 2)


def test_find_matches_in_csv_key_not_found(sample_csv_file):
    result = find_matches_in_csv(sample_csv_file, "Chicago")
    assert len(result) == 0


def test_find_matches_in_csv_with_ignore_case(sample_csv_file):
    result = find_matches_in_csv(sample_csv_file, "new york", ignore_case=True)
    assert len(result) == 2
    assert result[0]["match"] == "New York"
    assert result[1]["match"] == "New York"


def test_find_matches_in_csv_ignore_whitespace(tmp_path):
    file_content = """name,age,city
John,30,  New York
Alice,25,  Los Angeles
Bob,35,New  York"""
    file_path = tmp_path / "sample_with_whitespace.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    result = find_matches_in_csv(file_path, "New York", ignore_whitespace=True)
    assert len(result) == 2
    assert result[0]["coords"] == (0, 2)
    assert result[1]["coords"] == (2, 2)


def test_find_matches_in_csv_correct_neighbor_data(sample_csv_file):
    result = find_matches_in_csv(sample_csv_file, "Alice")
    assert len(result) == 1
    assert result[0]["coords"] == (1, 0)
    assert result[0]["data"] == {"col_1": "25", "col_2": "Los Angeles"}
