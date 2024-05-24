pre-commit
==========

``towncrier`` can also be used in your `pre-commit <https://pre-commit.com/>`_ configuration (``.pre-commit-config.yaml``) to check and/or update your news fragments on commit or during CI processes.

No additional configuration is needed in your ``towncrier`` configuration; the hook will read from the appropriate configuration files in your project.

.. code-block:: yaml

    repos:
      - repo: https://github.com/twisted/towncrier
        rev: 23.11.0  # run 'pre-commit autoupdate' to update
        hooks:
          - id: towncrier-checks


``towncrier-checks`` Hook
-------------------------

The ``towncrier-checks`` hook matches the ``towncrier check`` command, useful to check that a feature branch adds at least one news fragment.

This hook runs no matter which files were modified, only during the ``pre-push`` stage by default.


``towncrier-draft`` Hook
------------------------

The ``towncrier-draft`` hook matches the ``towncrier build --draft`` command, useful to create a draft of news fragments that will be added to the next release, ensuring they are formatted correctly.

This hook runs in all stages if any text files were added or modified.

.. note::

    The ``draft`` hook was previously (somewhat confusingly) named ``towncrier-check``.


``towncrier-update`` Hook
-------------------------

The ``towncrier-update`` hook matches the ``towncrier build`` command, which updates the changelog to a new version containing any news fragments.

It requires the version to be defined in your configuration file, or that is can be inferred from the Python package defined in your configuration file.
It uses the ``--yes`` flag to automatically confirm the git deletion of news fragments that are added to the changelog.

This hook runs no matter which files were modified, but only via the ``manual`` stage by default (meaning you run ``pre-commit run --hook-stage manual towncrier-update`` to update the changelog, or change the ``stages`` in your pre-commit configuration file).


Customizing the hook arguments
------------------------------

You can customize the hook arguments by adding them to the ``args`` key in your pre-commit configuration file.

.. code-block:: yaml

  repos:
    - repo: https://github.com/twisted/towncrier
      rev: 23.11.0  # run 'pre-commit autoupdate' to update
      hooks:
      - id: towncrier-checks
        args: ['--compare-with', 'trunk']
      - id: towncrier-update
        args: ['--config', 'custom.toml', '--directory', 'src/myapp']
