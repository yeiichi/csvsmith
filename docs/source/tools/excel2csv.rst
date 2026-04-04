Excel to CSV
============

What it does
------------

Converts an Excel worksheet (.xlsx or .xls) into a CSV file.
By default, it converts the first worksheet.

Python usage
------------

.. code-block:: python

   from csvsmith.tools.excel2csv import excel_to_csv

   # Simple conversion
   csv_path = excel_to_csv("input.xlsx")

   # Specify output path and worksheet name
   excel_to_csv("data.xlsx", "output.csv", sheet_name="Sheet2")

CLI usage
---------

.. code-block:: bash

   csvsmith excel-to-csv input.xlsx -o output.csv --sheet-name "Data"

Behavior notes
--------------

- Requires `openpyxl` for .xlsx files.
- The output CSV is encoded in UTF-8.
- If no output path is specified, it uses the input file's name with a `.csv` extension.
