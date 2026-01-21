# csvsmith

[![PyPI version](https://img.shields.io/pypi/v/csvsmith.svg)](https://pypi.org/project/csvsmith/)
![Python versions](https://img.shields.io/pypi/pyversions/csvsmith.svg)
[![License](https://img.shields.io/pypi/l/csvsmith.svg)](https://pypi.org/project/csvsmith/)

`csvsmith` is a small collection of CSV utilities.

---

Current focus:

- Duplicate value counting (`count_duplicates_sorted`)
- Row-level digest creation (`add_row_digest`)
- Duplicate-row detection (`find_duplicate_rows`)
- Deduplication with full duplicate report (`dedupe_with_report`)
- Command-line interface (CLI) for quick operations

---

## Installation

From PyPI (future):

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

---

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
print(dup_rows)
```

### Deduplicate with report

```python
import pandas as pd
from csvsmith import dedupe_with_report

df = pd.read_csv("input.csv")

# Use all columns
deduped, report = dedupe_with_report(df)
deduped.to_csv("deduped.csv", index=False)
report.to_csv("duplicate_report.csv", index=False)

# Use all columns except an ID column
deduped_no_id, report_no_id = dedupe_with_report(df, exclude=["id"])
```

---

## CLI Usage

`csvsmith` includes a small command-line interface for duplicate detection
and CSV deduplication.

### Show duplicate rows

```bash
csvsmith row-duplicates input.csv
```

Save only duplicate rows to a file:

```bash
csvsmith row-duplicates input.csv -o duplicates_only.csv
```

Use only a subset of columns to determine duplicates:

```bash
csvsmith row-duplicates input.csv --subset col1 col2 -o dup_rows_subset.csv
```

Exclude ID column(s) when looking for duplicates:

```bash
csvsmith row-duplicates input.csv --exclude id -o dup_rows_no_id.csv
```

### Deduplicate and generate a duplicate report

```bash
csvsmith dedupe input.csv   --deduped deduped.csv   --report duplicate_report.csv
```

### Deduplicate using selected columns

```bash
csvsmith dedupe input.csv   --subset col1 col2   --deduped deduped_subset.csv   --report duplicate_report_subset.csv
```

### Remove *all* occurrences of duplicated rows

```bash
csvsmith dedupe input.csv   --subset col1   --keep False   --deduped deduped_no_dups.csv   --report duplicate_report_col1.csv
```

Exclude “id” from duplicate logic:

```bash
csvsmith dedupe input.csv   --exclude id   --deduped deduped_no_id.csv   --report duplicate_report_no_id.csv
```

---

## Philosophy (“csvsmith Manifesto”)

1. CSVs deserve tools that are simple, predictable, and transparent.
2. A row has meaning only when its identity is stable and hashable.
3. Collisions are sin; determinism is virtue.
4. Let no delimiter sow ambiguity among fields.
5. **Love thy `\x1f`.**  
   The unseen separator, the quiet guardian of clean hashes.  
   Chosen not for aesthetics, but for truth.
6. The pipeline should be silent unless something is wrong.
7. Your data deserves respect — and your tools should help you give it.

For more, see `MANIFESTO.md`.

---

## Usage

### Classify CSVs
Organize a mess of CSV files into structured folders based on their column headers.

```bash
# Preview what would happen (Dry Run)
csvsmith classify --src ./raw_data --dest ./organized --auto --dry-run

# Run classification with a signature config
csvsmith classify --src ./raw_data --dest ./organized --config signatures.json

# Undo a classification run
csvsmith classify --rollback ./organized/manifest_20260121_120000.json
```

## License

MIT License.
