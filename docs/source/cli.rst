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

- ``excel-to-csv`` — Convert Excel files to CSV
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

This will display:

- available options
- required arguments
- usage examples

---

Notes
-----

- Commands are designed to be composable in scripts and pipelines.
- Input files are not modified unless explicitly overwritten.