CLI Reference
=============

csvsmith provides a command-line interface (CLI) for common CSV processing tasks.

All commands follow this general structure:

.. code-block:: bash

   csvsmith <command> [options]

---

Available commands
------------------

The following subcommands are available:

Data transformation
^^^^^^^^^^^^^^^^^^^

- ``clean-numeric`` — Normalize numeric values in text fields
- ``clean-currency-numeric`` — Normalize currency-prefixed numeric values
- ``dedupe`` — Remove duplicate rows
- ``row-duplicates`` — Print rows that belong to duplicate groups
- ``drop-rows`` — Filter rows based on conditions
- ``concentrate`` — Replace repeated values with deterministic tokens
- ``rehydrate`` — Restore tokenized values using a dense CSV map
- ``sample-csv`` — Generate a sample CSV file for tests and examples
- ``knapsack`` — Mark rows whose values best fit a capacity

File operations
^^^^^^^^^^^^^^^

- ``excel-to-csv`` — Convert Excel files to CSV
- ``move-files`` — Move or organize files based on rules
- ``strict-concat`` — Concatenate CSV files with identical headers

Analysis
^^^^^^^^

- ``classify`` — Categorize or label data
- ``find-matches`` — Search for matching records
- ``string-distance`` — Compare two strings using similarity metrics

See the *Tools* section for detailed usage of each command.

---

Quick examples
--------------

Convert Excel to CSV:

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx -o output.csv

Remove duplicates:

.. code-block:: bash

   csvsmith dedupe data.csv -o clean.csv

Clean numeric fields:

.. code-block:: bash

   csvsmith clean-numeric "1,200.50" --sep "," --decimal "."

Clean currency-prefixed numeric fields:

.. code-block:: bash

   csvsmith clean-currency-numeric '$1,234.56'

Concentrate and restore repeated CSV values:

.. code-block:: bash

   csvsmith concentrate input.csv
   csvsmith rehydrate input.dense.csv -m input.dense-map.json -o restored.csv

Generate a sample CSV:

.. code-block:: bash

   csvsmith sample-csv -o sample.csv --rows 16 --seed 42

Mark rows whose values best fit a capacity:

.. code-block:: bash

   csvsmith knapsack sample.csv value 2036 -o marked.csv

.. note::
   When using values starting with ``$`` (e.g., ``"$1234.56"``) in the shell, 
   be aware that the shell might attempt to expand it as a variable. 
   Always use single quotes (``'$1234.56'``) to prevent unexpected expansion.

---

Global options
--------------

Some options are shared across multiple commands:

- ``-o, --output``  
  Specify output file or directory.

- ``-h, --help``  
  Show help message for a command.

To see command-specific options:

.. code-block:: bash

   csvsmith <command> --help

---

Command help
------------

Each subcommand provides its own help message:

.. code-block:: bash

   csvsmith clean-numeric --help

This displays:

- available options
- required arguments

---

Notes
-----

- Commands are designed to be composable in scripts and pipelines.
- Commands that write CSV output use a separate output path or generated
  suffix. File-organization commands such as ``classify`` and ``move-files``
  move source files by design.
