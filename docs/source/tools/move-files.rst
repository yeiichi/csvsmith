Move Files
==========

What it does
------------

Moves files from a source directory to a destination directory based on their file extensions (suffixes).

Python usage
------------

.. code-block:: python

   from csvsmith.tools.move_files import move_by_suffix

   # Move all CSV and PDF files
   count = move_by_suffix(
       src_dir="raw_data",
       dst_dir="processed_data",
       suffixes=[".csv", ".pdf"]
   )

   print(f"Moved {count} files")

CLI usage
---------

.. code-block:: bash

   csvsmith move-files raw_data/ processed_data/ --suffixes csv,pdf

Behavior notes
--------------

- **Suffix Matching**: Case-insensitive and supports suffixes with or without a leading dot (e.g., ``csv`` or ``.csv``).
- **Default Suffixes**: Defaults to ``.csv`` and ``.pdf`` if none are specified.
