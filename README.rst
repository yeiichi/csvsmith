csvsmith
========

.. image:: https://img.shields.io/pypi/v/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/

.. image:: https://img.shields.io/pypi/pyversions/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/

.. image:: https://img.shields.io/pypi/l/csvsmith.svg
   :target: https://pypi.org/project/ccsvsmith/

Introduction
------------

csvsmith is a lightweight collection of CSV utilities designed for data
integrity, deduplication, organization, Excel-to-CSV conversion, and
string-similarity analysis.

It provides a small Python API for programmatic data filtering and a single
CLI entrypoint for quick operations.

Whether you need to organize CSV files by header signatures, find duplicate
rows in a dataset, convert an Excel worksheet into CSV, drop rows by a
substring rule, or compare two strings for similarity, csvsmith aims to keep
the process predictable and reversible.

Features
--------

- row duplicate counting and reporting
- CSV deduplication with reports
- CSV classification by header signature
- dry-run and report-only classification modes
- rollback support via manifest
- row filtering by substring
- Excel worksheet to CSV conversion
- numeric string cleaning and normalization
- file moving by suffix
- string distance and similarity analysis
- a single command-line entrypoint with subcommands

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

Find duplicate rows in a CSV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import find_duplicate_rows, read_csv_rows

   rows = read_csv_rows("input.csv")
   dup_rows = find_duplicate_rows(rows)

Deduplicate with report
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import dedupe_with_report, read_csv_rows, write_csv_rows

   rows = read_csv_rows("input.csv")

   deduped, report = dedupe_with_report(rows)
   write_csv_rows("deduped.csv", deduped, fieldnames=list(rows[0].keys()))

   # Exclude columns (e.g. IDs or timestamps)
   deduped2, report2 = dedupe_with_report(rows, exclude=["id"])

Analyze string distance
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import analyze_pair

   result = analyze_pair("kitten", "sitting")

   print(result.get_relation_string())
   print(result.damerau_levenshtein_distance)
   print(result.jaro_winkler_score)
   print(result.similarity_percentage)

Clean numeric values
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import clean_numeric

   # Handles separators and parentheses for negative numbers
   val1 = clean_numeric("1,234.56")
   val2 = clean_numeric("(100.00)")
   val3 = clean_numeric("1 234,56", sep=" ", decimal=",")

   print(val1)  # 1234.56
   print(val2)  # -100.0
   print(val3)  # 1234.56

CLI Usage
Drop rows in a CSV by column name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import DropRowsBySubstring

   cleaner = DropRowsBySubstring(
       "input.csv",
       column_name="notes",
       unwanted_text="spam",
       case_sensitive=False,
   )

   cleaner.write_filtered_rows()

If you are upgrading from an older version, CSVCleaner is still available as a
compatibility alias, but DropRowsBySubstring is the preferred name.

Convert Excel to CSV
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import excel_to_csv

   csv_path = excel_to_csv(
       "input.xlsx",
       sheet_name="Details",
   )

   print(csv_path)

Move files by suffix
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csvsmith import move_by_suffix

   moved_count = move_by_suffix(
       src_dir="./raw",
       dst_dir="./processed",
       suffixes=[".csv", ".pdf"],
   )

   print(f"Moved {moved_count} files.")

CSV File Classification (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

csvsmith provides a single CLI entrypoint with subcommands for duplicate
detection, CSV organization, Excel conversion, file moving, row filtering,
and string comparison.

Show duplicate rows
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith row-duplicates input.csv

Save duplicate rows only:

.. code-block:: bash

   csvsmith row-duplicates input.csv -o duplicates_only.csv

Analyze string distance
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith string-distance "kitten" "sitting"

Ignore case:

.. code-block:: bash

   csvsmith string-distance "Hello" "hello" --ignore-case

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
   csvsmith classify ./raw ./out --match contains

   # Report-only (plan without moving files)
   csvsmith classify ./raw ./out --auto --report-only

   # Roll back using manifest
   # Use the Python API for rollback:
   # classifier.rollback("./out/manifest_YYYYMMDD_HHMMSS.json")

Move files by suffix
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith move-files src_dir dst_dir --suffixes csv,pdf

This moves files whose suffix matches one of the given values. The suffixes can
be written with or without a leading dot, and matching is case-insensitive.

Clean numeric values
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   csvsmith clean-numeric "1,234.56"

Using custom separators:

.. code-block:: bash

   csvsmith clean-numeric "1 234,56" --sep " " --decimal ","

Drop CSV rows
~~~~~~~~~~~~~

Use the ``drop-rows`` subcommand to remove rows from a CSV file when a chosen
column contains an unwanted substring.

The command expects three positional arguments:

- input: path to the source CSV file
- column_name: the header name of the column to inspect
- unwanted_text: the text that, if found in the chosen column, causes a row to be removed

It also supports two optional flags:

- --case-insensitive: match unwanted_text without regard to letter case
- --drop-header: do not copy the first row to the output file

The output is written next to the input file using the same name with
``.filtered.csv`` appended. For example:

- orders.csv -> orders.filtered.csv

Basic usage
^^^^^^^^^^^

.. code-block:: bash

   csvsmith drop-rows input.csv notes spam

This removes every row where the notes column contains spam. The header row is
preserved by default.

Case-insensitive matching
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   csvsmith drop-rows input.csv notes spam --case-insensitive

This is useful when the data may contain values such as Spam, SPAM, or sPaM.

Skip the header row
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   csvsmith drop-rows input.csv notes spam --drop-header

Use this only if you explicitly want the output file to contain data rows only.

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

   csvsmith drop-rows input.csv notes spam

produces a filtered file containing:

.. code-block:: csv

   id,name,notes
   1,Alice,ok
   3,Carol,ok

Report-only mode
~~~~~~~~~~~~~~~~

``--report-only`` scans matching CSVs and writes a manifest describing what
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