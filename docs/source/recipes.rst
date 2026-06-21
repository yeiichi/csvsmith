Recipes
=======

These examples combine a few csvsmith tools into practical workflows. For
individual command options, follow the linked tool pages.

Convert and deduplicate a worksheet
-----------------------------------

Convert one Excel worksheet, inspect duplicate groups, and then write a clean
CSV:

.. code-block:: console

   csvsmith excel-to-csv source.xlsx -o source.csv --sheet-name "Data"
   csvsmith row-duplicates source.csv --subset customer_id,date
   csvsmith dedupe source.csv -o clean.csv \
       --subset customer_id,date --report duplicates.json

See :doc:`tools/excel2csv` and :doc:`tools/dedupe`.

Clean a CSV column with the Python API
--------------------------------------

The numeric CLI commands process individual values. For a whole column, use
the Python API:

.. code-block:: python

   from csvsmith import read_csv_rows, write_csv_rows
   from csvsmith.utils.clean_numeric import clean_currency_numeric

   rows = read_csv_rows("source.csv")
   for row in rows:
       row["amount"] = clean_currency_numeric(row["amount"], relaxed=True)

   fieldnames = list(rows[0]) if rows else []
   write_csv_rows("clean.csv", rows, fieldnames=fieldnames)

``relaxed=True`` preserves values that cannot be parsed. See
:doc:`tools/clean-numeric` and :doc:`python-api`.

Combine matching exports
------------------------

When several exports have identical headers, concatenate them while retaining
their source filenames:

.. code-block:: console

   csvsmith strict-concat daily_exports/ -o combined.csv
   csvsmith dedupe combined.csv -o combined-clean.csv --exclude file_stem

See :doc:`tools/strict-concat` and :doc:`tools/dedupe`.

Preview before organizing files
-------------------------------

Inspect automatic classification before moving CSV files:

.. code-block:: console

   csvsmith classify incoming/ organized/ --auto --dry-run
   csvsmith classify incoming/ organized/ --auto

For simple suffix-based moves:

.. code-block:: console

   csvsmith move-files incoming/ processed/ --suffixes csv,pdf

The destination directories should already exist. See :doc:`tools/classify`
and :doc:`tools/move-files`.
