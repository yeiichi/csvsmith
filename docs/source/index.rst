csvsmith documentation
======================

csvsmith is a toolkit for cleaning, transforming, and managing CSV-oriented workflows.

It provides both a command-line interface (CLI) and a Python API for building
reproducible data processing pipelines.

Example
-------

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx -o output.csv
   csvsmith dedupe data.csv -o clean.csv
   csvsmith clean-currency-numeric '$1,234.56'

Getting started
---------------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   recipes
   cli

Tools
-----

.. toctree::
   :maxdepth: 1

   tools/classify
   tools/clean-numeric
   tools/dedupe
   tools/drop-rows
   tools/excel2csv
   tools/find-matches
   tools/move-files
   tools/string-distance

Python API
----------

.. toctree::
   :maxdepth: 2

   python-api
   api/csvsmith
   api/tools
   api/utils

Development & History
---------------------

.. toctree::
   :maxdepth: 2

   development
   changelog
