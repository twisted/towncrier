Hear ye, hear ye, says the ``towncrier``
========================================

.. image:: https://travis-ci.org/hawkowl/towncrier.svg?branch=master
    :target: https://travis-ci.org/hawkowl/towncrier

.. image:: https://codecov.io/github/hawkowl/towncrier/coverage.svg?branch=master
    :target: https://codecov.io/github/hawkowl/towncrier?branch=master

``towncrier`` is a utility to produce useful, summarised news files for your project.
Rather than reading the Git history as some newer tools to produce it, or having one single file which developers all write to, ``towncrier`` reads "news fragments" which contain information `useful to end users`.

Philosophy
----------

``towncrier`` delivers the news which is convenient to those that hear it, not those that write it.

That is, by duplicating what has changed from the "developer log" (which may contain complex information about the original issue, how it was fixed, who authored the fix, and who reviewed the fix) into a "news fragment" (a small file containing just enough information to be useful to end users), ``towncrier`` can produce a digest of the changes which is valuable to those who may wish to use the software.
These fragments are also commonly called "topfiles" or "newsfiles" in Twisted parlance.

``towncrier`` works best in a development system where all merges involve closing a ticket.


Quick Start
-----------

Install from PyPI::

    python3 -m pip install towncrier

.. note::

   ``towncrier``, as a command line tool, works on Python 3.5+ only.
   It is usable by projects written in other languages, provided you give it the version of the project when invoking it.
   For Python 2/3 compatible projects, the version can be discovered automatically.

In your project root, add a ``pyproject.toml`` file, with the contents::

    [tool.towncrier]
        package = "mypackage"
        package_dir = "src"
        filename = "NEWS.rst"

Then put news fragments (see "News Fragments" below) into a "newsfragments" directory under your package (so, if your project is named "myproject", and it's kept under ``src``, your newsfragments dir would be ``src/myproject/newsfragments/``).

To prevent git from removing the newsfragments directory, make a ``.gitignore`` file in it with::

    !.gitignore

This will keep the folder around, but otherwise "empty".

``towncrier`` needs to know what version your project is, and there are two ways you can give it:

- For Python 2/3 compatible projects, a ``__version__`` in the top level package.
  This can be either a string literal, a tuple, or an `Incremental <https://github.com/hawkowl/incremental>`_ version.
- Manually passing ``--version=<myversionhere>`` when interacting with ``towncrier``.

To produce a draft of the news file, run::

    towncrier --draft

To produce the news file for real, run::

    towncrier

This command will remove the news files (with ``git rm``) and append the built news to the filename specified in ``towncrier.ini``, and then stage the news file changes (with ``git add``).
It leaves committing the changes up to the user.

If you wish to have content at the top of the news file (for example, to say where you can find the tickets), put your text above a rST comment that says::

  .. towncrier release notes start

``towncrier`` will then put the version notes after this comment, and leave your existing content that was above it where it is.


News Fragments
--------------

``towncrier`` has a few standard types of news fragments, signified by the file extension.
These are:

- ``.feature``: Signifying a new feature.
- ``.bugfix``: Signifying a bug fix.
- ``.doc``: Signifying a documentation improvement.
- ``.removal``: Signifying a deprecation or removal of public API.
- ``.misc``: A ticket has been closed, but it is not of interest to users.

The start of the filename is the ticket number, and the content is what will end up in the news file.
For example, if ticket #850 is about adding a new widget, the filename would be ``myproject/newsfragments/850.feature`` and the content would be ``myproject.widget has been added``.
