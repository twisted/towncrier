Command Line Reference
======================

The following options can be passed to all of the commands that explained below:

.. option:: --config FILE_PATH

   Pass a custom config file at ``FILE_PATH``.

   Default: ``towncrier.toml`` or ``pyproject.toml`` file.
   If both files exist, the first will take precedence

.. option:: --dir PATH

   Build fragment in ``PATH``.

   Default: current directory.


``towncrier build``
-------------------

Build the combined news file from news fragments.
``build`` is also assumed if no command is passed.

.. option:: --draft

   Don't stage changes nor remove fragments.
   If option ``--filename`` is provided, write the news there;
   otherwise, render the fragments **without** the surrounding template to ``stdout``.

.. option:: --name NAME

   Use `NAME` as project name in the news file.
   Can be configured.

.. option:: --version VERSION

   Use ``VERSION`` in the rendered news file.
   Can be configured or guessed (default).

.. option:: --date DATE

   The date in `ISO format <https://xkcd.com/1179/>`_ to use in the news file.

   Default: today's date

.. option:: --filename FILENAME

   Use `FILENAME` to override field ``filename`` from the configuration.
   If used together with ``--draft``, write to ``FILENAME`` instead of ``stdout``.

.. option:: --yes

   Do not ask for confirmations.
   Useful for automated tasks.

.. option:: --keep

   Don't delete news fragments after the build and don't ask for confirmation whether to delete or keep the fragments.


``towncrier create``
--------------------

Create a news fragment in the directory that ``towncrier`` is configured to look for fragments::

   $ towncrier create 123.bugfix.rst

``towncrier create`` will enforce that the passed type (e.g. ``bugfix``) is valid.

If the filename exists already, ``towncrier create`` will add (and then increment) a number after the fragment type until it finds a filename that does not exist yet.
In the above example, it will generate ``123.bugfix.1.rst`` if ``123.bugfix.rst`` already exists.

.. option:: --content, -c CONTENT

   A string to use for content.
   Default: an instructive placeholder.

.. option:: --edit

   Create file and start `$EDITOR` to edit it right away.`


``towncrier check``
-------------------

To check if a feature branch adds at least one news fragment, run::

   $ towncrier check

The check is automatically skipped when the main news file is modified inside the branch as this signals a release branch that is expected to not have news fragments.

By default, ``towncrier`` compares the current branch against ``origin/main`` (and falls back to ``origin/master`` with a warning if it exists, *for now*).

.. option:: --compare-with REMOTE-BRANCH

   Use ``REMOTE-BRANCH`` instead of ``origin/main``::

      $ towncrier check --compare-with origin/trunk
