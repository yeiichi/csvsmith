# csvsmith

[![PyPI version](https://img.shields.io/pypi/v/csvsmith.svg)](https://pypi.org/project/csvsmith/)
![Python versions](https://img.shields.io/pypi/pyversions/csvsmith.svg)
[![License](https://img.shields.io/pypi/l/csvsmith.svg)](https://pypi.org/project/csvsmith/)

## Introduction

`csvsmith` is a lightweight collection of CSV utilities designed for
data integrity, deduplication, and organization. It provides a robust
Python API for programmatic data cleaning and a convenient CLI for quick
operations.

Whether you need to organize thousands of files based on their structural
signatures or pinpoint duplicate rows in a complex dataset, `csvsmith`
ensures the process is predictable, transparent, and reversible.

As of recent versions, CSV classification supports:

- strict vs relaxed header matching
- exact vs subset (“contains”) matching
- auto clustering with collision‑resistant hashes
- dry‑run preview
- report‑only planning mode (scan without moving)
- full rollback via manifest


## Installation

From PyPI:

```bash
pip install csvsmith
```

For local development:

```bash
git clone https://github.com/yeiichi/csvsmith.git
cd csvsmith
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```


## Python API Usage

### Count duplicate values

```python
from csvsmith import count_duplicates_sorted

items = ["a", "b", "a", "c", "a", "b"]
print(count_duplicates_sorted(items))
# [('a', 3), ('b', 2)]
```


### Find duplicate rows in a DataFrame

```python
import pandas as pd
from csvsmith import find_duplicate_rows

df = pd.read_csv("input.csv")
dup_rows = find_duplicate_rows(df)
```


### Deduplicate with report

```python
import pandas as pd
from csvsmith import dedupe_with_report

df = pd.read_csv("input.csv")

deduped, report = dedupe_with_report(df)
deduped.to_csv("deduped.csv", index=False)
report.to_csv("duplicate_report.csv", index=False)

# Exclude columns (e.g. IDs or timestamps)
deduped2, report2 = dedupe_with_report(df, exclude=["id"])
```


### CSV File Classification (Python)

```python
from csvsmith.classify import CSVClassifier

classifier = CSVClassifier(
    source_dir="./raw_data",
    dest_dir="./organized",
    auto=True,
    mode="relaxed",        # or "strict"
    match="exact",        # or "contains"
)

classifier.run()

# Roll back using the generated manifest
classifier.rollback("./organized/manifest_YYYYMMDD_HHMMSS.json")
```


## CLI Usage

csvsmith provides a CLI for duplicate detection and CSV organization.


### Show duplicate rows

```bash
csvsmith row-duplicates input.csv
```

Save duplicate rows only:

```bash
csvsmith row-duplicates input.csv -o duplicates_only.csv
```


### Deduplicate and generate a report

```bash
csvsmith dedupe input.csv --deduped deduped.csv --report duplicate_report.csv
```


### Classify CSVs

```bash
# Dry-run (preview only)
csvsmith classify --src ./raw --dest ./out --auto --dry-run

# Exact matching (default)
csvsmith classify --src ./raw --dest ./out --config signatures.json

# Relaxed matching (ignore column order)
csvsmith classify --src ./raw --dest ./out --config signatures.json --mode relaxed

# Subset matching (signature columns must be present)
csvsmith classify --src ./raw --dest ./out --config signatures.json --match contains

# Report-only (plan without moving files)
csvsmith classify --src ./raw --dest ./out --auto --report-only

# Roll back using manifest
csvsmith classify --rollback ./out/manifest_YYYYMMDD_HHMMSS.json
```


### Report-only mode

`--report-only` scans all CSVs and writes a manifest describing what *would*
happen, without touching the filesystem. This enables downstream pipelines
to consume the classification plan for custom processing.


## Philosophy

1. CSVs deserve tools that are simple, predictable, and transparent.
2. A row has meaning only when its identity is stable and hashable.
3. Collisions are sin; determinism is virtue.
4. Let no delimiter sow ambiguity among fields.
5. Love thy \x1f — the unseen separator, guardian of clean hashes.
6. The pipeline should be silent unless something is wrong.
7. Your data deserves respect — and your tools should help you give it.


## License

MIT License.
