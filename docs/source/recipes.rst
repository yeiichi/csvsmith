Recipes
=======

This section demonstrates how to combine multiple `csvsmith` tools for common data-cleaning and organization workflows.

Cleaning and Deduplicating Excel Data
-------------------------------------

A common workflow: convert an Excel file to CSV, normalize its numeric columns, and then remove duplicate records.

**Shell Command Workflow:**

.. code-block:: bash

   # 1. Convert Excel to CSV
   csvsmith excel-to-csv data.xlsx -o raw_data.csv

   # 2. Clean numeric values (e.g., currency fields in "amount" column)
   csvsmith clean-numeric raw_data.csv --sep "," -o numeric_data.csv

   # 3. Remove duplicate records considering all columns
   csvsmith dedupe numeric_data.csv -o final_clean.csv --keep first --report report.json

**Python API Integration:**

.. code-block:: python

   from csvsmith.tools.excel2csv import excel_to_csv
   from csvsmith.utils.io import read_csv_rows, write_csv_rows
   from csvsmith.utils.clean_numeric import clean_numeric
   from csvsmith.tools.row_dedup import dedupe_with_report

   # 1. Convert
   csv_path = excel_to_csv("data.xlsx")

   # 2. Load and Clean
   rows = read_csv_rows(csv_path)
   for row in rows:
       row['amount'] = clean_numeric(row['amount'], relaxed=True)

   # 3. Deduplicate
   deduped, report = dedupe_with_report(rows)

   # 4. Save result
   write_csv_rows("final_clean.csv", deduped, fieldnames=rows[0].keys())

Organizing and Filtering Large Datasets
---------------------------------------

If you have a collection of files, you can automatically categorize them by structure, and then filter out rows based on a specific criteria.

**Shell Command Workflow:**

.. code-block:: bash

   # 1. Automatically categorize files into subdirectories based on their headers
   csvsmith classify raw_incoming/ organized/ --auto

   # 2. Process specific categorized files to filter out unwanted rows
   # For example, filtering files in a "user_logs" category
   csvsmith drop-rows organized/user_logs/data_1.csv status "internal_test"

   # 3. Archive or move the final CSV files
   csvsmith move-files organized/user_logs/ processed/ --suffixes csv
