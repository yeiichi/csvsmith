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
   csvsmith concentrate input.csv
   csvsmith sample-csv -o sample.csv --rows 16
   csvsmith view sample.csv --head 5
   csvsmith knapsack sample.csv value 2036 -o marked.csv
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
   tools/dense-csv
   tools/dedupe
   tools/drop-rows
   tools/excel2csv
   tools/find-matches
   tools/knapsack
   tools/move-files
   tools/sample-csv
   tools/view
   tools/strict-concat
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
