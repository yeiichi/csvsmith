Quickstart
==========

Welcome to `csvsmith`! This guide will help you get started with the most common tasks.

1. Convert an Excel file to CSV
-------------------------------

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx -o output.csv

2. Remove duplicate rows
------------------------

.. code-block:: bash

   csvsmith dedupe data.csv -o clean.csv --subset id,name

3. Clean numeric fields
-----------------------

.. code-block:: bash

   csvsmith clean-numeric "3,000" --sep ","

4. Find a specific value in a CSV
---------------------------------

.. code-block:: bash

   csvsmith find-matches data.csv "Alice"

5. Filter rows by substring
---------------------------

.. code-block:: bash

   csvsmith drop-rows data.csv status "deprecated"