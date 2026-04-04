Clean Numeric
=============

What it does
------------

Normalizes and extracts numeric values from messy text strings. 
It handles currency symbols, group separators (thousands), and varied decimal separators.

Python usage
------------

.. code-block:: python

   from csvsmith.utils.clean_numeric import clean_numeric

   # Basic usage
   val = clean_numeric("1,200.50")  # Returns 1200.5

   # Using localized separators (e.g., German style)
   val = clean_numeric("1.200,50", sep=".", decimal=",")  # Returns 1200.5

   # Relaxed mode returns the original value if it can't be parsed
   val = clean_numeric("Not a number", relaxed=True)  # Returns "Not a number"

CLI usage
---------

.. code-block:: bash

   csvsmith clean-numeric "¥5,000" --sep "," --decimal "."

Behavior notes
--------------

- **Group Separators**: Commas, underscores, and non-breaking spaces are handled.
- **Negative Values**: Supports leading minus signs or values enclosed in parentheses (e.g., ``(100)`` becomes ``-100``).
- **Default Separators**: Defaults to ``,`` for thousands and ``.`` for decimal.