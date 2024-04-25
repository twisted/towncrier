Command Line Reference
======================

The following options can be passed to all of the commands that explained below:

.. option:: --config FILE_PATH

   Pass a custom config file at ``FILE_PATH``.

   Default: ``towncrier.toml`` or ``pyproject.toml`` file.
   If both files exist, the first will take precedence

.. option:: --dir PATH

   The command is executed relative to ``PATH``.
   For instance with the default config news fragments are checked and added in ``PATH/newsfragments`` and the news file is built in ``PATH/NEWS.rst``.

   Default: current directory.


``towncrier build``
-------------------

Build the combined news file from news fragments.
``build`` is also assumed if no command is passed.

If there are no news fragments (including an empty fragments directory or a
non-existent directory), a notice of "no significant changes" will be added to
the news file.

By default, the processed news fragments are removed using ``git``, which will
also remove the fragments directory if now empty.

.. option:: --draft

   Only render news fragments to standard output.
   Don't write to files, don't check versions.
   Only renders the news fragments **without** the surrounding template.

.. option:: --name NAME

   Use `NAME` as project name in the news file.
   Can be configured.

.. option:: --version VERSION

   Use ``VERSION`` in the rendered news file.
   Can be configured or guessed (default).

   This option requires the ``build`` command to be explicitly passed.

.. option:: --date DATE

   The date in `ISO format <https://xkcd.com/1179/>`_ to use in the news file.

   Default: today's date

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

If the fragments directory does not exist, it will be created.

If the filename exists already, ``towncrier create`` will add (and then increment) a number after the fragment type until it finds a filename that does not exist yet.
In the above example, it will generate ``123.bugfix.1.rst`` if ``123.bugfix.rst`` already exists.

To create a news fragment not tied to a specific issue (which towncrier calls an "orphan fragment"), start the fragment name with a ``+``.
If that is the entire fragment name, a random hash will be added for you::

   $ towncrier create +.feature.rst
   $ ls newsfragments/
   +fcc4dc7b.feature.rst

.. option:: --content, -c CONTENT

   A string to use for content.
   Default: an instructive placeholder.

.. option:: --edit

   Create file and start `$EDITOR` to edit it right away.


``towncrier check``
-------------------

To check if a feature branch adds at least one news fragment, run::

   $ towncrier check

The check is automatically skipped when the main news file is modified inside the branch as this signals a release branch that is expected to not have news fragments.

By default, ``towncrier`` compares the current branch against ``origin/main`` (and falls back to ``origin/master`` with a warning if it exists, *for now*).

.. option:: --compare-with REMOTE-BRANCH

   Use ``REMOTE-BRANCH`` instead of ``origin/main``::

      $ towncrier check --compare-with origin/trunk
