Multiple Projects Share One Config (Monorepo)
=============================================

Several projects may have independent release notes with the same format.
For instance packages in a monorepo.
Here's how you can use towncrier to set this up.

Below is a minimal example:

.. code-block:: text

  repo
  ├── project_a
  │   ├── newsfragments
  │   │   └── 123.added
  │   ├── project_a
  │   │   └── __init__.py
  │   ├── NEWS.rst
  │   └── pyproject.toml
  ├── project_b
  │   ├── newsfragments
  │   │   └── 120.bugfix
  │   ├── project_b
  │   │   └── __init__.py
  │   ├── NEWS.rst
  │   └── pyproject.toml
  └── towncrier.toml

The ``towncrier.toml`` looks like this:

.. code-block:: toml

  [tool.towncrier]
  # It's important to keep these config fields empty
  # because we have more than one package/name to manage.
  package = ""
  name = ""

Each ``pyproject.toml`` provides the project's name and version:

.. code-block:: toml

  [project]
  name = "project_a"
  version = "1.5"

Now to add a fragment:

.. code-block:: console

   towncrier create --config towncrier.toml --dir project_a  124.added

This should create a file at ``project_a/newsfragments/124.added``.

To build the news file for the same project:

.. code-block:: console

   towncrier build --config towncrier.toml --dir project_a

The name and version are read from ``project_a/pyproject.toml``.
If the version is dynamic, pass it explicitly with ``--version``.
