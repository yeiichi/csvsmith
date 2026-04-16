Strict Concat
=============

What it does
------------

Concatenates multiple CSV files into a single output, ensuring that all files have identical headers.
It also adds a ``file_stem`` column to the output so you can track the source of each row.

Python usage
------------

.. code-block:: python

   from csvsmith import strict_concat_rows, save_csv

   # Concatenate all CSV files in a directory
   rows = strict_concat_rows("path/to/csv_dir")

   # Save the result to a new file
   save_csv(rows, "combined.csv")

CLI usage
---------

.. code-block:: bash

   csvsmith strict-concat path/to/csv_dir -o combined.csv

Behavior notes
--------------

- **Header Validation**: All CSV files in the target directory must have the exact same header (column names and order). If any file has a different header, a ``ValueError`` is raised.
- **Source Tracking**: A new first column named ``file_stem`` is added to the output, containing the filename (without extension) of the source file for each row.
- **Encoding**: Reads files using ``utf-8-sig`` (to handle BOM) and writes the output in ``utf-8``.
