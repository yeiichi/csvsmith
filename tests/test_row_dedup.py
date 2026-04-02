from csvsmith.tools.row_dedup import (
    add_row_digest,
    find_duplicate_rows,
    dedupe_with_report,
)
from csvsmith.utils.io import (
    count_duplicates_sorted,
    read_csv_rows,
    write_csv_rows,
)


# -------------------------------------------------------------------
# count_duplicates_sorted
# -------------------------------------------------------------------


def test_count_duplicates_sorted_basic():
    items = ["a", "b", "a", "c", "a", "b"]
    result = count_duplicates_sorted(items)
    assert result == [("a", 3), ("b", 2)]


def test_count_duplicates_sorted_threshold():
    items = ["x", "x", "y", "y", "y"]
    result = count_duplicates_sorted(items, threshold=3)
    assert result == [("y", 3)]


def test_count_duplicates_sorted_reverse_false():
    items = ["a", "b", "a", "b", "b"]
    result = count_duplicates_sorted(items, reverse=False)
    assert result == [("a", 2), ("b", 3)]


def test_count_duplicates_sorted_empty_input():
    items: list[str] = []
    result = count_duplicates_sorted(items)
    assert result == []


def test_count_duplicates_sorted_numeric_items():
    items = [1, 2, 2, 3, 3, 3]
    result = count_duplicates_sorted(items)
    assert result == [(3, 3), (2, 2)]


def test_count_duplicates_sorted_threshold_above_all():
    items = ["a", "a", "b"]
    result = count_duplicates_sorted(items, threshold=5)
    assert result == []


# -------------------------------------------------------------------
# add_row_digest
# -------------------------------------------------------------------


def test_add_row_digest_basic():
    rows = [{"A": 1, "B": "x"}, {"A": 1, "B": "x"}, {"A": 2, "B": "y"}]
    out = add_row_digest(rows)
    assert "row_digest" in out[0]
    assert out[0]["row_digest"] == out[1]["row_digest"]
    assert out[2]["row_digest"] != out[0]["row_digest"]


def test_add_row_digest_subset_columns():
    rows = [{"A": 1, "B": "x"}, {"A": 1, "B": "y"}, {"A": 1, "B": "z"}]
    out = add_row_digest(rows, subset=["A"], colname="digest_a")
    assert "digest_a" in out[0]
    digests = {row["digest_a"] for row in out}
    assert len(digests) == 1


def test_add_row_digest_inplace_true_modifies_original():
    rows = [{"A": 1, "B": "x"}, {"A": 2, "B": "y"}]
    add_row_digest(rows, inplace=True)
    assert "row_digest" in rows[0]


def test_add_row_digest_handles_nans():
    rows = [{"A": 1, "B": "x"}, {"A": None, "B": "x"}, {"A": 1, "B": None}]
    out = add_row_digest(rows)
    for row in out:
        assert "row_digest" in row
        assert len(row["row_digest"]) == 64


def test_add_row_digest_exclude_id_column():
    rows = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 10},
        {"id": 3, "value": 20},
    ]
    out_all = add_row_digest(rows)
    digests_all = {row["row_digest"] for row in out_all}
    assert len(digests_all) == 3

    out_no_id = add_row_digest(rows, exclude=["id"])
    assert out_no_id[0]["row_digest"] == out_no_id[1]["row_digest"]
    assert out_no_id[2]["row_digest"] != out_no_id[0]["row_digest"]


# -------------------------------------------------------------------
# find_duplicate_rows
# -------------------------------------------------------------------


def test_find_duplicate_rows_all_columns():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 1, "B": "x"},
        {"A": 2, "B": "y"},
        {"A": 2, "B": "y"},
        {"A": 2, "B": "z"},
        {"A": 3, "B": "z"},
    ]
    dup_rows = find_duplicate_rows(rows)
    # Rows 0, 1 (1, x) and 2, 3 (2, y) are duplicates
    assert len(dup_rows) == 4
    assert dup_rows[0] == {"A": 1, "B": "x"}
    assert dup_rows[1] == {"A": 1, "B": "x"}
    assert dup_rows[2] == {"A": 2, "B": "y"}
    assert dup_rows[3] == {"A": 2, "B": "y"}


def test_find_duplicate_rows_subset():
    rows = [
        {"A": 1, "B": 10},
        {"A": 1, "B": 11},
        {"A": 2, "B": 20},
        {"A": 2, "B": 21},
        {"A": 2, "B": 22},
        {"A": 3, "B": 30},
    ]
    dup_rows = find_duplicate_rows(rows, subset=["A"])
    # Rows with A=1 (indices 0, 1) and A=2 (indices 2, 3, 4) are duplicates
    assert len(dup_rows) == 5


def test_find_duplicate_rows_no_duplicates():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 2, "B": "y"},
        {"A": 3, "B": "z"},
    ]
    dup_rows = find_duplicate_rows(rows)
    assert dup_rows == []


def test_find_duplicate_rows_empty_input():
    rows = []
    dup_rows = find_duplicate_rows(rows)
    assert dup_rows == []


# -------------------------------------------------------------------
# dedupe_with_report
# -------------------------------------------------------------------


def test_dedupe_with_report_all_columns():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 1, "B": "x"},
        {"A": 2, "B": "y"},
        {"A": 2, "B": "y"},
        {"A": 2, "B": "z"},
        {"A": 3, "B": "z"},
    ]

    deduped, report = dedupe_with_report(rows)
    # Expected unique: (1, x), (2, y), (2, z), (3, z)
    assert len(deduped) == 4
    assert len(report) == 2  # (1, x) and (2, y) had duplicates
    assert {r["count"] for r in report} == {2}


def test_dedupe_with_report_subset_column():
    rows = [
        {"A": 1, "B": 10},
        {"A": 1, "B": 11},
        {"A": 2, "B": 20},
        {"A": 2, "B": 21},
        {"A": 2, "B": 22},
        {"A": 3, "B": 30},
    ]

    deduped, report = dedupe_with_report(rows, subset=["A"])
    # Expected unique A values: 1, 2, 3
    assert len(deduped) == 3
    assert len(report) == 2
    counts = sorted([r["count"] for r in report], reverse=True)
    assert counts == [3, 2]


def test_dedupe_with_report_no_duplicates_gives_empty_report():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 2, "B": "y"},
        {"A": 3, "B": "z"},
    ]
    deduped, report = dedupe_with_report(rows)
    assert len(deduped) == 3
    assert report == []


def test_dedupe_with_report_keep_last():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 1, "B": "y"},
        {"A": 1, "B": "z"},
    ]

    deduped_first, _ = dedupe_with_report(rows, subset=["A"], keep="first")
    deduped_last, _ = dedupe_with_report(rows, subset=["A"], keep="last")

    assert deduped_first[0]["B"] == "x"
    assert deduped_last[0]["B"] == "z"


def test_dedupe_with_report_custom_digest_col_name():
    rows = [
        {"A": 1, "B": "x"},
        {"A": 1, "B": "x"},
        {"A": 2, "B": "y"},
        {"A": 2, "B": "y"},
    ]

    deduped, report = dedupe_with_report(rows, digest_col="my_digest")
    assert len(deduped) == 2
    assert "my_digest" in report[0]