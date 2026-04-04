String Distance
===============

What it does
------------

Analyzes the similarity and relationship between two strings. It provides multiple ways to measure how close two strings are to being identical, including exact matches, case-insensitive matches, and structural matches (whitespace-normalized).

It implements two widely-used algorithms for string similarity:
- **Damerau-Levenshtein Distance**: Measures the number of single-character edits (insertions, deletions, substitutions, and transpositions of adjacent characters) required to change one string into another.
- **Jaro-Winkler Score**: A measure of similarity between two strings, where 0.0 is completely different and 1.0 is identical. It's particularly effective for short strings like names.

Python usage
------------

.. code-block:: python

   from csvsmith.utils.distance import analyze_pair

   # Compare two strings
   res = analyze_pair("Ames, IA", "Ames IA", ignore_case=True)

   print(f"Relation: {res.get_relation_string()}")
   print(f"Similarity: {res.similarity_percentage:.2f}%")
   print(f"Jaro-Winkler: {res.jaro_winkler_score:.4f}")

CLI usage
---------

.. code-block:: bash

   csvsmith string-distance "Apple Inc." "apple inc" --ignore-case

Behavior notes
--------------

- **Classifications**: 
    - ``Identical``: Exact character-for-character match.
    - ``Case-Insensitive Match``: Matches if case is ignored.
    - ``Similar (Trimmed)``: Matches after removing leading/trailing whitespace.
    - ``Synonymous (No Spaces)``: Matches after removing ALL internal whitespace.
    - ``Different``: No structural match found.
- **Similarity Percentage**: A normalized score derived from the Damerau-Levenshtein distance relative to the length of the longer string.
