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
  │   └── NEWS.rst
  ├── project_b
  │   ├── newsfragments
  │   │   └── 120.bugfix
  │   ├── project_b
  │   │   └── __init__.py
  │   └── NEWS.rst
  └── towncrier.toml

The ``towncrier.toml`` looks like this:

.. code-block:: toml

  [tool.towncrier]
  # It's important to keep these config fields empty
  # because we have more than one package/name to manage.
  package = ""
  name = ""

Now to add a fragment:

.. code-block:: console

   towncrier create --config towncrier.toml --dir project_a  124.added

This should create a file at ``project_a/newsfragments/124.added``.

To build the news file for the same project:

.. code-block:: console

   towncrier build --config towncrier.toml --dir project_a --version 1.5

If ``project_a`` has a ``pyproject.toml``, its ``[project.name]`` and static ``[project.version]`` are used, so ``--version`` can be omitted:

.. code-block:: console

   towncrier build --config towncrier.toml --dir project_a
