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

Release publishing
------------------

PyPI publishing is handled by GitHub Actions when a version tag is pushed.
The workflow uses PyPI Trusted Publishing, so no long-lived PyPI API token is
stored in GitHub.

Before the first automated publish, configure a Trusted Publisher for the
``csvsmith`` project on PyPI with these values:

- Owner: ``yeiichi``
- Repository name: ``csvsmith``
- Workflow name: ``pypi.yml``
- Environment name: ``pypi``

To publish a release, make sure ``pyproject.toml`` contains the intended
version, then create and push the matching tag:

.. code-block:: bash

   git tag v0.10.0
   git push origin v0.10.0

The PyPI workflow builds the source distribution and wheel, checks them with
Twine, and publishes them to PyPI.

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
