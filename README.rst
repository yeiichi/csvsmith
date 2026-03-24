csvsmith
========

.. image:: https://img.shields.io/pypi/v/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/

.. image:: https://img.shields.io/pypi/pyversions/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/

.. image:: https://img.shields.io/pypi/l/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/

Introduction
------------

csvsmith is a lightweight collection of CSV utilities designed for
data integrity, deduplication, organization, and Excel-to-CSV conversion.
It provides a robust Python API for programmatic data cleaning and a
convenient CLI for quick operations.

Whether you need to organize thousands of files based on their structural
signatures, pinpoint duplicate rows in a complex dataset, or convert an
Excel worksheet into CSV, csvsmith ensures the process is predictable,
transparent, and reversible.

As of recent versions, CSV classification supports:

- strict vs relaxed header matching
- exact vs subset ("contains") matching
- auto clustering with collision-resistant hashes
- dry-run preview
- report-only planning mode (scan without moving)
- full rollback via manifest

Installation
------------

From PyPI:

.. code-block:: bash

   pip install csvsmith

For local development:

.. code-block:: bash

   git clone https://github.com/yeiichi/csvsmith.git
   cd csvsmith
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]

Python API Usage
----------------

Count duplicate values
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import count_duplicates_sorted

   items = ["a", "b", "a", "c", "a", "b"]
   print(count_duplicates_sorted(items))
   # [('a', 3), ('b', 2)]

Find duplicate rows in a DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from csvsmith import find_duplicate_rows

   df = pd.read_csv("input.csv")
   dup_rows = find_duplicate_rows(df)

Deduplicate with report
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from csvsmith import dedupe_with_report

   df = pd.read_csv("input.csv")

   deduped, report = dedupe_with_report(df)
   deduped.to_csv("deduped.csv", index=False)
   report.to_csv("duplicate_report.csv", index=False)

   # Exclude columns (e.g. IDs or timestamps)
   deduped2, report2 = dedupe_with_report(df, exclude=["id"])

Clean a CSV by column name
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import DropRowsBySubstring

   cleaner = DropRowsBySubstring(
       "input.csv",
       column_name="notes",
       unwanted_text="spam",
       case_sensitive=False,
   )

   cleaner.write_filtered_rows()

If you are upgrading from an older version, CSVCleaner is kept as a
compatibility alias.

Convert Excel to CSV
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import excel_to_csv

   csv_path = excel_to_csv(
       "input.xlsx",
       sheet_name="Details",
   )

   print(csv_path)

CSV File Classification (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith.classify import CSVClassifier

   classifier = CSVClassifier(
       source_dir="./raw_data",
       dest_dir="./organized",
       auto=True,
       mode="relaxed",        # or "strict"
       match="exact",         # or "contains"
   )

   classifier.run()

   # Roll back using the generated manifest
   classifier.rollback("./organized/manifest_YYYYMMDD_HHMMSS.json")

CLI Usage
---------

csvsmith provides a CLI for duplicate detection, CSV organization,
Excel conversion, and cleaning.

Show duplicate rows
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith row-duplicates input.csv

Save duplicate rows only:

.. code-block:: bash

   csvsmith row-duplicates input.csv -o duplicates_only.csv

Deduplicate and generate a report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith dedupe input.csv -o deduped.csv --report duplicate_report.json

Convert Excel to CSV
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx

Select a named worksheet:

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx --sheet-name Details

Write to a custom output path:

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx -o output/result.csv

Classify CSVs
~~~~~~~~~~~~~

.. code-block:: bash

   # Dry-run (preview only)
   csvsmith classify ./raw ./out --auto --dry-run

   # Exact matching (default)
   csvsmith classify ./raw ./out

   # Relaxed matching (ignore col order)
   csvsmith classify ./raw ./out --mode relaxed

   # Subset matching (signature columns must be present)
   csvsmith classify ./raw ./out --match subset

   # Report-only (plan without moving files)
   csvsmith classify ./raw ./out --auto --report-only

   # Roll back using manifest
   # Use the Python API for rollback:
   # classifier.rollback("./out/manifest_YYYYMMDD_HHMMSS.json")

Clean CSV rows
~~~~~~~~~~~~~~

Use clean to remove rows from a CSV file when a chosen column contains
an unwanted substring.

The command expects three positional arguments:

- input: path to the source CSV file
- column_name: the header name of the column to inspect
- unwanted_text: the text that, if found in the chosen column, causes a row to be removed

It also supports two optional flags:

- --case-insensitive: match unwanted_text without regard to letter case
- --drop-header: do not copy the first row to the output file

The output is written next to the input file using the same name with
.clean.csv appended. For example:

- orders.csv -> orders.clean.csv

Basic usage
^^^^^^^^^^^

.. code-block:: bash

   csvsmith clean input.csv notes spam

This removes every row where the notes column contains spam.
The header row is preserved by default.

Case-insensitive matching
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   csvsmith clean input.csv notes spam --case-insensitive

This is useful when the data may contain values such as Spam,
SPAM, or sPaM.

Skip the header row
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   csvsmith clean input.csv notes spam --drop-header

Use this only if you explicitly want the output file to contain data rows
only.

How to use it effectively
^^^^^^^^^^^^^^^^^^^^^^^^^

- Make sure column_name exactly matches a header value in the CSV.
- Choose a substring that is specific enough to avoid removing unrelated rows.
- Use --case-insensitive when the source data is inconsistent in capitalization.
- Keep the header unless you are intentionally producing a headerless file.
- If the column name is missing, the command will fail with a clear error.

Example
^^^^^^^

Suppose you have a CSV like this:

.. code-block:: csv

   id,name,notes
   1,Alice,ok
   2,Bob,contains spam here
   3,Carol,ok

Running:

.. code-block:: bash

   csvsmith clean input.csv notes spam

produces a cleaned file containing:

.. code-block:: csv

   id,name,notes
   1,Alice,ok
   3,Carol,ok

Report-only mode
~~~~~~~~~~~~~~~~

--report-only scans all CSVs and writes a manifest describing what
would happen, without touching the filesystem. This enables downstream
pipelines to consume the classification plan for custom processing.

Philosophy
----------

1. CSVs deserve tools that are simple, predictable, and transparent.
2. A row has meaning only when its identity is stable and hashable.
3. Collisions are sin; determinism is virtue.
4. Let no delimiter sow ambiguity among fields.
5. Love thy \x1f — the unseen separator, guardian of clean hashes.
6. The pipeline should be silent unless something is wrong.
7. Your data deserves respect — and your tools should help you give it.

License
-------

MIT License.