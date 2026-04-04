Drop Rows
=========

What it does
------------

Filters CSV rows by removing those that contain a specific substring in a selected column.

Python usage
------------

.. code-block:: python

   from csvsmith.tools.filter_rows import DropRowsBySubstring

   cleaner = DropRowsBySubstring(
       "data.csv",
       column_name="status",
       unwanted_text="deprecated",
       case_sensitive=False
   )

   # Iterate over kept rows
   for row in cleaner.iter_kept_rows():
       print(row)

   # Or write directly to a new file (data.filtered.csv)
   cleaner.write_filtered_rows()

CLI usage
---------

.. code-block:: bash

   csvsmith drop-rows input.csv status "deprecated" --case-insensitive

Behavior notes
--------------

- **Output**: By default, it creates a new file with the suffix `.filtered.csv`.
- **Case Sensitivity**: Controlled by the `--case-insensitive` flag (CLI) or `case_sensitive` argument (Python).
- **Header**: The header row is preserved by default. Use `--drop-header` to remove it.
