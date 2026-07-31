Generate sample CSV files
=========================

The sample CSV tool creates small data files for examples, demos, tests, and
manual workflow checks. It writes predictable columns containing an ID, date,
category, two item strings, a numeric value, and a formatted amount.

Command line
------------

Create a sample CSV using the defaults:

.. code-block:: console

   csvsmith sample-csv

Set the output path, row count, start date, and random seed:

.. code-block:: console

   csvsmith sample-csv -o sample.csv --rows 16 --start 2026-01-01 --seed 42

Use non-ASCII item strings:

.. code-block:: console

   csvsmith sample-csv --item-charset kanji

``--item-charset`` accepts ``ascii``, ``kanji``, or ``mix``. Use ``--seed``
when a reproducible sample file is useful for tests or documentation.

Python API
----------

.. code-block:: python

   from csvsmith import create_sample_csv

   result = create_sample_csv(
       row_count=16,
       start="2026-01-01",
       output_path="sample.csv",
       seed=42,
   )

   print(result.output_path)

The API returns a ``SampleCSVResult`` with the written path and row count.
