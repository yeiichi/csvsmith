Concentrate and rehydrate CSV values
====================================

The dense CSV tool replaces repeated, nonblank values with deterministic
SHA-256 tokens and writes a separate JSON map that can restore them.

This is tokenization and deduplication, not general-purpose compression.
Short values or small datasets may not become smaller after the JSON map is
included. By default, a value must appear at least twice before it is replaced.

Intended scope
--------------

Dense CSV is designed for spreadsheet-oriented and medium-sized CSV files,
roughly in the 100 MB class. It is a practical fit for files that are still
reasonable to inspect or exchange as CSV but contain long values repeated
across many rows.

Concentration makes two passes over the source CSV:

#. Count values in the selected columns.
#. Write the concentrated CSV and its map.

The CSV rows are processed incrementally, but the value counts and mapped
values are held in memory. Actual memory use therefore depends on the number
and size of distinct values, not only the source file size. The 100 MB figure
describes the intended workload rather than a fixed or benchmarked limit.

For substantially larger datasets, particularly gigabyte-scale pipelines or
data-lake workloads, avoid passing flat CSV files and JSON maps downstream.
A binary columnar format such as Apache Parquet will usually provide better
storage efficiency, typed data, and selective reads.

Token size and storage trade-offs
---------------------------------

Each mapped value uses a 64-character SHA-256 hexadecimal digest. To make
tokens recognizable and safe to rehydrate, csvsmith stores the digest with the
``csvsmith:sha256:`` prefix. The complete token is therefore 79 ASCII
characters, or 79 bytes in UTF-8.

The JSON map also stores one copy of every mapped value and its digest.
Storage comparisons should therefore include both output files:

- the concentrated CSV
- the dense CSV JSON map

.. warning::

   Concentration does not guarantee a smaller combined output. Replacing short
   values such as ``True``, ``M``, or ``NY`` with a 79-character token will
   increase the CSV size.

Dense CSV works best when selected columns contain values that are both:

- substantially longer than the token
- repeated often enough to offset the map entry

Use ``--columns`` to avoid tokenizing short identifiers, flags, state codes,
and other compact fields. ``--min-occurrences`` can raise the repetition
threshold when a dataset contains many low-frequency values.

Reducing downstream work
------------------------

Dense CSV can be useful even when the concentrated files are larger than the
source. In pipelines where processing a value is expensive, process each
mapped value once and reuse the result for every occurrence of its token.
Examples include remote API calls, model inference, enrichment, normalization,
and other per-value transformations.

After concentration, the CLI reports:

.. code-block:: text

   Potential repeated-operation reduction for mapped values: 855/937 (91.2%)

This calculation is:

.. math::

   \frac{\text{mapped cell occurrences} - \text{unique mapped values}}
        {\text{mapped cell occurrences}} \times 100

In this example, 937 mapped cells share 82 unique values, so a downstream
consumer could avoid repeating 855 operations if it processes the map values
once and fans the results back out.

This percentage applies only to mapped cells. It is not:

- the reduction in CSV or combined output size
- the reduction across unmapped values
- a guarantee of cost or latency savings for the complete pipeline

Character-, token-, or request-based services may use different billing units.
For those systems, measure the relevant units across unique map values versus
all mapped occurrences.

Command line
------------

Concentrate repeated values in all columns:

.. code-block:: console

   csvsmith concentrate input.csv

By default, this writes ``input.dense.csv`` and
``input.dense-map.json`` beside the source file.

Limit concentration to selected columns:

.. code-block:: console

   csvsmith concentrate input.csv --columns description,notes \
       --min-occurrences 3

Use ``--output`` and ``--map`` to override either generated path:

.. code-block:: console

   csvsmith concentrate input.csv -o compact.csv -m compact-map.json

Restore the original values:

.. code-block:: console

   csvsmith rehydrate input.dense.csv -m input.dense-map.json -o restored.csv

The input CSV, output CSV, and map paths must be different. Output files are
written through temporary files so validation or processing failures do not
replace existing outputs.

Python API
----------

.. code-block:: python

   from csvsmith import concentrate_csv, rehydrate_csv

   result = concentrate_csv(
       "input.csv",
       "dense.csv",
       "dense-map.json",
       columns=["description", "notes"],
       min_occurrences=2,
   )

   restored = rehydrate_csv(
       "dense.csv",
       "dense-map.json",
       "restored.csv",
   )

The API returns immutable result objects containing row and transformed-cell
counts. Errors are reported with exceptions; the API does not print messages
or terminate the Python process.

Map safety
----------

The JSON map has a versioned format and records:

- the hash algorithm and token prefix
- the complete CSV header
- the indices and names of transformed columns
- the digest-to-original-value mapping

Rehydration validates this metadata and only examines the recorded columns.
This prevents ordinary values in unrelated columns from being mistaken for
tokens.
