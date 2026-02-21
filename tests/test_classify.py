import pytest
from csvsmith.classify import CSVClassifier


@pytest.fixture
def test_data(tmp_path):
    """Sets up a temporary directory with CSV files and a config."""
    raw_dir = tmp_path / "raw"
    dest_dir = tmp_path / "output"
    raw_dir.mkdir()
    dest_dir.mkdir()

    # Create dummy CSVs
    (raw_dir / "sales_01.csv").write_text("date,item,price\n2023-01-01,hammer,15.00", encoding="utf-8")
    (raw_dir / "users_01.csv").write_text(
        "user_id,email,signup_date\n1,test@example.com,2023-01-01",
        encoding="utf-8",
    )
    (raw_dir / "weather.csv").write_text("temp,humidity\n22.5,45", encoding="utf-8")

    # Note:
    # - Sales signature is exact match for sales_01.csv
    # - Users signature is a *subset* match for users_01.csv (extra signup_date column)
    sigs = {"Sales": ["date", "item", "price"], "Users": ["user_id", "email"]}

    return {"raw": raw_dir, "dest": dest_dir, "sigs": sigs}


def test_classifier_run_contains_with_auto(test_data):
    # Use contains so "Users" matches even with extra columns.
    classifier = CSVClassifier(
        test_data["raw"],
        test_data["dest"],
        test_data["sigs"],
        auto=True,
        match="contains",
        mode="strict",
    )
    classifier.run()

    # Check if files moved to correct folders
    assert (test_data["dest"] / "Sales" / "sales_01.csv").exists()
    assert (test_data["dest"] / "Users" / "users_01.csv").exists()

    # Auto-cluster should create a cluster_* folder (hash suffix makes it unique).
    cluster_dirs = list(test_data["dest"].glob("cluster_*"))
    assert cluster_dirs, "Expected at least one cluster_* directory"
    assert any((d / "weather.csv").exists() for d in cluster_dirs)


def test_classifier_exact_relaxed_users_goes_to_unclassified(test_data):
    # Default is match="exact" -> users_01.csv does NOT match Users signature (extra column).
    # With auto=False it should go to unclassified.
    classifier = CSVClassifier(
        test_data["raw"],
        test_data["dest"],
        test_data["sigs"],
        auto=False,
        match="exact",
        mode="relaxed",
    )
    classifier.run()

    assert (test_data["dest"] / "Sales" / "sales_01.csv").exists()
    assert (test_data["dest"] / "unclassified" / "users_01.csv").exists()


def test_classifier_rollback(test_data):
    classifier = CSVClassifier(
        test_data["raw"],
        test_data["dest"],
        test_data["sigs"],
        auto=True,
        match="contains",
    )
    classifier.run()

    # Find the manifest
    manifest_path = next(test_data["dest"].glob("manifest_*.json"))

    # Run rollback
    classifier.rollback(manifest_path)

    # Files should be back in raw
    assert (test_data["raw"] / "sales_01.csv").exists()
    assert (test_data["raw"] / "users_01.csv").exists()
    assert (test_data["raw"] / "weather.csv").exists()

    # Moved files should no longer be in destination
    assert not (test_data["dest"] / "Sales" / "sales_01.csv").exists()
    assert not (test_data["dest"] / "Users" / "users_01.csv").exists()

    # The auto cluster folder should no longer contain the file
    cluster_dirs = list(test_data["dest"].glob("cluster_*"))
    for d in cluster_dirs:
        assert not (d / "weather.csv").exists()


def test_classifier_dry_run(test_data):
    classifier = CSVClassifier(
        test_data["raw"],
        test_data["dest"],
        test_data["sigs"],
        dry_run=True,
        auto=True,
        match="contains",
    )
    classifier.run()

    # Nothing should have moved
    assert (test_data["raw"] / "sales_01.csv").exists()
    assert (test_data["raw"] / "users_01.csv").exists()
    assert (test_data["raw"] / "weather.csv").exists()

    # No destination folders should be created in dry-run mode
    assert not (test_data["dest"] / "Sales").exists()
    assert not (test_data["dest"] / "Users").exists()
    assert not list(test_data["dest"].glob("cluster_*"))

    # And no manifest should be written (per current _save_manifest behavior)
    assert not list(test_data["dest"].glob("manifest_*.json"))


def test_classifier_report_only_writes_manifest_and_moves_nothing(test_data):
    classifier = CSVClassifier(
        test_data["raw"],
        test_data["dest"],
        test_data["sigs"],
        report_only=True,
        auto=True,
        match="contains",
    )
    classifier.run()

    # Files should still be in raw
    assert (test_data["raw"] / "sales_01.csv").exists()
    assert (test_data["raw"] / "users_01.csv").exists()
    assert (test_data["raw"] / "weather.csv").exists()

    # No destination folders created in report-only (no filesystem touch)
    assert not (test_data["dest"] / "Sales").exists()
    assert not (test_data["dest"] / "Users").exists()
    assert not list(test_data["dest"].glob("cluster_*"))

    # Manifest SHOULD be written (report-only is not dry-run)
    manifests = list(test_data["dest"].glob("manifest_*.json"))
    assert manifests, "Expected a manifest_*.json to be written in report-only mode"

    # Basic sanity on manifest content
    manifest_path = manifests[0]
    data = manifest_path.read_text(encoding="utf-8")
    assert '"report_only": true' in data.lower()