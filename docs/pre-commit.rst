pre-commit
==========

``towncrier`` can also be used in your `pre-commit <https://pre-commit.com/>`_ configuration (``.pre-commit-config.yaml``) to check and/or update your news fragments on commit or during CI processes.

No additional configuration is needed in your ``towncrier`` configuration; the hook will read from the appropriate configuration files in your project.


Examples
--------

Usage with the default configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    repos:
      - repo: https://github.com/twisted/towncrier
        rev: 23.11.0  # run 'pre-commit autoupdate' to update
        hooks:
          - id: towncrier-check


Usage with custom configuration and directories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

News fragments are stored in ``changelog.d/`` in the root of the repository and we want to keep the news fragments when running ``update``:

.. code-block:: yaml

    repos:
      - repo: https://github.com/twisted/towncrier
        rev: 23.11.0  # run 'pre-commit autoupdate' to update
        hooks:
          - id: towncrier-update
            files: $changelog\.d/
            args: ['--keep']
