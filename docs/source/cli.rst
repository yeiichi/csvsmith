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
- ``drop-rows`` — Filter rows based on conditions

File operations
^^^^^^^^^^^^^^^

- ``excel2csv`` — Convert Excel files to CSV
- ``move-files`` — Move or organize files based on rules

Analysis
^^^^^^^^

- ``classify`` — Categorize or label data
- ``find-matches`` — Search for matching records

See the *Tools* section for detailed usage of each command.

---

Quick examples
--------------

Convert Excel to CSV:

.. code-block:: bash

   csvsmith excel2csv input.xlsx -o out/

Remove duplicates:

.. code-block:: bash

   csvsmith dedupe data.csv -o clean.csv

Clean numeric fields:

.. code-block:: bash

   csvsmith clean-numeric data.csv -c amount -o normalized.csv

Clean currency-prefixed numeric fields:

.. code-block:: bash

   csvsmith clean-currency-numeric '$1,234.56'

.. note::

   In Python, normal string quoting is fine. In the shell, values containing
   ``$`` should usually be single-quoted to avoid expansion.

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

This will display:

- available options
- required arguments
- usage examples

---

Notes
-----

- Commands are designed to be composable in scripts and pipelines.
- Input files are not modified unless explicitly overwritten.