Quickstart
==========

csvsmith provides small tools that can be used independently or combined in a
CSV workflow. Start with the task closest to your data; command-specific
options live on the linked tool pages.

Convert a worksheet
-------------------

Convert the first worksheet in an Excel workbook:

.. code-block:: console

   csvsmith excel-to-csv input.xlsx -o output.csv

Use ``--sheet-name`` when the workbook contains multiple worksheets. See
:doc:`tools/excel2csv`.

Inspect and compare data
------------------------

Find exact normalized matches anywhere in a CSV:

.. code-block:: console

   csvsmith find-matches data.csv "Alice" --ignore-case

Compare two individual strings:

.. code-block:: console

   csvsmith string-distance "Apple Inc." "apple inc" --ignore-case

See :doc:`tools/find-matches` and :doc:`tools/string-distance`.

Filter and deduplicate rows
---------------------------

Remove rows whose ``status`` column contains ``deprecated``:

.. code-block:: console

   csvsmith drop-rows data.csv status "deprecated" --case-insensitive

Remove duplicate rows using selected columns:

.. code-block:: console

   csvsmith dedupe data.csv -o clean.csv --subset id,name --report duplicates.json

To inspect duplicates without writing a deduplicated file:

.. code-block:: console

   csvsmith row-duplicates data.csv --subset id,name

See :doc:`tools/drop-rows` and :doc:`tools/dedupe`.

Combine compatible CSV files
----------------------------

Concatenate every CSV in a directory when their headers match exactly:

.. code-block:: console

   csvsmith strict-concat incoming/ -o combined.csv

The output includes a ``file_stem`` column identifying each source file. See
:doc:`tools/strict-concat`.

Organize file collections
-------------------------

Preview automatic CSV classification by header:

.. code-block:: console

   csvsmith classify incoming/ organized/ --auto --dry-run

Move files by suffix:

.. code-block:: console

   csvsmith move-files organized/ processed/ --suffixes csv,pdf

``classify`` supports ``--dry-run``; ``move-files`` always performs the move.
See :doc:`tools/classify` and :doc:`tools/move-files`.

Concentrate repeated long values
--------------------------------

Replace repeated values in selected columns with deterministic tokens, then
restore them later using the generated map:

.. code-block:: console

   csvsmith concentrate input.csv --columns description,notes
   csvsmith rehydrate input.dense.csv -m input.dense-map.json -o restored.csv

This workflow is intended for long, repeated values; it can enlarge data made
mostly of short strings. See :doc:`tools/dense-csv` for scope and storage
trade-offs.

Clean individual numeric values
-------------------------------

Normalize a numeric or currency string:

.. code-block:: console

   csvsmith clean-numeric "3,000.50"
   csvsmith clean-currency-numeric '$3,000.50'

These commands process one value at a time. For CSV-wide transformations, use
the Python API in a script. See :doc:`tools/clean-numeric`.

Next steps
----------

- Browse :doc:`cli` for the complete command list.
- Use :doc:`python-api` when integrating csvsmith into Python code.
- See :doc:`recipes` for a few multi-step workflows.
