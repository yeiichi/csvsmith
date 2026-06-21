Python API
==========

csvsmith also provides a Python API for integrating CSV cleaning and transformation
logic into scripts, applications, and data-processing workflows.

Use the Python API when you want to:

- call csvsmith functionality from Python code
- reuse cleaning or matching logic programmatically
- build repeatable pipelines without shell commands

---

Overview
--------

The Python API complements the command-line interface (CLI).

- Use the CLI for one-off tasks and shell workflows.
- Use the Python API when you need direct integration in Python code.

For command-oriented usage, see :doc:`cli`.

For detailed module reference, see:

- :doc:`api/csvsmith`
- :doc:`api/tools`
- :doc:`api/utils`

---

Typical import style
--------------------

Import from public modules whenever possible.

.. code-block:: python

   from csvsmith import clean_numeric

   value = clean_numeric("1,234")

---

Example
-------

Clean a list of numeric-like values:

.. code-block:: python

   from csvsmith import clean_numeric

   values = ["1,200", "¥3,000", "N/A", " 42 ", 7]
   cleaned = [clean_numeric(v, relaxed=True) for v in values]

   print(cleaned)

Expected result:

.. code-block:: python

   [1200.0, "¥3,000", "N/A", 42.0, 7.0]

---

When to use the Python API
--------------------------

The Python API is a good fit when you want to:

- preprocess values before writing CSV output
- integrate csvsmith logic into a larger ETL or data-cleaning script
- test data-processing behavior directly in Python
- avoid shelling out to CLI commands from application code

---

Relationship to tool pages
--------------------------

Some tool pages describe behavior that is also useful from Python.

Examples:

- :doc:`tools/clean-numeric`
- :doc:`tools/dense-csv`
- :doc:`tools/find-matches`

The tool pages explain user-facing behavior, while the API reference documents
modules, functions, and classes.

---

Reference
---------

For full module-level documentation, see:

.. toctree::
   :maxdepth: 1

   api/csvsmith
   api/tools
   api/utils

---

Notes
-----

- Prefer stable, public imports over internal implementation modules.
- Keep CLI usage and Python usage documented separately.
- If a function is primarily internal, document it in the API reference rather
  than this overview page.
