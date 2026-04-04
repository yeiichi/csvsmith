Development
===========

Running tests
-------------

We use `pytest` for testing. You can run all tests with:

.. code-block:: bash

   pytest

Local docs build
----------------

To build the documentation locally, you need Sphinx installed.

.. code-block:: bash

   sphinx-build -b html docs/source docs/build/html

The generated HTML files will be in `docs/build/html`.

Contributing
------------

We welcome contributions! To get started:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. **Install dependencies** (see :doc:`installation`).
4. **Create a branch** for your feature or bug fix.
5. **Add tests** for any new functionality in the ``tests/`` directory.
6. **Submit a Pull Request** with a clear description of your changes.

Code Checklist
^^^^^^^^^^^^^^

Before submitting a PR, please ensure:

- Your code follows PEP 8 style guidelines.
- All tests pass (run ``pytest``).
- New features are documented in the ``docs/source/tools/`` or ``api/`` directories.
- The ``CHANGELOG.rst`` is updated if you've made user-facing changes.

Notes
-----

- Follow PEP 8 style guidelines.
- Add tests for any new features or bug fixes.
- Update the documentation when changing user-facing behavior.
- Use `pyproject.toml` to manage dependencies.
