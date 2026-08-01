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

Release versioning and tagging are handled by Python Semantic Release in
GitHub Actions. When commits land on ``main``, Semantic Release evaluates the
commit history, updates ``pyproject.toml`` and ``CHANGELOG.rst`` when a new
version is due, creates the version tag and GitHub release, and builds the
package distributions.

PyPI publishing then uses PyPI Trusted Publishing, so no long-lived PyPI API
token is stored in GitHub.

Before the first automated publish, configure a Trusted Publisher for the
``csvsmith`` project on PyPI with these values:

- Owner: ``yeiichi``
- Repository name: ``csvsmith``
- Workflow name: ``pypi.yml``
- Environment name: ``pypi``

To publish a release, merge commits using Conventional Commit messages such as
``feat: ...`` or ``fix: ...``. The release workflow runs after the merge to
``main``:

- ``feat`` creates a minor release.
- ``fix`` creates a patch release.
- breaking changes create a major release.

If no release-worthy commits are present, the workflow exits without creating
a release or publishing to PyPI.

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
