Mark rows by knapsack capacity
==============================

The knapsack tool selects target-column values whose sum is as large as
possible without exceeding a capacity. It is useful when you want to pick CSV
rows that fit within a numeric budget, size, or other limit.

Values may contain thousands separators, so both ``1105.857`` and
``1,105.857`` are accepted.

Command line
------------

Mark rows in ``value`` whose sum best fits ``2036``:

.. code-block:: console

   csvsmith knapsack sample.csv value 2036 -o marked.csv

By default, the output path is ``<input-stem>.knapsack.csv`` and the added
column is named ``<target-column>_knapsack``. Selected rows are marked with
``yes``.

Customize the marker column and selected value:

.. code-block:: console

   csvsmith knapsack sample.csv value 2036 \
       --mark-column selected --mark-value knapsack

Python API
----------

.. code-block:: python

   from csvsmith import find_knapsack_indices

   indices = find_knapsack_indices("sample.csv", "value", "2,036")

The API returns zero-based data-row indices. Header rows are not counted.
