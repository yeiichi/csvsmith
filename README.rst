csvsmith
========

.. image:: https://img.shields.io/pypi/v/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/csvsmith.svg
   :target: https://pypi.org/project/csvsmith/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/csvsmith.svg
   :target: https://opensource.org/licenses/
   :alt: License

.. image:: https://img.shields.io/badge/docs-Read%20the%20Docs-blue.svg
   :target: https://csvsmith.readthedocs.io/en/latest/
   :alt: Documentation

Small, focused CSV utilities for common data wrangling tasks.

``csvsmith`` provides a handful of practical tools for working with CSV
files, including cleaning numeric values, filtering rows, deduplicating
records, classifying files, converting Excel spreadsheets to CSV, moving
files by suffix, and finding matches inside CSV content.

Documentation
-------------

Read the full documentation at:

https://csvsmith.readthedocs.io/en/latest/

Features
--------

- Clean numeric strings into normalized values
- Filter CSV rows by substring matching
- Deduplicate row data and generate reports
- Classify CSV files into folders based on headers/signatures
- Convert Excel workbooks to CSV
- Move files by suffix
- Find matching values inside CSV files
- Concatenate CSV files with identical headers
- Use the tools either from Python or from the command line

Installation
------------

Install the package in your environment as usual for your project setup.

Example:

.. code-block:: console

   pip install csvsmith

If you are developing locally, install it in editable mode from the project
root:

.. code-block:: console

   pip install -e .

Quick start
-----------

You can use the library from Python:

.. code-block:: python

   from csvsmith.utils.clean_numeric import clean_currency_numeric

   print(clean_currency_numeric("$1,234.56"))

For command-line usage, use single quotes around values containing ``$``:

.. code-block:: console

   csvsmith --help

Command-line usage
------------------

The package provides a CLI with several subcommands.

Clean numeric values:

.. code-block:: console

   csvsmith clean-numeric "1,234.56" --sep "," --decimal "."

Clean currency-prefixed numeric values:

.. code-block:: console

   csvsmith clean-currency-numeric '$1,234.56' --sep "," --decimal "."

.. note::

   Use single quotes for values containing ``$``. Double quotes may trigger
   shell expansion and change the input unexpectedly.

Filter rows in a CSV:

.. code-block:: console

   csvsmith drop-rows input.csv notes spam --case-insensitive --drop-header

Deduplicate rows:

.. code-block:: console

   csvsmith dedupe input.csv -o out.csv --subset id --keep first

Classify CSV files:

.. code-block:: console

   csvsmith classify src_dir dst_dir --mode relaxed --match subset --auto --dry-run

Convert Excel to CSV:

.. code-block:: console

   csvsmith excel2csv input.xlsx

Move files by suffix:

.. code-block:: console

   csvsmith move-files src_dir dst_dir --suffixes .csv,.pdf

Find matches in a CSV:

.. code-block:: console

   csvsmith find-matches input.csv target --ignore-case --ignore-whitespace

Concatenate CSV files:

.. code-block:: console

   csvsmith strict-concat file1.csv file2.csv -o combined.csv

Find matches in a CSV
---------------------

``find_matches_in_csv`` searches a CSV file for a target value and returns
match records containing coordinates and row context information.

Python API:

.. code-block:: python

   from csvsmith import find_matches_in_csv

   results = find_matches_in_csv("input.csv", "target")

CLI:

.. code-block:: console

   csvsmith find-matches input.csv target

Options:

- ``--ignore-case``: ignore case while matching
- ``--ignore-whitespace``: ignore whitespace while matching
- ``--no-nfkc``: disable NFKC normalization

If matches are found, the CLI prints formatted JSON. If no matches are found,
it prints a simple message.

Other Python APIs
-----------------

The package also exposes a few other helper functions and classes from its
top-level API.

Numeric and row tools:

.. code-block:: python

   from csvsmith import (
       clean_numeric,
       count_duplicates_sorted,
       add_row_digest,
       find_duplicate_rows,
       dedupe_with_report,
       read_csv_rows,
       write_csv_rows,
   )

CSV classification and filtering:

.. code-block:: python

   from csvsmith import CSVClassifier, DropRowsBySubstring, CSVCleaner

File and conversion helpers:

.. code-block:: python

   from csvsmith import excel_to_csv, move_by_suffix, strict_concat_rows, save_csv

String comparison utilities:

.. code-block:: python

   from csvsmith import StringDistance, Relation, Result, analyze_pair

Project structure
-----------------

The code is organized into two main areas:

- ``csvsmith.tools`` for higher-level CSV workflows
- ``csvsmith.utils`` for reusable utility helpers

Testing
-------

Run the test suite with your preferred Python test runner.

Example:

.. code-block:: console

   pytest

License
-------

See the project license for details.