View CSV files
==============

The view tool prints CSV rows as a compact text table. It can show the first
rows, select columns, and apply simple filters from the command line.

Command line
------------

View a CSV file:

.. code-block:: console

   csvsmith view sample.csv

Show the first rows:

.. code-block:: console

   csvsmith view sample.csv --head 5

Select columns and filter rows:

.. code-block:: console

   csvsmith view sample.csv --columns date,value --filter value ">" 700

By default, numeric-looking values are converted before filters are evaluated.
Use ``--no-convert-types`` to compare all values as strings.

When stdout and stdin are connected to a terminal, ``csvsmith view`` paginates
larger output. Use ``--page-size`` to control the number of rows per page.

Python API
----------

.. code-block:: python

   from csvsmith import DataFrame, build_filter

   df = DataFrame.from_csv("sample.csv")
   filtered = df.filter(build_filter("value", ">", "700")).select(["date", "value"])

   print(filtered.head(5))

The API returns formatted tables as strings via ``render`` and ``head``.
