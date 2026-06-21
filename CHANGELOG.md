# CHANGELOG

<!-- version list -->

## v0.9.0 (2026-06-21)

### Features

- Add dense CSV concentration workflow
  ([`e6ae861`](https://github.com/yeiichi/csvsmith/commit/e6ae861651671f11e3270cd8bc1f0fdfc9f82c6f))


## v0.8.0 (2026-04-16)

### Chores

- Add Indian rupee sign (src/csvsmith/utils/clean_numeric.py)
  ([`aff4f25`](https://github.com/yeiichi/csvsmith/commit/aff4f2592ee44ac0d76e9b5ce71f19e3f79c3df6))

- Bump version to 0.7.3 after bug fixes and docs updates
  ([`0cea885`](https://github.com/yeiichi/csvsmith/commit/0cea8855ed455df4dda5180b2f0e0dea7becf0f4))

- Bump version to 0.7.3 after bug fixes and docs updates
  ([`e05cf51`](https://github.com/yeiichi/csvsmith/commit/e05cf51c46b70f79d57134c7db9743255cb87409))

### Documentation

- Clarify clean-numeric and add currency note
  ([`8bbf967`](https://github.com/yeiichi/csvsmith/commit/8bbf9671bba1c4074deed8bf0d4b2b42c8f8a64d))

- Switch Sphinx theme from alabaster to furo
  ([`9c470a2`](https://github.com/yeiichi/csvsmith/commit/9c470a213aa1d21373b63ee7970b1cd13c2615d0))

### Features

- Add strict-concat tool for CSV files and bump version to 0.8.0
  ([`73545a1`](https://github.com/yeiichi/csvsmith/commit/73545a192a37b4d07dbeded3fc56b86c1f670c92))


## v0.7.2 (2026-04-04)

### Chores

- Add docs/source/_static/.gitkeep
  ([`8b5a9e4`](https://github.com/yeiichi/csvsmith/commit/8b5a9e4e2383ed3650d1a6899bfb9a2a003cb30d))

- Add Read the Docs configuration
  ([`b3fcb6f`](https://github.com/yeiichi/csvsmith/commit/b3fcb6f6a5da3b91370c0689378c5a84f906ba8c))

### Documentation

- Add Read the Docs link (pyproject.toml; README.rst;)
  ([`a58a0de`](https://github.com/yeiichi/csvsmith/commit/a58a0dedd1827e671ef77c18d47078814e482b8c))

- Add Sphinx documentation directory
  ([`1b4a615`](https://github.com/yeiichi/csvsmith/commit/1b4a615f70f78229f2074a20f978f9f1f023ce43))

- Add to RTD requirements
  ([`6cdef9e`](https://github.com/yeiichi/csvsmith/commit/6cdef9eec415f7d23196c375e09eca0d8fe4e22e))

- Expose find_matches_in_csv API and document CLI usage
  ([`b79fc90`](https://github.com/yeiichi/csvsmith/commit/b79fc90b68e5e2bfb0f66690938b7fd909564045))

- Remove furo from RTD requirements
  ([`307ff39`](https://github.com/yeiichi/csvsmith/commit/307ff39a3f19544b14896b6ffc3fb63461ac2a89))

- Remove myst-parser from RTD requirements
  ([`11fd410`](https://github.com/yeiichi/csvsmith/commit/11fd41082b48c71471d437c1f862a2110e59b2eb))

### Features

- Expose find_matches_in_csv and bump version
  ([`0454e63`](https://github.com/yeiichi/csvsmith/commit/0454e63a91b76a32c743c667630069dbb88c868e))

### Refactoring

- Move clean_numeric into utils/ and update CLI/tests
  ([`4dd5d43`](https://github.com/yeiichi/csvsmith/commit/4dd5d439d00831672da0c9cf9c893490a7869a4a))


## v0.7.0 (2026-04-02)

### Refactoring

- Rename probe tool to find_matches_in_csv
  ([`3d5d5df`](https://github.com/yeiichi/csvsmith/commit/3d5d5df685447c2cbec17bffa2fad1811d6fc137))

- Reorganize CSVSmith modules into tools and utils packages
  ([`2830b5a`](https://github.com/yeiichi/csvsmith/commit/2830b5ad08799ea471fd7b0fcf634a76e20ca344))


## v0.6.0 (2026-04-02)

### Bug Fixes

- Correct version number, fix reST format (README.rst; pyproject.toml)
  ([`8d4bdb7`](https://github.com/yeiichi/csvsmith/commit/8d4bdb758d5ed33d03ef749266925cf1cda3a8f5))

### Chores

- Correct README.rst formatting
  ([`322e644`](https://github.com/yeiichi/csvsmith/commit/322e6446f43fcce34d34bb171c2d098e4fae4234))

### Documentation

- Refresh project metadata and documentation
  ([`d4adc13`](https://github.com/yeiichi/csvsmith/commit/d4adc132e728f3466ba015931a9bf21cf963ed61))

### Features

- Add relaxed mode to clean_numeric CLI
  ([`42d83e6`](https://github.com/yeiichi/csvsmith/commit/42d83e6a5bf5ec20018edd264f003708f3ba7ff0))

### Refactoring

- **string-distance**: Simplify strip_all implementation
  ([`66a12fc`](https://github.com/yeiichi/csvsmith/commit/66a12fc45b1f0aa2113272ed823f0e9309be8f08))


## v0.5.0 (2026-03-31)

### Bug Fixes

- README.rst format
  ([`3ead04c`](https://github.com/yeiichi/csvsmith/commit/3ead04c90701fbfafde14acd9911589261952868))

### Chores

- Resolve the version number discrepancy
  ([`55fc7b7`](https://github.com/yeiichi/csvsmith/commit/55fc7b753bccbcc7724aa06aa09e3a3d68204cf2))

### Features

- Add string_distance API and CLI
  ([`b5ee5b1`](https://github.com/yeiichi/csvsmith/commit/b5ee5b1a426fa57bc2a7e1d71134677521377d5f))


## v0.3.0 (2026-03-31)

### Refactoring

- Remove pandas dependency from row_dedup module
  ([`bde62a0`](https://github.com/yeiichi/csvsmith/commit/bde62a03e7fdd5acda242f98d7a5d316e2dddb5f))


## v0.2.3 (2026-03-25)

### Bug Fixes

- Correct syntax of README.rst
  ([`8b74951`](https://github.com/yeiichi/csvsmith/commit/8b74951b0090fe88fec32c87061c9838b8c91160))

### Chores

- Rename duplicates module to row_dedup and update related imports
  ([`90f1700`](https://github.com/yeiichi/csvsmith/commit/90f17003cde93a0d58e30e2dafd5d07934b1225e))


## v0.2.2 (2026-03-24)

### Chores

- Update src/csvsmith/__init__.py
  ([`176d6f9`](https://github.com/yeiichi/csvsmith/commit/176d6f9df1c383913631316bd7f20017790083ef))

### Features

- Rename CSVCleaner to DropRowsBySubstring
  ([`387d895`](https://github.com/yeiichi/csvsmith/commit/387d8955d2e1950cb7801fa56f873b5714b2beb5))


## v0.2.1 (2026-02-21)


## v0.2.0 (2026-01-21)

### Chores

- Add CSVClassifer (src/csvsmith/__init__.py)
  ([`eab1b0e`](https://github.com/yeiichi/csvsmith/commit/eab1b0e59c0c1cd2fc81cf1644d92e31b9d13b5e))

### Testing

- Add suite for CSV classification engine
  ([`58e5257`](https://github.com/yeiichi/csvsmith/commit/58e525783a922df5f2537f5622be47b683e11cfe))


## v0.1.1 (2026-01-21)

- Initial Release
