Find Matches
============

What it does
------------

Scans a CSV file for a specific target string and returns its coordinates (row and column) along with associated data from the same row.

Python usage
------------

.. code-block:: python

   from csvsmith.tools.find_matches_in_csv import find_matches_in_csv

   # Find "Alice" in the CSV
   results = find_matches_in_csv("data.csv", "Alice")

   for match in results:
       print(f"Found {match['match']} at {match['coords']}")
       print(f"Row data: {match['data']}")

CLI usage
---------

.. code-block:: bash

   csvsmith find-matches input.csv "Alice" --ignore-case

Behavior notes
--------------

- **Search**: Case-insensitive and whitespace-ignoring by default.
- **NFKC Normalization**: Enabled by default to handle Unicode variations.
- **Result Output**: In CLI, results are displayed as a JSON list.
