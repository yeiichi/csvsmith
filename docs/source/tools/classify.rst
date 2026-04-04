Classify
========

What it does
------------

Categorizes CSV files into subdirectories based on their header rows. This is useful for organizing large collections of CSV files that share similar structures.

Python usage
------------

.. code-block:: python

   from csvsmith.tools.classify import CSVClassifier

   classifier = CSVClassifier(
       source_dir="raw_data",
       dest_dir="organized_data",
       auto=True  # Automatically create categories based on headers
   )

   classifier.run()

CLI usage
---------

.. code-block:: bash

   csvsmith classify raw_data/ organized_data/ --auto

Behavior notes
--------------

- **Modes**: 
    - ``strict``: Matches headers exactly (including order).
    - ``relaxed``: Ignores column order and case.
- **Auto-categorization**: If ``--auto`` is used, files with the same header structure are moved into the same generated subdirectory.
- **Dry Run**: Use ``--dry-run`` to see which files would be moved without actually moving them.
