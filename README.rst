Hear ye, hear ye, says the ``towncrier``
========================================

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

   ``towncrier``, as a command line tool,  works on Python 3 only.
   It is usable by projects written in other languages, as it does not directly import the project.

In your project root, add a ``towncrier.ini`` file, with the contents:

    [towncrier]
    ; Your project name
    package = mypackage
    ; Where your project is kept -- current dir by default
    package_dir = src/
    ; The filename that it will write to, relative to the current dir
    filename = NEWS.rst

Then put news fragments (see "News Fragments" below) into a "newsfiles" directory under your project.

To produce the news file, run::

    towncrier

This command will remove the news files (with ``git rm``) and append the built news to the filename specified in ``towncrier.ini``, and then stage the news file changes (with ``git add``).
It leaves committing the changes up to the user.


News Fragments
--------------

``towncrier`` has a few standard types of news fragments, signified by the file extension.
These are:

- ``.feature``: Signifying a new feature.
- ``.bugfix``: Signifying a bug fix.
- ``.doc``: Signifying a documentation improvement.
- ``.misc``: A ticket has been closed, but it is not of interest to users.

The start of the filename is the ticket number, and the content is what will end up in the news file.
For example, if ticket #850 is about adding a new widget, the filename would be ``myproject/newsfiles/850.feature`` and the content would be ``myproject.widget has been added``.
