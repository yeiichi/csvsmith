Deduplication
=============

What it does
------------

Removes duplicate rows from a CSV file. You can specify a subset of columns to consider for identifying duplicates, or exclude specific columns.

Python usage
------------

.. code-block:: python

   from csvsmith.tools.row_dedup import dedupe_with_report

   rows = [
       {"id": "1", "name": "Alice"},
       {"id": "2", "name": "Bob"},
       {"id": "1", "name": "Alice"},
   ]

   # Remove duplicates by considering "id" and "name"
   deduped, report = dedupe_with_report(rows, subset=["id", "name"])

CLI usage
---------

.. code-block:: bash

   csvsmith dedupe input.csv -o output.csv --subset id,name --keep first --report report.json

Behavior notes
--------------

- **Subset**: Comma-separated list of columns to check for duplicates. If omitted, all columns are used.
- **Keep**: Which record to keep: ``first`` (default) or ``last``.
- **Report**: Path to a JSON file where a summary of duplicates found will be saved.
