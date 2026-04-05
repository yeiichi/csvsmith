Clean Numeric and Currency
==========================

What it does
------------

Normalizes and extracts numeric values from messy text strings. 
It handles group separators (thousands), and varied decimal separators. 

The ``clean-currency-numeric`` tool additionally handles currency symbols (like ``$``, ``¥``, ``€``).

Python usage
------------

.. code-block:: python

   from csvsmith.utils.clean_numeric import clean_numeric, clean_currency_numeric

   # Basic numeric cleaning
   val = clean_numeric("1,200.50")  # Returns 1200.5

   # Using localized separators (e.g., German style)
   val = clean_numeric("1.200,50", sep=".", decimal=",")  # Returns 1200.5

   # Cleaning values with currency symbols
   val = clean_currency_numeric("¥5,000")  # Returns 5000.0

   # Relaxed mode returns the original value if it can't be parsed
   val = clean_numeric("Not a number", relaxed=True)  # Returns "Not a number"

CLI usage
---------

To clean a standard numeric string:

.. code-block:: bash

   csvsmith clean-numeric "1,200.50" --sep "," --decimal "."

To clean a value that includes a currency symbol:

.. code-block:: bash

   csvsmith clean-currency-numeric "¥5,000" --sep "," --decimal "."

.. note::
   When using currency strings starting with ``$`` (e.g., ``"$1234.56"``) in shell scripts, 
   be aware that the shell might attempt to expand it as a variable. 
   Always use single quotes (``'$1234.56'``) to prevent unexpected expansion.

Behavior notes
--------------

- **Group Separators**: Commas, underscores, and non-breaking spaces are handled.
- **Negative Values**: Supports leading minus signs or values enclosed in parentheses (e.g., ``(100)`` becomes ``-100``).
- **Default Separators**: Defaults to ``,`` for thousands and ``.`` for decimal.